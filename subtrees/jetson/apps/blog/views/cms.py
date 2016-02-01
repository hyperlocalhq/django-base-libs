# -*- coding: utf-8 -*-
import re
import datetime
import time

from django.template import loader
from django.template import RequestContext
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _, ugettext
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.fields import DateTimeField
from django.utils.timezone import now as tz_now
from django.shortcuts import get_object_or_404, render

from tagging.models import TaggedItem

from base_libs.views import get_object_from_url
from base_libs.views import get_container
from base_libs.views import access_denied
from base_libs.utils.misc import get_or_404
from base_libs.utils.loader import select_template_name
from base_libs.forms.formprocessing import FormPreviewHandler
from base_libs.forms.formprocessing import ID_ACTION_NEW
from base_libs.forms.formprocessing import ID_ACTION_EDIT
from base_libs.forms.formprocessing import ID_ACTION_DELETE
from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED
from base_libs.models.base_libs_settings import MARKUP_HTML_WYSIWYG

from jetson.apps.utils.views import object_list
from jetson.apps.utils.decorators import login_required

from jetson.apps.blog.models import Blog, Post

from jetson.apps.comments.views.comments import post_comment, refuse_comment
from jetson.apps.comments.views.comments import accept_comment, mark_as_spam_comment

# PRIVATE FUNCTIONS

def _get_archive(container, queryset, extra_context, allow_future, allow_empty):
    """
    Updates the extra context on normal archive views
    and returns the extra context and the queryset
    
    Additional context:
    date_list:     List of years available: 
    """
    date_field = 'published_from'
    if not allow_future:
        queryset = queryset.filter(**{'%s__lte' % date_field: tz_now()})

    date_list = queryset.dates(date_field, 'year')[::-1]
    extra_context['date_list'] = date_list
    if not date_list:
        queryset = Post.objects.none()
        if not allow_empty:
            raise Http404, "No object available"
    else:
        queryset = queryset.order_by('-%s' % date_field)
    
    return (queryset, extra_context)

def _get_year_archive(year, container, queryset, extra_context, allow_future, allow_empty):
    """
    Updates the extra context on year-based views and
    returns the extra context and the queryset
    
    Additional context:
    date_list:     List of months in this year as a tuple: 
                   (month(datetime), has_posts(boolean))
    year:          This year
    """
    date_field = 'published_from'
    now = tz_now()
    
    lookup_kwargs = {'%s__year' % date_field: year}

    """ Only bother to check current date if the year 
    isn't in the past and future objects aren't requested."""
    if int(year) >= now.year and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    date_list = queryset.filter(**lookup_kwargs).dates(date_field, 'month')
    
    month_has_posts_list = []
    for month in date_list:
        month_has_posts_list.append((datetime.datetime(int(year), month.month, 1), True))
    
    if not date_list and not allow_empty:
        raise Http404
    queryset = queryset.filter(**lookup_kwargs)
    extra_context['date_list'] = month_has_posts_list
    extra_context['year'] = year
    extra_context['post_filter'] = year
    return (queryset, extra_context)

def _get_month_archive(year, month, container, queryset, extra_context, allow_future, allow_empty):
    """
    Updates the extra context on month-based views and
    returns the extra context and the queryset
    
    Additional context:
    month:            (date) this month
    next_month:       (date) the first day of the next month, or 
                      None if the next month is in the future
    previous_month:   (date) the first day of the previous month
    day_list          list of days with posts
    """
    month_format='%m'
    date_field='published_from'
    try:
        date = datetime.date(*time.strptime(year+month, '%Y'+month_format)[:3])
    except ValueError:
        raise Http404

    # Calculate first and last day of month, for use in a date-range lookup.
    first_day = date.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1)
    lookup_kwargs = {'%s__range' % date_field: (first_day, last_day)}

    """ Only bother to check current date if the month isn't in
     the past and future objects are requested."""
    if last_day >= tz_now().date() and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = tz_now()
    queryset = queryset.filter(**lookup_kwargs)
    if not queryset and not allow_empty:
        raise Http404
    # Calculate the next month, if applicable.
    if allow_future:
        next_month = last_day + datetime.timedelta(days=1)
    elif last_day < datetime.date.today():
        next_month = last_day + datetime.timedelta(days=1)
    else:
        next_month = None
    day_list = queryset.filter(**lookup_kwargs).dates(date_field, 'day')        
    extra_context['month'] = date
    extra_context['next_month'] = next_month
    extra_context['previous_month'] = first_day - datetime.timedelta(days=1),
    extra_context['day_list'] = day_list
    extra_context['post_filter'] = str(year)+str(month)
    return (queryset, extra_context)

