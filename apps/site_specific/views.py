# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.conf import settings
# json related stuff
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

image_mods = models.get_app("image_mods")

from base_libs.middleware import get_current_language
from base_libs.utils.misc import get_installed
from base_libs.views import access_denied

from jetson.apps.utils.decorators import login_required
from jetson.apps.structure.models import Term, ContextCategory
from jetson.apps.location.models import LocalityType
from jetson.apps.comments.models import Comment
from jetson.apps.comments.views.comments import post_comment

from ccb.apps.people.models import Person, URL_ID_PERSON
from ccb.apps.institutions.models import Institution, URL_ID_INSTITUTION
from ccb.apps.events.models import Event, URL_ID_EVENT, URL_ID_EVENTS
from ccb.apps.resources.models import Document, URL_ID_DOCUMENT
from ccb.apps.groups_networks.models import PersonGroup, URL_ID_PERSONGROUP
from ccb.apps.marketplace.models import JobOffer, URL_ID_JOB_OFFER, URL_ID_JOB_OFFERS, \
    SECURITY_SUMMAND as MARKETPLACE_SECURITY_SUMMAND
from ccb.apps.site_specific.forms import ClaimForm
from ccb.apps.site_specific.forms import people as people_forms
from ccb.apps.site_specific.forms import institutions as institutions_forms
from ccb.apps.site_specific.forms import resources as resources_forms
from ccb.apps.site_specific.forms import events as events_forms
from ccb.apps.site_specific.forms import groups_networks as groups_networks_forms
from ccb.apps.site_specific.forms import marketplace as marketplace_forms
from ccb.apps.site_specific.forms import InvitationForm
from ccb.apps.site_specific.forms import ProfileDeletionForm
from ccb.apps.site_specific.forms import ObjectDeletionForm
from ccb.apps.site_specific.forms import KreativArbeitenContactForm

BROWSING_CRITERIA = {
    "creative-sector": Term.objects.filter(
        vocabulary__sysname="categories_creativesectors",
    ),
    "context-category": ContextCategory.objects.all(),
    "location-type": LocalityType.objects.all(),
}

TYPE_2_MODEL = {
    URL_ID_PERSON: {
        'model': Person,
        'form_namespace': people_forms,
        'slug_field': "user__username",
        'change_perm': "people.change_person",
        'template_folder': "people",
    },
    URL_ID_INSTITUTION: {
        'model': Institution,
        'form_namespace': institutions_forms,
        'slug_field': 'slug',
        'change_perm': "institutions.change_institution",
        'template_folder': "institutions",
    },
    URL_ID_DOCUMENT: {
        'model': Document,
        'form_namespace': resources_forms,
        'slug_field': 'slug',
        'change_perm': "resources.change_document",
        'template_folder': "resources/documents",
    },
    URL_ID_EVENT: {
        'model': Event,
        'form_namespace': events_forms,
        'slug_field': 'slug',
        'change_perm': "events.change_event",
        'template_folder': "events",
    },
    URL_ID_PERSONGROUP: {
        'model': PersonGroup,
        'form_namespace': groups_networks_forms,
        'slug_field': 'slug',
        'change_perm': "groups_networks.change_persongroup",
        'template_folder': "groups_networks/persongroups",
    },
    URL_ID_JOB_OFFER: {
        'model': JobOffer,
        'form_namespace': marketplace_forms,
        'slug_field': 'slug',
        'get_object': lambda slug: get_object_or_404(JobOffer, **{
            'pk': int(slug) - MARKETPLACE_SECURITY_SUMMAND,
        }),
        'change_perm': "marketplace.change_joboffer",
        'template_folder': "marketplace",
    },
}


