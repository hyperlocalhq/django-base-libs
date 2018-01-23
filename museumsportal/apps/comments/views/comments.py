# -*- coding: UTF-8 -*-
import base64, datetime

from django import forms
from django.core.mail import mail_admins, mail_managers
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import normalize_newlines
from django.utils.translation import ngettext
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.utils.timezone import now as tz_now

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.forms.fields import SecurityField, SingleEmailTextField
from base_libs.middleware import get_current_user

from museumsportal.apps.comments.models import Comment, ModeratorDeletionReason, ModeratorDeletion
from museumsportal.apps.comments.models import RATINGS_REQUIRED, RATINGS_OPTIONAL, IS_PUBLIC

COMMENTS_PER_PAGE = getattr(settings, "COMMENTS_PER_PAGE", 20)

COMMENT_DELETION_REASON_CHOICES = XChoiceList(get_related_queryset(ModeratorDeletion, 'deletion_reason'))

class PublicCommentForm(dynamicforms.Form):
    """
    Form that handles public registered comments
    """
    
    name = forms.CharField(
        label=_("Your Name"),
        required=True, 
        max_length=50,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
    )
    
    email = SingleEmailTextField(
        label=_("Your Email Address"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
    )   
    
    url_link = forms.URLField(
        label=_(u"Your URL"),
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
    ) 
    
    headline = forms.CharField(
        label=_(u"Title"),
        required=False, 
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
    )
    
    comment = forms.CharField(
        label= _("Comment"),
        required=True,
        max_length=3000,
        widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
    )
    
    # prevent from spam
    prevent_spam = SecurityField()
    
    rating1 = forms.ChoiceField(label=_("Rating1"),)
    rating2 = forms.ChoiceField(label=_("Rating2"),)
    rating3 = forms.ChoiceField(label=_("Rating3"),)
    rating4 = forms.ChoiceField(label=_("Rating4"),)
    rating5 = forms.ChoiceField(label=_("Rating5"),)
    rating6 = forms.ChoiceField(label=_("Rating6"),)
    rating7 = forms.ChoiceField(label=_("Rating7"),)
    rating8 = forms.ChoiceField(label=_("Rating8"),)
        
    def __init__(self, user=None, 
                 headline_required=False, ratings_required=False,
                 ratings_range=[], num_rating_choices=None,
                 additional_data=None, *args, **kwargs):
        
        super(PublicCommentForm, self).__init__(*args, **kwargs)
        
        self.additional_data = additional_data
        self.user = user
        
        self.ratings_range, self.num_rating_choices = ratings_range, num_rating_choices
        choices = [(c, c) for c in ratings_range]
        
        for i in range(1, 9):
            self.fields["rating%d" % i].required = ratings_required and num_rating_choices > 0
            self.fields["rating%d" % i].choices = choices
            if len(choices) > 0:
                self.fields["rating%d" % i].initial = choices[0]
            else:
                self.fields["rating%d" % i].initial = None
        
        if user and user.is_authenticated():
            self.fields["name"].required = False
            self.fields["email"].required = False
            self.user_cache = user
        if headline_required:
            self.fields["headline"].required = True
            
        self.helper = FormHelper()
        self.helper.form_tag = False
        if user is None or not user.is_authenticated():
            self.helper.layout = layout.Layout(
                layout.Fieldset(
                    _("Write a comment"),
                    "name",
                    "email",
                    "url_link",
                    "headline",
                    "comment",
                    "prevent_spam",
                    layout.HTML("{{ form.prevent_spam.error_tag }}"),
                    ),
                layout.HTML("""
                    {% load base_tags babel i18n %}
                    {% if comment_form.is_valid %}
                    <fieldset>
                    <legend>{% trans "Preview" %}</legend>
                        <div class="preview">
                            <div>
                                {% if comment.user %}
                                    <span class="no_link">
                                        {{ comment.user.username }}
                                    </span><br />
                                {% else %}
                                    <span class="no_link">
                                        {{ comment.name }}
                                    </span><br />
                                {% endif %}
                                {{ comment.submit_date|datefmt:"long" }}
                            </div>
                            <div class="post_comment">
                               {{ comment.comment|disarm_user_input }}
                            </div>
                        </div>
                    </fieldset>
                    {% endif %}
                """),
                bootstrap.FormActions(
                    layout.HTML("""
                        {% load i18n %}
                        <input type="hidden" class="form_hidden" name="goto_next" value="{% if goto_next %}{{ goto_next }}{% else %}{{ request.get_full_path }}{% endif %}" />
                        <input type="hidden" class="form_hidden" name="options" value="{{ options }}" />
                        <input type="hidden" class="form_hidden" name="target" value="{{ target }}" />
                        <input type="hidden" class="form_hidden" name="gonzo" value="{{ hash }}" />
                        {% if comment_form.is_valid %}
                            <input type="button" id="but_cancel" class="btn" value='{% filter upper %}{% trans "Cancel" %}{% endfilter %}' />&zwnj;
                        {% endif %}
                        <input type="submit" id="but_preview" class="btn btn-primary" value='{% filter upper %}{% trans "Preview" %}{% endfilter %}' />&zwnj;
                        {% if comment_form.is_valid %}
                            <input type="submit" id="but_post" class="button_good" name="post" value='{% filter upper %}{% trans "Post comment" %}{% endfilter %}' />&zwnj;
                        {% endif %}
                        """),
                    )
                )
        else:
            self.helper.layout = layout.Layout(
                layout.Fieldset(
                    _("Write a comment"),
                    "headline",
                    "comment",
                    "prevent_spam",
                    layout.HTML("{{ form.prevent_spam.error_tag }}"),
                ),
                layout.HTML("""
                    {% load base_tags babel i18n %}
                    {% if comment_form.is_valid %}
                    <fieldset>
                    <legend>{% trans "Preview" %}</legend>
                        <div class="preview">
                            <div>
                                {% if comment.user %}
                                    <span class="no_link">
                                        {{ comment.user.username }}
                                    </span><br />
                                {% else %}
                                    <span class="no_link">
                                        {{ comment.name }}
                                    </span><br />
                                {% endif %}
                                 {{ comment.submit_date|datefmt:"long" }}
                            </div>
                            <div class="post_comment">
                                {{ comment.comment|disarm_user_input }}
                            </div>
                        </div>
                    </fieldset>
                    {% endif %}
                """),
                bootstrap.FormActions(
                    layout.HTML("""
                        {% load i18n %}
                        <input type="hidden" class="form_hidden" name="goto_next" value="{% if goto_next %}{{ goto_next }}{% else %}{{ request.get_full_path }}{% endif %}" />
                        <input type="hidden" class="form_hidden" name="options" value="{{ options }}" />
                        <input type="hidden" class="form_hidden" name="target" value="{{ target }}" />
                        <input type="hidden" class="form_hidden" name="gonzo" value="{{ hash }}" />
                        {% if comment_form.is_valid %}
                            <input type="button" id="but_cancel" class="btn" value='{% filter upper %}{% trans "Cancel" %}{% endfilter %}' />&zwnj;
                        {% endif %}
                        <input type="submit" id="but_preview" class="btn btn-primary" value='{% filter upper %}{% trans "Preview" %}{% endfilter %}' />&zwnj;
                        {% if comment_form.is_valid %}
                            <input type="submit" id="but_post" class="btn btn-primary" name="post" value='{% filter upper %}{% trans "Post comment" %}{% endfilter %}' />&zwnj;
                        {% endif %}
                        """),
                    )
                )
            
    def get_comment(self):
        "Helper function"
        # do character encoding
        cleaned = self.cleaned_data
        #for key, value in cleaned.items():
        #    if type(value).__name__ == "unicode":
        #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)

        if self.user and self.user.is_authenticated():
            self.name = self.user.username;
        else:
            self.name = cleaned.get("name", None)
            
        for i in range(1, 9):
            rating = cleaned.get("rating%d" % i, '')
            if rating is not None and len(str(rating)) == 0:
                cleaned["rating%d" % i] = 0

        return Comment(user=self.user,
                       name=self.name,
                       email=cleaned.get("email", None),
                       url_link=cleaned.get("url_link", None),
                       content_type=ContentType.objects.get(
                           pk=self.additional_data["content_type_id"],
                           ),
                       object_id=self.additional_data["object_id"], 
                       headline=cleaned.get("headline", ""),
                       comment=cleaned["comment"].strip(), 
                       rating1=cleaned.get("rating1", 0),
                       rating2=cleaned.get("rating2", 0),
                       rating3=cleaned.get("rating3", 0),
                       rating4=cleaned.get("rating4", 0),
                       rating5=cleaned.get("rating5", 0),
                       rating6=cleaned.get("rating6", 0),
                       rating7=cleaned.get("rating7", 0),
                       rating8=cleaned.get("rating8", 0),
                       valid_rating=cleaned.get("rating1", None) is not None,
                       submit_date=tz_now(),
                       is_public=self.additional_data["is_public"], 
                       ip_address=self.additional_data["ip_address"],
                       is_removed=False,
                       site=Site.objects.get(id=settings.SITE_ID)
                       )

    def save(self):
        today = datetime.date.today()
        c = self.get_comment()
        for old in Comment.objects.filter(content_type__id__exact=self.additional_data["content_type_id"],
            object_id__exact=self.additional_data["object_id"], name__exact=self.name):
            # Check that this comment isn't duplicate. (Sometimes people post
            # comments twice by mistake.) If it is, fail silently by pretending
            # the comment was posted successfully.
            if old.submit_date.date() == today \
                and force_unicode(old.comment) == force_unicode(c.comment) \
                and old.rating1 == c.rating1 and old.rating2 == c.rating2 \
                and old.rating3 == c.rating3 and old.rating4 == c.rating4 \
                and old.rating5 == c.rating5 and old.rating6 == c.rating6 \
                and old.rating7 == c.rating7 and old.rating8 == c.rating8:
                return old
            # If the user is leaving a rating, invalidate all old ratings.
            if c.rating1 is not None:
                old.valid_rating = False
                old.save()
        c.save()
        # If the commentor has posted fewer than COMMENTS_FIRST_FEW comments,
        # send the comment to the managers.
        if self.user and self.user.is_authenticated():
            if self.user_cache.comment_set.count() <= settings.COMMENTS_FIRST_FEW:
                message = ngettext('This comment was posted by a user who has posted fewer than %(count)s comment:\n\n%(text)s',
                    'This comment was posted by a user who has posted fewer than %(count)s comments:\n\n%(text)s', settings.COMMENTS_FIRST_FEW) % \
                    {'count': settings.COMMENTS_FIRST_FEW, 'text': c.get_as_text()}
                mail_managers("Comment posted by rookie user", message)
        if settings.COMMENTS_SKETCHY_USERS_GROUP and settings.COMMENTS_SKETCHY_USERS_GROUP in [g.id for g in self.user_cache.get_group_list()]:
            message = _('This comment was posted by a sketchy user:\n\n%(text)s') % {'text': c.get_as_text()}
            mail_managers("Comment posted by sketchy user (%s)" % self.user_cache.username, c.get_as_text())
        return c
    
class PublicCommentRefuseForm(dynamicforms.Form):
    """
    Form that handles the deletion of public registered comments
    """
    reason = forms.ChoiceField(
        required=True,
        choices=COMMENT_DELETION_REASON_CHOICES,
        label=_("Reason"),
    )

    def __init__(self, comment_id, user=None, *args, **kwargs):
        
        super(PublicCommentRefuseForm, self).__init__(*args, **kwargs)
        
        self.comment_id = comment_id
        self.user = user
        
    def save(self):
        
        cleaned = self.cleaned_data
        #for key, value in cleaned.items():
        #    if type(value).__name__ == "unicode":
        #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)
        
        today = datetime.date.today()

        comment = Comment.objects.get(id=self.comment_id)
        comment.is_removed = True
        comment.save()
        # if this comment has been refused for any reason before, just overwrite...
        try:
            m = ModeratorDeletion.objects.get(comment__id = self.comment_id)
            m.user=self.user
            m.deletion_date=today
            m.deletion_reason=ModeratorDeletionReason.objects.get(id=cleaned['reason'])
        except:
            m = ModeratorDeletion(
                  user=self.user, 
                  comment=Comment.objects.get(id=self.comment_id),
                  deletion_date=today,
                  deletion_reason=ModeratorDeletionReason.objects.get(id=cleaned['reason']),
            )
        m.save()
        
        return comment    

@never_cache
def post_comment(
        request, 
        headline_required=False, 
        template_name='comments/preview.html',
        use_ajax=False, 
        extra_context=None):
    """
    Post a comment

    Redirects to the `comments.comments.comment_was_posted` view upon success or
    to a given redirection (see 'next' below).

    Templates: `comment_preview`
    Context:
        comment
            the comment being posted
        comment_form
            the comment form
        options
            comment options
        target
            comment target
        hash
            security hash (must be included in a posted form to succesfully
            post a comment).
        rating_options
            comment ratings options
        ratings_optional
            are ratings optional?
        ratings_required
            are ratings required?
        rating_range
            range of ratings
        rating_choices
            choice of ratings
        next
            <<redirection URL>>
        extra_context
            dictionary containing extra_context
    """
    if not request.POST:
        raise Http404, "Only POSTs are allowed"
    try:
        options, target, security_hash = request.POST['options'], request.POST['target'], request.POST['gonzo']
        redirect_to = request.POST.get(settings.REDIRECT_FIELD_NAME, '')
    except KeyError:
        raise Http404, "One or more of the required fields wasn't submitted"
    
    photo_options = request.POST.get('photo_options', '')
    rating_options = normalize_newlines(request.POST.get('rating_options', ''))
    
    if Comment.objects.get_security_hash(options, photo_options, rating_options, target) != security_hash:
        raise Http404, "Somebody tampered with the comment form (security violation)"
    
    # Now we can be assured the data is valid.
    if rating_options:
        rating_range, rating_choices = Comment.objects.get_rating_options(base64.decodestring(rating_options))
    else:
        rating_range, rating_choices = [], []
        
    content_type_id, object_id = target.split(':') # target is something like '52:5157'
    try:
        obj = ContentType.objects.get(
            pk=content_type_id,
            ).get_object_for_this_type(pk=object_id)
    except ObjectDoesNotExist:
        raise Http404, "The comment form had an invalid 'target' parameter -- the object ID was invalid"
    option_list = options.split(',') # options is something like 'pa,ra'
    
    data = request.POST.copy()
    data.update(request.FILES)
    
    # additional data passed to the form ...
    additional_data = {}
    additional_data['content_type_id'] = content_type_id
    additional_data['object_id'] = object_id
    additional_data['ip_address'] = request.META.get('REMOTE_ADDR')
    additional_data['is_public'] = IS_PUBLIC in option_list
    
    form = PublicCommentForm(get_current_user(),
        headline_required=headline_required,
        ratings_required=RATINGS_REQUIRED in option_list,
        ratings_range=rating_range,
        num_rating_choices=len(rating_choices),
        additional_data=additional_data,
        data=data)
    
    comment = None
    
    if form.is_valid():
        if 'post' in request.POST:
            # If the IP is banned, mail the admins, do NOT save the comment, and
            # serve up the "Thanks for posting" page as if the comment WAS posted.
            if request.META['REMOTE_ADDR'] in settings.BANNED_IPS:
                mail_admins("Banned IP attempted to post comment", unicode(request.POST) + "\n\n" + unicode(request.META))
            else:
                comment = form.save()
                pass
            if not use_ajax:
                return HttpResponseRedirect("../posted/?c=%s:%s" % (content_type_id, object_id))

            # in the ajax case, page should be reloaded!!!
            else:
                return HttpResponse("reload")

        elif 'preview' in request.POST:
            comment = form.get_comment()
        else:
            raise Http404, _("The comment form didn't provide either 'preview' or 'post'")

    context = {
        'comment': comment,
        'comment_form': form,
        'options': options,
        'target': target,
        'hash': security_hash,
        'rating_options': rating_options,
        'ratings_optional': RATINGS_OPTIONAL in option_list,
        'ratings_required': RATINGS_REQUIRED in option_list,
        'rating_range': rating_range,
        'rating_choices': rating_choices,
        settings.REDIRECT_FIELD_NAME: redirect_to,
    }
        
    if extra_context:
        context.update(extra_context)
    return render_to_response(template_name, context, context_instance=RequestContext(request))

def comment_was_posted(request, template_name='comments/posted.html'):
    """
    Display "comment was posted" success page

    Templates: `comment_posted`
    Context:
        object
            The object the comment was posted on
    """
    obj = None
    if 'c' in request.GET:
        content_type_id, object_id = request.GET['c'].split(':')
        try:
            content_type = ContentType.objects.get(pk=content_type_id)
            obj = content_type.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            pass
    return render_to_response(template_name, {'object': obj}, context_instance=RequestContext(request))

def get_comments(content_type_id, object_id, sort_order = "", extra_kwargs=None):
    get_list_function = Comment.objects.get_list_with_karma
    kwargs = {
        'object_id__exact': object_id,
        'content_type__id__exact': content_type_id,
        'site__id__exact': settings.SITE_ID,
    }
    if extra_kwargs:
        kwargs.update(extra_kwargs)
    if settings.COMMENTS_BANNED_USERS_GROUP:
        kwargs['select'] = {'is_hidden': 'user_id IN (SELECT user_id FROM auth_user_groups WHERE group_id = %s)' % settings.COMMENTS_BANNED_USERS_GROUP}
        
    return get_list_function(**kwargs).order_by(sort_order + 'submit_date').select_related()

def get_rating_list(queryset, rating_map, selected = None):
    """
    help function:
    returns a list of ratings contained in a comment queryset
    the "rating map" contains a mppaing of the "rating index" (1-8),
    and a display value for the templates. For example:
    
    rating_map = [(1, "helpful", _("helpful")),
                  (2, "interesting", _("interesting")),
                 ]
    """
    rating_list = []
    rating_list.append(("all", _("All"), len(queryset) > 0, selected is None))

    for rating in rating_map:
        count = queryset.filter(**{"rating" + str(rating[0]) + "__gt" : 0}).count()
        rating_list.append((str(rating[1]), str(rating[2]), count > 0, selected == str(rating[1])))
    return rating_list

def filter_rating(queryset, rating_map, filter_value):
    """
    help function:
    filters a queryset for a specific year
    """
    rating_index = None
    for rating in rating_map:
        if rating[1] == filter_value:
            rating_index = rating[0]
            break;
            
    if rating_index:
        return queryset.filter(**{"rating" + str(rating_index) + "__gt" : 0}).order_by("-rating" + str(rating_index))
    return queryset

@never_cache
def refuse_comment(
       request, 
       comment_id, 
       template_name,
       redirect_to,
       extra_context=None, 
       use_popup=False,
       **kwargs):

    """
    Displays a refuse comment form and handles the associated action
    Privileges must be handled by a wrapper view!!!!
    """
    comment = Comment.objects.get(id=comment_id)
    user = request.user
    
    if request.method == 'POST':

        # cancel the whole action
        if not use_popup:
            # cancel the whole action
            if request.POST.has_key('cancel'):
                return HttpResponseRedirect(redirect_to)

        data = request.POST.copy()
        data.update(request.FILES)
        form = PublicCommentRefuseForm(comment_id, user, data)
        if form.is_valid():
            form.save()
            if use_popup:
                return HttpResponse("reload")    
            else:
                return HttpResponseRedirect(redirect_to)        

    else:
        form = PublicCommentRefuseForm(comment_id, user)
                
    context = {
        'form': form,
    }
        
    if extra_context:
        context.update(extra_context)
    return render_to_response(template_name, context, context_instance=RequestContext(request))

@never_cache
def accept_comment(
       request, 
       comment_id, 
       template_name,
       redirect_to,
       extra_context=None, 
       use_popup=False,
       **kwargs):

    """
    Displays an accept comment form and handles the associated action.
    Privileges must be handled by a wrapper view!!!!
    """
    comment = Comment.objects.get(id=comment_id)
    # nothing has to be done...
    if not comment.is_removed:
        if not use_popup:
            return HttpResponseRedirect(redirect_to)
    
    if request.method == 'POST':

        # cancel the whole action
        if not use_popup:
            # cancel the whole action
            if request.POST.has_key('cancel'):
                return HttpResponseRedirect(redirect_to)

        comment.is_removed = False
        comment.save()
        try:
            m = ModeratorDeletion.objects.get(comment__id = self.comment_id)
            m.delete()
        except:
            pass
        if use_popup:
            return HttpResponse("reload")    
        else:
            return HttpResponseRedirect(redirect_to)        

    context = {}
    if extra_context:
        context.update(extra_context)
    return render_to_response(template_name, context, context_instance=RequestContext(request))

@never_cache
def mark_as_spam_comment(
       request, 
       comment_id, 
       template_name,
       redirect_to,
       extra_context=None, 
       use_popup=False,
       **kwargs):

    """
    Displays an "mark as spam" comment form and handles the associated action.
    Privileges must be handled by a wrapper view!!!!
    """
    comment = Comment.objects.get(id=comment_id)
    # nothing has to be done...
    if comment.is_spam:
        if not use_popup:
            return HttpResponseRedirect(redirect_to)
    
    if request.method == 'POST':

        # cancel the whole action
        if not use_popup:
            # cancel the whole action
            if request.POST.has_key('cancel'):
                return HttpResponseRedirect(redirect_to)

        comment.is_spam = True
        comment.save()
        if use_popup:
            return HttpResponse("reload")    
        else:
            return HttpResponseRedirect(redirect_to)        

    context = {}
    if extra_context:
        context.update(extra_context)
    return render_to_response(template_name, context, context_instance=RequestContext(request))