def _get_day_archive(year, month, day, container, queryset, extra_context, allow_future, allow_empty):
    """
    Updates the extra context on day-based views and
    returns the extra context and the queryset
    
    Additional context:
    day:            (datetime) the day
    previous_day:   (datetime) the previous day
    next_day:       (datetime) the next day, or None if the 
                    current day is today
    """
    date_field='published_from'
        
    try:
        date = datetime.date(int(year), int(month), int(day))
    except ValueError:
        raise Http404

    model = queryset.model
    now = tz_now()

    if isinstance(model._meta.get_field(date_field), DateTimeField):
        lookup_kwargs = {'%s__range' % date_field: (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max))}
    else:
        lookup_kwargs = {date_field: date}

    if date >= now.date() and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    queryset = queryset.filter(**lookup_kwargs)
    if not allow_empty and not queryset:
        raise Http404

    # Calculate the next day, if applicable.
    if allow_future:
        next_day = date + datetime.timedelta(days=1)
    elif date < datetime.date.today():
        next_day = date + datetime.timedelta(days=1)
    else:
        next_day = None

    extra_context['day'] = date
    extra_context['next_day'] = next_day
    extra_context['previous_day'] = date - datetime.timedelta(days=1)
    extra_context['post_filter'] = str(year)+str(month)
    return (queryset, extra_context)

def _get_tag_archive(tag, container, queryset, extra_context, allow_future, allow_empty):
    """
    Updates the extra context on tag-based views and
    returns the extra context and the queryset
    
    Additional context:
    tag:      the tag to be displayed
    """
    queryset = TaggedItem.objects.get_union_by_model(queryset, [tag])
    extra_context['tag'] = tag
    extra_context['post_filter'] = tag  
    return (queryset, extra_context)      

# PUBLIC FUNCTIONS

def get_blog_params(request, post_slug=None, **kwargs):
    """
    gets some parameters. 
    It is used by the view functions and for form processing.
    Returns the parsed and calculated parameters as a 
    dictionary. This later can be used is extra_context
    in the rendered templates or for other purposes.
    """
    base_template = None
    # obj = request.current_page
    url_identifier = request.current_page.get_path()
    obj = None
    current_post = None
    site = None
    if kwargs.has_key('only_for_this_site'):
        if kwargs['only_for_this_site']:
            site = Site.objects.get_current()
            
    container = get_container(Blog, site, obj, url_identifier, create=False)
    
    # try to resolve post from slug
    if post_slug:
        current_post = get_or_404(Post, slug=post_slug)
 
    extra_context = {'container': container, 'object': obj}
    if obj:
        extra_context['object_change_permission'] = u"%s.%s" % (
            obj._meta.app_label,
            obj._meta.get_change_permission(),
            )
    else:
        extra_context['object_change_permission'] = ""
    extra_context['current_post'] = current_post
    extra_context['base_template'] = base_template or "blog/base.html"
    extra_context['post_filter'] = 'all'
    extra_context['nof_drafts'] = Post.draft_objects.filter(blog=container).count()
      
    return extra_context
    