def get_browse_queryset(request, use_httpstate=False, **kwargs):
    """
    helper method to get the search results from a request.GET
    """

    # first get the browsing filters from the httpstate ...
    if use_httpstate:
        browsing_filters = request.httpstate['browsing_filters']
    else:
        browsing_filters = dict([(item[0], item[1]) for item in request.GET.items() if item[0] in BROWSING_CRITERIA])

    queryset = kwargs['queryset']
    selected_cats = []
    for k, v in browsing_filters.items():
        if type(v).__name__ in ("str", "unicode"):
            v = get_object_or_404(BROWSING_CRITERIA[k], slug=v)
            browsing_filters[k] = v
        if k == "creative-sector":
            queryset = queryset.filter(
                creative_sectors__lft__gte=v.lft,
                creative_sectors__rght__lte=v.rght,
                creative_sectors__tree_id=v.tree_id,
            )
        elif k == "context-category":
            queryset = queryset.filter(
                context_categories__lft__gte=v.lft,
                context_categories__rght__lte=v.rght,
                context_categories__tree_id=v.tree_id,
            )
        elif k == "location-type":
            queryset = queryset.filter(
                locality_type__lft__gte=v.lft,
                locality_type__rght__lte=v.rght,
                locality_type__tree_id=v.tree_id,
            )
        v.criterion = k
        selected_cats.append(v)
    kwargs['queryset'] = queryset
    if selected_cats:
        if 'extra_context' not in kwargs:
            kwargs['extra_context'] = {}
        kwargs['extra_context']['selected_browsing_cats'] = selected_cats

    kwargs["query"] = "&".join(["%s=%s" % (k, v.slug) for k, v in browsing_filters.items()])

    return kwargs


def splash_page(request):
    """
    Displays the starting page of the website
    """
    request.httpstate['browsing_filters'] = {}
    return render_to_response("index.html", {}, context_instance=RequestContext(request))


def get_vcard(request, content_type_id, object_id):
    """
    calculates a vCard of a person or institution 
    """

    content_type = ContentType.objects.get(id=content_type_id)
    if content_type.model in ('person', 'institution'):
        try:
            instance = content_type.get_object_for_this_type(pk=object_id)
        except Exception:
            raise Http404
        primary_contact = instance.get_contacts()
        if primary_contact:
            primary_contact = primary_contact[0]
            output = primary_contact.get_vcard().read()
            filename = "%s.vcf" % (instance.get_slug())
            # response = HttpResponse(output, content_type="text/x-vcard")
            response = HttpResponse(output, content_type="text/javascript")
            response['Content-Disposition'] = 'inline; filename="%s"' % filename
            return response

    raise Http404, _("Sorry, no vCard available")


@never_cache
def wrap_post_comment(request, slug, year=0, month=0, day=0, template_name='comments/preview.html'):
    """ 
    a wrapper function for the post_comment function from 
    ccb.comments.models.Comment (see there)
    Here it is used for the reviews (but we laeave the name post_"COMMENT")
    """
    # if there is a 'post' key in the post, the comment is published. we do the redirection then
    redirect_to = request.POST.get(settings.REDIRECT_FIELD_NAME, '')
    # Light security check -- make sure redirect_to isn't garbage.
    if not redirect_to or '://' in redirect_to or ' ' in redirect_to:
        redirect_to = '/'

    if request.POST.has_key('post'):
        response = post_comment(request)
        return HttpResponseRedirect(redirect_to)

        # the normal preview is done ...
    elif request.POST.has_key('preview'):

        # Hi Aidas, is there a way to make that simpler?
        target = request.POST['target']
        content_type_id, object_id = target.split(':')  # target is something like '52:5157'
        try:
            content_type = ContentType.objects.get(id=content_type_id)
            model = content_type.model_class()
        except ObjectDoesNotExist:
            raise Http404, _("The comment form had an invalid 'target' parameter -- the object ID was invalid")

        if model.__name__ in ("Person", "Institution", "Event", "Document"):
            object_type = model.__name__
        else:
            object_type = "NOTHING"

        return post_comment(request,
                            headline_required=True,
                            template_name=template_name,
                            extra_context={'object_type': object_type})
        # cancel
    else:
        return HttpResponseRedirect(redirect_to)