def get_archives(queryset):
    """
    returns a list of tuples with years and lists of months for article archives
    e.g., (2009, ((2, "Feb"),(1, "Jan"),)),(2008, ((3, "Mar"),))
    """
    months = [_('Jan'), _('Feb'), _('Mar'), _('Apr'), _('May'), _('Jun'), 
              _('Jul'), _('Aug'), _('Sep'), _('Oct'), _('Nov'), _('Dec')]
    archives = {}
    for i in queryset.dates('published_from', 'month', order="DESC"):
        year = i.year
        month = i.month
        if year not in archives:
            archives[year] = []
            archives[year].append((month, months[month - 1])) 
        else: 
            if month not in archives[year]: 
                archives[year].append((month, months[month - 1]))
    return sorted(archives.items(),reverse=True)
    
def handle_request(request, year=None, month=None, day=None, post_slug=None, tag=None, status=STATUS_CODE_PUBLISHED,
                   paginate_by=None, page=None, allow_future=False, allow_empty=True, extra_context=None,
                   context_processors=None, **kwargs):
    """
    handles a blog request 
    We do not provide separate view functions for 
    date based and non date based views. This method
    avoids code redundancy! 
       
    Context (provided as extra_context):
    
    object           The object related to the blog container (or None)
    container        The blog container (defined by the rel. object)

    """
    if not extra_context:
        extra_context = {}

    template_object_name='post'
        
    # first of all, get blog parameters from the url parts...
    extra_context = get_blog_params(request, post_slug, **kwargs)
    extra_context[settings.REDIRECT_FIELD_NAME] = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    container = extra_context['container']
    
    #check some permissions
    if status == STATUS_CODE_DRAFT:
        if not request.user.has_perm("blog.change_blog_posts", container):
            return access_denied(request)

    template_name = select_template_name("blog", extra_context['object'], "blog")
    
    if status == STATUS_CODE_PUBLISHED:
        queryset = Post.published_objects.filter(blog=container)
    elif status == STATUS_CODE_DRAFT:
        queryset = Post.draft_objects.filter(blog=container)
    else:
        raise NotImplementedError, "You provided an unknown status. Cannot continue."                

    archives = get_archives(queryset)
    
    archive = 'archive'
    (queryset, extra_context) = _get_archive(container, queryset, extra_context,
                                     allow_future, allow_empty)
    
    # the detail archive
    if post_slug:
        # this is used for the previous-next context processors
        extra_context['archives'] = archives
        extra_context['archive'] = 'details'
        extra_context['post_filter'] = 'details'
        
        # get post to incremnt views... 
        # TODO find a generic mechanism for incrementing views.
        post = get_object_or_404(Post, slug=post_slug)
        post.increase_views()
        extra_context['object'] = post

        return render(request, template_name, extra_context)
    
    # the list archives
    if tag:
        archive = 'tag_archive'
        (queryset, extra_context) = _get_tag_archive(tag, container, queryset, 
                                        extra_context, allow_future, allow_empty)        
    elif day:
        archive = 'day_archive'
        (queryset, extra_context) = _get_day_archive(year, month, day, container, 
                                         queryset, extra_context,
                                         allow_future, allow_empty)        
    elif month:
        archive = 'month_archive'
        (queryset, extra_context) = _get_month_archive(year, month, container, 
                                         queryset, extra_context,
                                         allow_future, allow_empty)        
    elif year: # the year archive
        archive = 'year_archive'
        (queryset, extra_context) = _get_year_archive(year, container, 
                                         queryset, extra_context,
                                         allow_future, allow_empty)
    
    extra_context['archive'] = archive        
    extra_context['archives'] = archives
    
    return object_list(request, queryset, 
        paginate_by=paginate_by, page=page, allow_empty=True, 
        template_name=template_name, template_loader=loader,
        extra_context=extra_context, context_processors=context_processors,
        template_object_name=template_object_name, content_type=None)
           