def delete_review(request, slug, id, year=0, month=0, day=0, template_name='site_specific/review_delete.html'):
    """
    Displays the delete review form and handles the associated action
    """
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')

    # get the comment and make some security checks...
    allowed = None
    try:
        comment = Comment.objects.get(id=id)
        if comment.content_type.model == "person" and request.user.has_perm('person.can_change'):
            allowed = True
        elif comment.content_type.model == "institution" and request.user.has_perm('institution.can_change'):
            allowed = True
        elif comment.content_type.model == "document" and request.user.has_perm('institution.can_change'):
            allowed = True
        elif comment.content_type.model == "event" and request.user.has_perm('institution.can_change'):
            allowed = True
        else:
            allowed = False
    except Exception:
        comment = None

    if not comment:
        raise Http404, _("There is no object available")

    if not allowed:
        raise Http404, _("You are not allowed to access the required object")

    if request.POST:
        # cancel the whole action
        if request.POST.has_key('cancel'):
            return HttpResponseRedirect(redirect_to)

        elif request.POST.has_key('delete'):
            comment.delete()
            return HttpResponseRedirect(redirect_to)

    return render_to_response(template_name, {
        settings.REDIRECT_FIELD_NAME: redirect_to,
    }, context_instance=RequestContext(request))

# def json_review_add_rating(request, rate_index, object_id):
#     """
#     Increments the review rating.
#     """
#     json_data = "false"
#     result = {}
#
#     comment = Comment.objects.get(id = object_id)
#
#     """
#     As Reinhard decided, only authenticated users may access the rating!!!
#     """
#     if request.user and request.user.is_authenticated():
#         UserRating.objects.rate(comment, request.user, int(rate_index))
#
#     result.update({
#         'id': comment.id,
#         'rating1': comment.rating1,
#         'rating2': comment.rating2,
#         'rating3': comment.rating3,
#         'can_rate1': UserRating.objects.can_rate(comment, request.user, 1),
#         'can_rate2': UserRating.objects.can_rate(comment, request.user, 2),
#         'can_rate3': UserRating.objects.can_rate(comment, request.user, 3),
#         })
#
#     json_data = json.dumps(result, ensure_ascii=False, cls=ExtendedJSONEncoder)
#     return HttpResponse(json_data, content_type='text/javascript; charset=utf-8')
#
# json_review_add_rating = never_cache(json_review_add_rating)


"""
this is the binary search version of get_index, which does not work, because
you cannot filter or get after slicing a queryset...
   
def get_index(queryset, low_index = 0, high_index = -1, **kwargs):
    '''
    get the "rownumber" from of a given query matching exactly one! item
    defined by the **kwargs. On no match, two or more, -1 is returned
    '''
    
    if high_index == -1:
        high_index = queryset.count()
        
    mid_index = high_index / 2
    
    q_low = queryset[low_index:mid_index]
    q_high = queryset[mid_index + 1: high_index]
    
    found = q_low.get(**kwargs)
    
    #perform a binary search
    try:
        found = q_low.get(**kwargs)
        b=n        
        if high_index - low_index == 1:
            return low_index
        else:
            b=n
            return get_index(queryset, low_index, mid_index, **kwargs)
    except Exception:
        try:
            found = q_high.get(**kwargs)
            b=n
            return get_index(queryset, mid_index + 1, high_index, **kwargs)
        except Exception:
            c=b
            return -1
"""