class BlogPostFormPreviewHandler(FormPreviewHandler):    
    """
    Handler for new/edit/delete blog post form
    """    
    @never_cache
    def __call__(self, request, *args, **kwargs):
        from base_libs.forms.formprocessing import ALLOWED_ACTIONS, ID_ACTION_DELETE

        
        """ 
        The call method acts as an action dispatcher. 
        """
        # first, parse the desired action from the kwargs.
        if kwargs.has_key('action'):
            action = kwargs['action']
            """ Checks for allowed actions """
            if action not in ALLOWED_ACTIONS:
                raise AttributeError, "You have defined an invalid action '%s' in your %s form call. Allowed actions are %s." % (action, self.__class__.__name__, str(ALLOWED_ACTIONS))
            self.context['form_action'] = self._check_name(action)
            self.action = action
        else:
            raise AttributeError, "You must provide an 'action' parameter in your %s call. Please correct." % self.__class__.__name__

        # get extra params and extra inits        
        self.extra_context = self.parse_extra_params(request, *args, **kwargs)
        
        # check, if the whole action is allowed!
        check = self.check_allowed(request, action)
        if isinstance(check, (HttpResponseRedirect, HttpResponse, HttpResponseForbidden)):
            return check
        
        warnings = self.check_warnings(request, action)
        if warnings:
            self.context['warnings'] = warnings

        # get the submit_action from the post (or default to 'start')
        submit_action = 'start'
        for key, val in request.POST.items():
            regex = re.match('submit_(.*)', key)
            if regex:
                submit_action = regex.group(1)
                break

        # delete action is detached from the others!
        if action == ID_ACTION_DELETE:
            if not self.confirm_delete or submit_action == 'delete':
                return self.delete(self.get_object())

        if submit_action == 'cancel':
            return self.cancel(self.action)
        else: # the rest of the actions: 'post' and others defined in subclasses ('preview', etc.)
            try:
                method = getattr(self, submit_action)
            except AttributeError:
                raise AttributeError, "Tried to call non existent method '%s' in the %s form subclass. Please correct." % (submit_action, self.__class__.__name__)
            return method(request, action)
            
    def parse_extra_params(self, *args, **kwargs):
        extra_context = get_blog_params(*args, **kwargs)
        self.container = extra_context['container']
        self.current_post = extra_context['current_post']
        self.only_for_this_site = kwargs.get("only_for_this_site", False)
        return extra_context

    def get_form_template(self, use_ajax):
        return select_template_name("post", self.container, "blog/forms", use_ajax)    
        
    def get_confirm_delete_template(self, use_ajax):
        return select_template_name("confirm_delete", self.container, "blog/forms", use_ajax)
        
    def check_allowed(self, request, action):
        #check privileges
        if action == 'new':
            if (not request.user.has_perm("blog.add_blog_posts", self.container)  and (
                not self.container.content_object or 
                not request.user.has_perm("%s.change_%s" % (self.container.content_type.app_label,self.container.content_type.model.lower()), self.container.content_object)
                )):
                return access_denied(request)
        elif action == 'edit':
            if not request.user.has_perm("blog.change_blog_posts", self.container):
                return access_denied(request)
        elif action == 'delete':
            if not request.user.has_perm("blog.delete_blog_posts", self.container):
                return access_denied(request)

    def get_object(self):
        return self.current_post
        
    def get_edit_data(self, obj):
        return {
            'title' : obj.title,
            'body' : obj.body,
            'tags' : obj.tags,
            #'enable_comment_form' : obj.enable_comment_form,
            'status' : obj.status,
            'published_from' : obj.published_from, 
            'published_till' : obj.published_till,
        }
        
    def redirect(self, action):
        if action == ID_ACTION_DELETE:
            return HttpResponseRedirect(self.container.get_url_path())
                        
        if self.current_post and self.current_post.status == STATUS_CODE_PUBLISHED:
            return HttpResponseRedirect(self.current_post.get_url_path())
        else:
            return HttpResponseRedirect(self.container.get_url_path())
        
    def cancel(self, action):
        return self.redirect(action)
    
    def save_new(self, cleaned):
        if not self.container.pk:
            site = None
            if self.only_for_this_site:
                site = Site.objects.get_current()
            if site:
                self.container.create_for_site(site)
            else:
                self.container.save()
        post = Post(
             blog = self.container,
             title = cleaned['title'],
             body = cleaned['body'],
             body_markup_type = MARKUP_HTML_WYSIWYG,
             tags = cleaned['tags'],
             #enable_comment_form = cleaned['enable_comment_form'],
             status = cleaned['status'],
             published_from = cleaned['published_from'], 
             published_till = cleaned['published_till'],
             )            
        post.save()
        return self.redirect(ID_ACTION_NEW)
    
    def save_edit(self, object, cleaned):
        post = object
        post.title = cleaned['title']
        post.body = cleaned['body']
        post.body_markup_type = MARKUP_HTML_WYSIWYG
        post.tags = cleaned['tags']
        #post.enable_comment_form = cleaned['enable_comment_form']
        post.status = cleaned['status']
        post.published_from = cleaned['published_from']
        post.published_till = cleaned['published_till']
        post.save()
        return self.redirect(ID_ACTION_EDIT)
  
    def delete(self, object):
        object.delete()
        return self.redirect(ID_ACTION_DELETE)