def popup_window(request, window_type):
    """
    Shows the content of POPUP window and manipulates forms in POPUPS
    returns 
    1. HTML with a form to show
    2. Empty string for closing popup
    3. "reload" for reloading the page
    """
    if window_type == "choose-profile":
        return render_to_response(
            "site_specific/popups/choose_profile.html",
            {},
            RequestContext(request),
        )
    elif window_type == "delete-contact":
        try:
            context_item_type = request.GET['type']
            slug = request.GET['slug']
            index = int(request.GET['index'])
            spec = TYPE_2_MODEL[context_item_type]
            obj = spec['model'].objects.get(**{spec['slug_field']: slug})
            contact = obj.get_contacts()[index]
        except Exception:
            raise Http404()
        if not request.user.has_perm(
                "%s.change_%s" % (
                type(obj)._meta.app_label,
                type(obj).__name__.lower(),
            ),
            obj,
        ):
            raise Http404()
        if request.method == "POST":
            contact.delete()
            return HttpResponse("reload")  # close popup
        return render_to_response(
            "site_specific/popups/delete_contact.html",
            {
                'contact': contact,
                'context_item_type': context_item_type,
                'slug': slug,
            },
            RequestContext(request),
        )
    elif window_type == "delete-avatar":
        try:
            context_item_type = request.GET['type']
            slug = request.GET['slug']
            spec = TYPE_2_MODEL[context_item_type]
            obj = spec['model'].objects.get(**{spec['slug_field']: slug})
        except Exception:
            raise Http404, "Object does not exist"
        if not request.user.has_perm(
                "%s.change_%s" % (
                type(obj)._meta.app_label,
                type(obj).__name__.lower(),
            ),
            obj,
        ):
            raise Http404, "No permission to delete"
        if request.method == "POST":
            image_mods.FileManager.delete_file_for_object(obj, field_name="image")
            return HttpResponse("reload")  # close popup
        return render_to_response(
            "site_specific/popups/delete_avatar.html",
            {
                'object': obj,
                'context_item_type': context_item_type,
                'slug': slug,
            },
            RequestContext(request),
        )
    raise Http404, "Popup does not exist"


@never_cache
def edit_profile(request, object_type, slug, section_name="", index=None):
    specifics = TYPE_2_MODEL[object_type]

    # get or define the function for retrieving a specific object from the given slug
    get_object = specifics.get(
        "get_object",
        lambda slug: get_object_or_404(
            specifics['model'],
            **{specifics.get("slug_field", "slug"): slug}
        )
    )
    instance = get_object(slug)
    if not request.user.has_perm(specifics['change_perm'], instance):
        return access_denied(request)
    if not section_name:
        return HttpResponse("")
    section_template = "%s/profile/%s_form.html" % (
        specifics['template_folder'],
        section_name,
    )

    form_class = specifics['form_namespace'].profile_forms.get(section_name, False)
    formset_classes = getattr(
        specifics['form_namespace'],
        "profile_formsets",
        {},
    ).get(section_name, {})

    formsets = {}
    if not form_class:
        raise Http404()
    show_form = True
    if request.method == "POST":
        form = form_class(instance, index, request.POST, request.FILES)

        formsets_are_valid = True
        data = request.POST.copy()
        for formset_name, formset_settings in formset_classes.items():
            formsets[formset_name] = formset_settings['formset'](
                instance,
                index,
                formset_settings['get_instances'],
                data=data,
                files=request.FILES,
                prefix=formset_name,
            )
            # bitwise "&" works as expected for boolean values
            formsets_are_valid &= formsets[formset_name].is_valid()

        if form.is_valid() and formsets_are_valid:
            form.save()
            for formset_name, formset in formsets.items():
                get_instances = formset_classes[formset_name]['get_instances']
                saved_instance_pks = []
                for f in formset.forms:
                    if (
                        f.is_valid() and
                        not f.cleaned_data.get("DELETE", False)
                    ):
                        obj = f.save()
                        saved_instance_pks.append(obj.pk)
                # delete unused event times
                get_instances(instance).exclude(
                    pk__in=saved_instance_pks,
                ).delete()

            section_template = "%s/profile/%s.html" % (
                specifics['template_folder'],
                section_name,
            )
            show_form = False
    else:
        form = form_class(instance, index)

        for formset_name, formset_settings in formset_classes.items():
            formsets[formset_name] = formset_settings['formset'](
                instance,
                index,
                formset_settings['get_instances'],
                prefix=formset_name,
            )

    extra_context = form.get_extra_context()
    t = loader.get_template("%s/profile/helper.html" % (
        specifics['template_folder'],
    ))
    c = {
        'object': instance,
        'form': show_form and form,
        'formsets': show_form and formsets,
        'index': index,
        'section_template': section_template,
    }
    c.update(extra_context)
    res = t.render(RequestContext(request, c))
    response = HttpResponse(res)
    # response['Content-Type'] = "text/plain; charset=utf-8"
    response['Pragma'] = "No-Cache"
    return response


def show_contact(request, object_type, slug, index="all"):
    specifics = TYPE_2_MODEL[object_type]
    instance = get_object_or_404(
        specifics['model'],
        **{specifics['slug_field']: slug}
    )
    if index.isdigit():
        index = int(index)
        t = loader.get_template("%s/profile/map_contact.html" % (
            specifics['template_folder'],
        ))
        c = {
            'object': instance,
            'contact': instance.get_contacts()[int(index)],
            'index': index,
        }
    else:
        t = loader.get_template("%s/profile/map_contacts.html" % (
            specifics['template_folder'],
        ))
        c = {
            'object': instance,
        }
    res = t.render(RequestContext(request, c))
    response = HttpResponse(res)
    response['Content-Type'] = "text/plain; charset=utf-8"
    response['Pragma'] = "No-Cache"
    return response


def redirect_to_creative_sector(request):
    redirect_to = "/"
    if "creative_sector" in request.POST:
        redirect_to = "/creative-sector/%s/" % (
            request.POST["creative_sector"],
        )
    return HttpResponseRedirect(redirect_to)

# maps url parts to class names and template names
CLAIM_CLASS_MAPPER = {
    'institution': (
        Institution,
        'institutions/claim_institution.html',
        'institutions/claim_institution_done.html'
    ),
    'event': (
        Event,
        'events/claim_event.html',
        'events/claim_event_done.html'
    ),
    'document': (
        Document,
        'resources/documents/claim_document.html',
        'resources/documents/claim_document_done.html'
    ),
}


def claim_object(request, **kwargs):
    """
    processes a "claim" request
    """
    ot_url_part = kwargs.get('ot_url_part', None)
    if not ot_url_part:
        raise Http404, "You must specify an object class"
    try:
        mapped_model = CLAIM_CLASS_MAPPER[ot_url_part][0]
    except Exception:
        raise Http404, "Unsupported object class"
    try:
        obj = mapped_model.objects.get(slug=kwargs['slug'])
    except Exception:
        raise Http404, "Object not found for given slug"

    if not obj.is_claimable():
        raise Http404, "Sorry, You cannot claim this object"

    content_type = ContentType.objects.get_for_model(mapped_model)
    object_id = obj.id

    if request.method == 'POST':
        data = request.POST.copy()

        form = ClaimForm(
            content_type=content_type,
            object_id=object_id,
            data=data,
        )

        if form.is_valid():
            form.save()
            template_done_name = CLAIM_CLASS_MAPPER[ot_url_part][2]
            return render_to_response(template_done_name, {
                'object': obj
            }, context_instance=RequestContext(request))
    else:
        form = ClaimForm(
            content_type=content_type,
            object_id=object_id
        )

    template_name = CLAIM_CLASS_MAPPER[ot_url_part][1]
    return render_to_response(template_name, {
        'form': form,
        'object': obj
    }, context_instance=RequestContext(request))


claim_object = login_required(claim_object)