def blog_feed(request, 
      feed_type, status=STATUS_CODE_PUBLISHED, **kwargs):
    """
    wrapper for feeds
    """
    context = get_blog_params(request, **kwargs)
    obj = context['object']
    if obj:
        context['object_id'] = obj.id
    else:
        context['object_id'] = None
        
    kwargs.update(context)
    feed = kwargs[feed_type]

    return feed(**kwargs)(request)

@never_cache
def blog_post_comment(request, 
      post_slug, extra_context=None, use_ajax=False, **kwargs):
  
    # first of all, get blog parameters from the url parts...
    extra_context = (get_blog_params(request, post_slug, **kwargs))
    container = extra_context['container']
    obj = extra_context['object']
    post = extra_context['current_post']
    template_name = select_template_name("form", container, "blog/comments", use_ajax)
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    
    if not post.enable_comment_form:
        raise Http404, ugettext("Comments are disabled")
    
    if request.method == 'POST':
        if request.POST.has_key('post'):
            
            post_comment(request, template_name=template_name, use_ajax=use_ajax)
            if not use_ajax:
                redirect_to += "#comments"
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponse("reload")
                
        # the normal preview is done ...
        elif request.POST.has_key('preview'):
            return post_comment(request, template_name=template_name, use_ajax=use_ajax, extra_context=extra_context)
        #cancel
        else:
            if not use_ajax:
                redirect_to += "#comments"
                return HttpResponseRedirect(redirect_to)
            
    from django.template import Template
    # we need to get the post from the post_slug ...
    t = Template("""
        {% load comments %}
        {% comment_form using "blog/comments/form_embedded.html" for blog.post current_post.id %}
        """)
    c = RequestContext(request, extra_context)
    return HttpResponse(t.render(c))

def blog_modify_comment(request, comment_id, 
    action, extra_context=None, use_ajax=False, use_popup=True, **kwargs):
    """
    Displays the refuse/accept/mark_as_spam comment form 
    and handles the associated action
    """
    # first of all, get blog parameters from the url parts...
    extra_context = (get_blog_params(request, **kwargs))
    container = extra_context['container']
    obj = extra_context['object']
    
    template_name = select_template_name(action, container, "blog/comments", use_popup or use_ajax)
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')

    # check permissions
    if not request.user.has_perm("blog.moderate_blog_comments", container):
        return access_denied(request)
    extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
    
    if action == "refuse":
        f = refuse_comment
    elif action == "accept":
        f = accept_comment
    elif action == "mark_as_spam":
        f = mark_as_spam_comment
    else:
        return
        
    return f(request, comment_id, template_name, redirect_to, extra_context, use_popup)   