DELETE_CLASS_MAPPER = {
    URL_ID_EVENT: {
        'model': Event,
        'get_object': lambda slug: Event.objects.get(slug=slug),
        'deletion_template': 'events/delete_event.html',
        'embedded_deletion_template': 'events/delete_event_embedded.html',
        'success_redirect': '/%s/' % URL_ID_EVENTS,
    },
    URL_ID_JOB_OFFER: {
        'model': JobOffer,
        'get_object': lambda slug: get_object_or_404(JobOffer, **{
            'pk': int(slug) - MARKETPLACE_SECURITY_SUMMAND,
        }),
        'deletion_template': 'marketplace/delete_job_offer.html',
        'embedded_deletion_template': 'marketplace/delete_job_offer_embedded.html',
        'success_redirect': '/%s/' % URL_ID_JOB_OFFERS,
    },
}


def delete_object(request, **kwargs):
    """
    processes a "delete" request
    """
    ot_url_part = kwargs.get('ot_url_part', None)
    if not ot_url_part:
        raise Http404, "You must specify an object class"
    try:
        get_object = DELETE_CLASS_MAPPER[ot_url_part]['get_object']
    except Exception:
        raise Http404, "Unsupported object class"
    try:
        obj = get_object(kwargs['slug'])
    except Exception:
        raise Http404, "Object not found for given slug"

    if not obj.is_deletable():
        raise Http404, "Sorry, You cannot delete this object"

    if request.method == 'POST':
        form = ObjectDeletionForm(obj, data=request.POST)
        if form.is_valid():
            form.delete()
            if request.is_ajax():
                return HttpResponse("redirect=%s" % DELETE_CLASS_MAPPER[ot_url_part]['success_redirect'])
            else:
                return HttpResponseRedirect(DELETE_CLASS_MAPPER[ot_url_part]['success_redirect'])
    else:
        form = ObjectDeletionForm(obj)

    if request.is_ajax():
        template_name = DELETE_CLASS_MAPPER[ot_url_part]['embedded_deletion_template']
    else:
        template_name = DELETE_CLASS_MAPPER[ot_url_part]['deletion_template']
    return render_to_response(template_name, {
        'form': form,
        'object': obj
    }, context_instance=RequestContext(request))


delete_object = login_required(delete_object)


def invite(request, **kwargs):
    if request.method == 'POST':
        form = InvitationForm(request.user, request.POST)

        if form.is_valid():
            form.send()
            return HttpResponseRedirect(reverse("invite_done"))
    else:
        form = InvitationForm(request.user)

    context = {
        'form': form,
    }
    return render_to_response(
        'site_specific/invitation.html',
        context,
        context_instance=RequestContext(request)
    )


invite = login_required(invite)


@never_cache
def site_visitors(request):
    User = models.get_model("auth", "User")
    Visit = models.get_model("site_specific", "Visit")

    ip_address = request.META['HTTP_X_FORWARDED_FOR' in request.META and 'HTTP_X_FORWARDED_FOR' or 'REMOTE_ADDR']
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    if request.user.is_authenticated():
        try:
            visit = Visit.objects.get(
                user=request.user,
            )
        except Visit.DoesNotExist:
            Visit.objects.create(
                user=request.user,
                ip_address=ip_address,
                user_agent=user_agent,
                session_key=request.session.session_key,
            )
        else:
            visit.session_key = request.session.session_key
            visit.ip_address = ip_address
            visit.user_agent = user_agent
            visit.last_activity = datetime.now()
            visit.save()
    else:
        try:
            visit = Visit.objects.get(
                session_key=request.session.session_key,
                user__isnull=True,
            )
        except Visit.DoesNotExist:
            if request.session.session_key:
                Visit.objects.create(
                    ip_address=ip_address,
                    user_agent=user_agent,
                    session_key=request.session.session_key,
                )
        else:
            visit.ip_address = ip_address
            visit.user_agent = user_agent
            visit.last_activity = datetime.now()
            visit.save()

    context = {
        'registered_visitors': User.objects.filter(
            visit__last_activity__gt=datetime.now() - timedelta(minutes=2),
        ).distinct(),
        'unregistered_visitors_count': Visit.objects.filter(
            user__isnull=True,
            last_activity__gt=datetime.now() - timedelta(minutes=2),
        ).count()
    }
    return render_to_response(
        'site_specific/blocks/sidebar_visitors.html',
        context,
        context_instance=RequestContext(request)
    )


def claim_action(request, object_id, action):
    Institution = get_installed("institutions.models.Institution")
    Document = get_installed("resources.models.Document")
    Event = get_installed("events.models.Event")
    ClaimRequest = get_installed("site_specific.models.ClaimRequest")
    PersonGroup = get_installed("groups_networks.models.PersonGroup")
    GroupMembership = get_installed("groups_networks.models.GroupMembership")
    Language = get_installed("i18n.models.Language")
    obj = get_object_or_404(ClaimRequest, pk=object_id)
    content_object = obj.content_object
    from base_libs.utils.misc import get_related_queryset

    if action == 'approve':
        obj.status = 1
        if isinstance(content_object, Institution):
            preferred_language = obj.user.profile.preferred_language
            if not preferred_language:
                preferred_language = Language.objects.get(
                    iso2_code=get_current_language(),
                )

            group, created = PersonGroup.objects.get_or_create(
                content_type=obj.content_type,
                object_id=obj.object_id,
                title=content_object.title,
                slug=content_object.slug,
                group_type=get_related_queryset(
                    PersonGroup,
                    "group_type"
                ).get(
                    slug="institutional",
                ),
                access_type="secret",
            )

            group.is_by_confirmation = True
            group.preferred_language = preferred_language
            group.save()

            membership, created = GroupMembership.objects.get_or_create(
                user=obj.user,
                person_group=group,
                role="owners",
                inviter=obj.user,
                confirmer=obj.user,
                is_accepted=True,
            )

        elif isinstance(content_object, Event):
            content_object.organizing_person = obj.user.profile

        elif isinstance(content_object, Document):
            raise Http404, "NOT YET IMPLEMENTED!!!"

    elif action == 'deny':
        obj.status = 2

        '''
        if isinstance(content_object, Institution):

            """
            TODO When denying the claim of an institution,
            currently only the membership of the user is deleted.
            New owner of the group is the modifier (a user with is_staff privileges)
            """
            institution = content_object
            from jetson.apps.groups_networks.models import PersonGroup, GroupMembership
            group = PersonGroup.objects.get(content_type=obj.content_type, object_id=obj.object_id)
            
            # delete membership of user
            membership = GroupMembership.objects.get(user=obj.user, person_group=group)
            membership.delete();
            
            # apply new membership to staff user
            current_user = get_current_user()
            (membership, created) = GroupMembership.objects.get_or_create(
                user = current_user,
                person_group = group,
                role = "owners",
                inviter = current_user,
                confirmer = current_user,
                is_accepted = True,
            )
            
        elif isinstance(content_object, Event):
            content_object.organizing_person = None
            
        elif isinstance(content_object, Document):
            raise Http404, "NOT YET IMPLEMENTED!!!"
        '''
    content_object.save()
    obj.save()

    return HttpResponseRedirect("/admin/site_specific/claimrequest")


claim_action = staff_member_required(never_cache(claim_action))


def delete_profile(request):
    Person = get_installed("people.models.Person")
    Institution = get_installed("institutions.models.Institution")
    Document = get_installed("resources.models.Document")
    Event = get_installed("events.models.Event")
    PersonGroup = get_installed("groups_networks.models.PersonGroup")
    GroupMembership = get_installed("groups_networks.models.GroupMembership")

    context = {}
    if request.method == "POST":
        form = ProfileDeletionForm(request.user, request.POST)
        if form.is_valid():
            # delete chosen profiles
            form.delete()
            # if user deleted, logout
            if form.user_deleted:
                logout(request)
                return HttpResponseRedirect("/my-profile/delete/done/")
            else:
                context['deleted_institutions'] = form.deleted_institutions
                form = ProfileDeletionForm(request.user)
    else:
        form = ProfileDeletionForm(request.user)

    context['form'] = form

    return render_to_response(
        'accounts/my_profile/delete_profile.html',
        context,
        context_instance=RequestContext(request)
    )


delete_profile = login_required(never_cache(delete_profile))


def object_list_for_map(request):
    if not request.is_ajax():
        return access_denied(request)

    try:
        center_lat = float("%.06f" % float(request.GET.get("center_lat", -180)))
        center_lng = float("%.06f" % float(request.GET.get("center_lng", 90)))
        distance = float(request.GET.get("distance", 90))
    except Exception:
        return access_denied(request)

    from ccb.apps.site_specific.models import MappedItem

    object_list = MappedItem.objects.raw(
        'SELECT *, ( 6371 * acos( cos( radians(' + str(
            center_lat) + ') ) * cos( radians( lat ) ) * cos( radians( lng ) - radians(' + str(
            center_lng) + ') ) + sin( radians(' + str(
            center_lat) + ') ) * sin( radians( lat ) ) ) ) AS distance FROM site_specific_mappeditem HAVING distance < ' + str(
            distance) + ' ORDER BY distance;'
    )

    return render_to_response(
        "gmap/ajax_object_list.html",
        {'object_list': object_list},
        context_instance=RequestContext(request),
    )


def my_profile(request):
    return HttpResponseRedirect(request.user.profile.get_url_path())


my_profile = login_required(never_cache(my_profile))


def test_view(request, *args, **kwargs):
    if "test" in request.httpstate:
        del request.httpstate['test']
    else:
        request.httpstate['test'] = "OK"
    raise Warning


@never_cache
def kreativarbeiten_contact_form(request,
                                 template_name='site_specific/kreativarbeiten_contact_form.html',
                                 **kwargs
                                 ):
    """
    Displays the contact form
    """
    if request.method == 'POST':
        data = request.POST.copy()
        form = KreativArbeitenContactForm(data)

        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('%sdone/' % request.path)
    else:
        form = KreativArbeitenContactForm()
    return render_to_response(
        template_name,
        {'form': form, },
        context_instance=RequestContext(request),
    )


def kreativarbeiten_best_practice(request):
    from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED
    from jetson.apps.blog.views import handle_request

    all_dict = {
        'url_identifier': "kreativarbeiten/blog",
        'object_url_part': None,
        'only_for_this_site': True,
        'include': [None],
        'base_template': "site_specific/kreativarbeiten_best_practice_base.html",
        'status': STATUS_CODE_PUBLISHED,
        'tag': "Best-Practice",
    }
    return handle_request(request, **all_dict)


def newsfeed(request, rss, number_of_news):
    from urllib2 import URLError
    from dateutil.parser import parse as datetime_parse
    from xml.dom.minidom import parseString

    from django.utils import dateformat
    import json

    from base_libs.utils.client import Connection

    from jetson.apps.external_services.utils import get_value

    c = Connection(rss)
    try:
        r = c.send_request()
    except URLError:
        return HttpResponse("Connection error")
    data = r.read()

    try:
        xml_doc = parseString(data)
    except Exception:
        return HttpResponse("Parsing error")

    articles = []
    for node_article in xml_doc.getElementsByTagName("item")[:number_of_news]:
        articles.append({
            'title': get_value(node_article, "title"),
            'pubDate': dateformat.format(datetime_parse(get_value(node_article, "pubDate")), 'd.m.Y H:i'),
            'description': get_value(node_article, "description"),
            'link': get_value(node_article, "link"),
        })

    return HttpResponse(json.dumps(articles), content_type="application/json")
