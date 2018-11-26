# -*- coding: UTF-8 -*-
import os
import re
import time
import fnmatch
from os.path import isfile, isdir
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, InvalidPage
from django.db import models
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.utils.timezone import now as tz_now

from filebrowser.settings import MEDIA_ROOT as UPLOADS_ROOT
from filebrowser.settings import MEDIA_URL as UPLOADS_URL

from base_libs.utils.misc import get_website_url
from base_libs.views import access_denied

from jetson.apps.utils.views import direct_to_js_template
from jetson.apps.utils.views import object_detail
from jetson.apps.utils.views import object_list
from jetson.apps.media_gallery.models import MediaGallery, MediaFile, URL_ID_PORTFOLIO, VIDEO_SPLASH_URL, VIDEO_SPLASH_TN_URL, AUDIO_SPLASH_URL, AUDIO_SPLASH_TN_URL
from jetson.apps.media_gallery.forms import ImageFileForm
from jetson.apps.media_gallery.forms import VideoFileForm
from jetson.apps.media_gallery.forms import AudioFileForm

image_mods = models.get_app("image_mods")

MEDIA_FILE_FORM_MAP = {
    'image': ImageFileForm,
    'audio': AudioFileForm,
    'video': VideoFileForm,
}


def _get_list_of_files(gallery=None):
    filters = {
        'gallery': gallery,
    }
    return MediaFile.objects.filter(**filters)


@never_cache
def gallery_detail(request, **kwargs):
    obj = request.current_page

    try:
        gallery = MediaGallery.objects.get(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )
    except:
        gallery = None

    list_of_files = _get_list_of_files(gallery)

    if gallery:
        gallery.increase_views()

    if not "extra_context" in kwargs:
        kwargs["extra_context"] = {}
    kwargs["extra_context"]["list_of_files"] = list_of_files
    kwargs["extra_context"]["gallery"] = gallery
    kwargs["extra_context"]["object"] = obj

    return render_to_response(
        'media_gallery/page_portfolio.html',
        kwargs["extra_context"],
        context_instance=RequestContext(request)
    )


@never_cache
def create_update_mediafile(request, token="", media_file_type="", **kwargs):

    media_file_type = media_file_type or "image"
    if media_file_type not in ("image", "video", "audio"):
        raise Http404

    if not "extra_context" in kwargs:
        kwargs["extra_context"] = {}

    obj = request.current_page
    if not request.user.has_perm(
        "%s.change_%s" %
        (type(obj)._meta.app_label, type(obj).__name__.lower()), obj
    ):
        return access_denied(request)

    rel_dir = getattr(obj, "get_filebrowser_dir", lambda: "")()
    rel_dir += URL_ID_PORTFOLIO + "/"

    try:
        gallery = MediaGallery.objects.get(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )
    except:
        gallery = None

    filters = {
        'id': token,
    }
    if gallery:
        filters['gallery'] = gallery
    try:
        media_file_obj = MediaFile.objects.get(**filters)
    except:
        media_file_obj = None

    if media_file_obj:
        if media_file_obj.file_type == "i":
            media_file_type = "image"
        elif media_file_obj.file_type == "a":
            media_file_type = "audio"
        elif media_file_obj.file_type in ("v", "y"):
            media_file_type = "video"

    form_class = MEDIA_FILE_FORM_MAP[media_file_type]

    if request.method == "POST":
        # just after submitting data
        form = form_class(request.POST, request.FILES)
        # Passing request.FILES to the form always breaks the form validation
        # WHY!?? As a workaround, let's validate just the POST and then
        # manage FILES separately.
        if not media_file_obj and (
            "media_file" not in request.FILES
        ) and not request.POST.get("external_url", ""):
            # new media file - media file required
            form.fields['media_file'].required = True
            form.fields['external_url'].required = True
        if form.is_valid():
            cleaned = form.cleaned_data
            file_obj = None
            splash_image_obj = None
            path = ""
            if media_file_obj and media_file_obj.path:
                path = media_file_obj.path.path
            if cleaned.get("media_file", None) or cleaned.get("external_url"):
                if path:
                    # delete the old file
                    try:
                        image_mods.FileManager.delete_file(path)
                    except OSError:
                        pass
                    path = ""

            media_file_path = ""
            if cleaned.get("media_file", None):
                fname, fext = os.path.splitext(cleaned['media_file'].name)
                filename = tz_now().strftime("%Y%m%d%H%M%S") + fext
                path = "".join((rel_dir, filename))
                image_mods.FileManager.save_file(
                    path=path,
                    content=cleaned['media_file'],
                )
                media_file_path = path

            splash_image_file_path = ""
            if cleaned.get("splash_image_file", None):
                if media_file_obj and media_file_obj.splash_image_path:
                    # delete the old file
                    try:
                        image_mods.FileManager.delete_file(
                            media_file_obj.splash_image_path.path
                        )
                    except OSError:
                        pass
                time.sleep(1)  # ensure that the filenames differ
                filename = tz_now().strftime("%Y%m%d%H%M%S.jpg")
                path = "".join((rel_dir, filename))
                image_mods.FileManager.save_file(
                    path=path,
                    content=cleaned['splash_image_file'],
                )
                splash_image_file_path = path

            if not media_file_obj:
                if not gallery:
                    gallery = MediaGallery.objects.create_for_object(obj)

                media_file_obj = MediaFile(gallery=gallery)
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(
                    media_file_obj, 'title_%s' % lang_code,
                    cleaned['title_%s' % lang_code]
                )
                setattr(
                    media_file_obj, 'description_%s' % lang_code,
                    cleaned['description_%s' % lang_code]
                )
            media_file_obj.external_url = cleaned['external_url']
            if media_file_path:  # update media_file path
                media_file_obj.path = media_file_path
            if splash_image_file_path:  # update media_file splash image path
                media_file_obj.splash_image_path = splash_image_file_path
            media_file_obj.save()

            if "save_continue" in request.POST:
                redirect_to = "%sfile_%s/" % (
                    obj.get_absolute_url(),
                    media_file_obj.id,
                )
            elif "save_add" in request.POST:
                redirect_to = "%sadd/%s/" % (
                    obj.get_absolute_url(),
                    media_file_type,
                )
            else:
                redirect_to = "%s#file_%s" % (
                    obj.get_absolute_url(),
                    media_file_obj.id,
                )
            return HttpResponseRedirect(redirect_to)
    else:
        if media_file_obj:
            # existing media file
            form = form_class(initial=media_file_obj.__dict__)
        else:
            # new media file
            form = form_class()
            form.fields['media_file'].required = True

    list_of_files = _get_list_of_files(gallery)
    kwargs['extra_context'] = {
        'media_file':
            media_file_obj or MediaFile(file_type=media_file_type[0]),
        'list_of_files':
            list_of_files,
        'media_file_type':
            media_file_type,
        'form':
            form,
    }
    kwargs["extra_context"]["object"] = obj
    return render_to_response(
        'media_gallery/page_portfolio_change.html',
        kwargs["extra_context"],
        context_instance=RequestContext(request)
    )


def delete_mediafile(request, token="", **kwargs):
    obj = request.current_page
    if not request.user.has_perm(
        "%s.change_%s" %
        (type(obj)._meta.app_label, type(obj).__name__.lower()), obj
    ):
        return access_denied(request)

    gallery = MediaGallery.objects.get(
        object_id=obj.id,
        content_type=ContentType.objects.get_for_model(obj),
    )

    filters = {
        'id': token,
    }
    if gallery:
        filters['gallery'] = gallery
    try:
        media_file_obj = MediaFile.objects.get(**filters)
    except:
        raise Http404

    if "POST" == request.method:
        if media_file_obj:
            if media_file_obj.path:
                try:
                    image_mods.FileManager.delete_file(media_file_obj.path.path)
                except OSError:
                    pass
            if media_file_obj.splash_image_path:
                try:
                    image_mods.FileManager.delete_file(
                        media_file_obj.splash_image_path.path
                    )
                except OSError:
                    pass
            media_file_obj.delete()

        redirect_to = obj.get_absolute_url()
        return HttpResponseRedirect(redirect_to)
    if not "extra_context" in kwargs:
        kwargs["extra_context"] = {}
    kwargs["extra_context"]["media_file"] = media_file_obj
    kwargs["extra_context"]["object"] = obj

    return render_to_response(
        'media_gallery/page_portfolio_delete.html',
        kwargs["extra_context"],
        context_instance=RequestContext(request)
    )


def delete_mediafile_popup(request, token="", **kwargs):
    response = delete_mediafile(request, token, **kwargs)
    if isinstance(response, HttpResponseRedirect):
        response = HttpResponse("reload")
    return response


def gallery_list(
    request,
    queryset,
    show="",
    paginate_by=None,
    order_by=None,
    page=None,
    allow_empty=False,
    template_name=None,
    template_loader=loader,
    extra_context=None,
    context_processors=None,
    template_object_name='object',
    content_type=None,
    pages_to_display=10,
    query=""
):
    queryset = queryset.distinct().extra(
        where=(
            "(SELECT COUNT(*) FROM media_gallery_mediafile WHERE media_gallery_id=media_gallery_mediagallery.id) > 0",
        ),
    )
    """
    Generic list of objects.

    Templates: ``<app_label>/<model_name>_list.html``
    Context:
        object_list
            list of objects
        is_paginated
            are the results paginated?
        results_per_page
            number of objects per page (if paginated)
        has_next
            is there a next page?
        has_previous
            is there a prev page?
        page
            the current page
        next
            the next page
        previous
            the previous page
        pages
            number of pages, total
        pagelist
            list of page numbers to display
        hits
            number of objects, total
    """

    if extra_context is None:
        extra_context = {}

    sort_order_map = getattr(queryset, "get_sort_order_map", lambda: None)()
    sort_order_mapper = getattr(
        queryset, "get_sort_order_mapper", lambda: None
    )()

    if show == "featured":
        queryset = queryset.filter(is_featured=True)
    elif show == "favorites":
        if request.user.is_anonymous():
            return access_denied(request)
        queryset = queryset.extra(
            tables=["favorites_favorite"],
            where=[
                "favorites_favorite.user_id = %d" % request.user.id,
                "favorites_favorite.object_id::integer = media_gallery_mediagallery.id",
                "favorites_favorite.content_type_id = %d" %
                ContentType.objects.get_for_model(MediaGallery).pk,
            ],
        ).distinct()

    queryset = queryset._clone()
    queryset.sort_order_map = sort_order_map
    queryset.sort_order_mapper = sort_order_mapper

    filter_field = request.REQUEST.get("filter_field", None)
    filter_value = request.REQUEST.get("filter_value", None)
    group_by = request.REQUEST.get("group_by", None)

    paginate_by = request.REQUEST.get(
        "paginate_by",
        request.httpstate.get("paginate_galleries_by", paginate_by or 30)
    )
    paginate_by = int(paginate_by)
    order_by = request.REQUEST.get(
        "order_by", request.httpstate.get("order_by", order_by)
    )

    url_query = []
    if filter_field:
        url_query.append("filter_field=" + filter_field)
    if filter_value:
        url_query.append("filter_value=" + filter_value)
    if order_by:
        url_query.append("order_by=" + order_by)
    if group_by:
        url_query.append("group_by=" + group_by)

    if filter_field and filter_value:
        queryset = queryset.filter(**{filter_field: filter_value})

    try:
        queryset = queryset.sort_by(order_by)
    except:
        pass

    request.httpstate["paginate_galleries_by"] = paginate_by
    request.httpstate["order_by"] = order_by
    """
    precalculate context processors
      
    we save the queryset in the httpstate, as we need that for the prev - next
    navigation in the details views. queryset_index_dict is build up once 
    for each queryset. It has an unique string containing contenttype_id and
    object_id as a key and the index of the dataset as value. The
    previous-next-processor just looks for occurrence of the appropriate key and
    gets the value from the dict. This solution seems to be much faster than
    searching the whole queryset every time!!!!
    
    IMPORTANT!!
    for any reason, we get a "PicklingError" here, when assigning 
    the queryset directly to the httpstate. So we take a list (current_queryset_list)
    """
    if context_processors and extra_context:
        queryset_index_dict = {}
        index = 0

        prev_next_use_content_object = extra_context.get(
            'prev_next_use_content_object', False
        )

        for obj in queryset.iterator():
            if prev_next_use_content_object:
                key = '%s_%s' % (obj.content_type_id, obj.object_id)
            else:
                key = '%s_%s' % (
                    ContentType.objects.get_for_model(queryset.model).id,
                    obj._get_pk_val(),
                )
            queryset_index_dict[key] = index
            index += 1

        if extra_context.get('source_list', None):
            request.httpstate['source_list'] = extra_context['source_list']

        request.httpstate['current_queryset_index_dict'] = queryset_index_dict
        request.httpstate['last_query_string'] = request.META['QUERY_STRING']

    request.httpstate['current_queryset_pk_list'] = [
        item.pk for item in queryset
    ]
    request.httpstate['current_queryset_model'] = queryset.model

    if paginate_by:
        paginator = Paginator(queryset, paginate_by)
        if not page:
            page = request.GET.get('page', 1)
        try:
            page = int(page)
            current_page = paginator.page(page)
            object_list = current_page.object_list
        except (InvalidPage, ValueError):
            raise Http404

        page_min = max(page - pages_to_display / 2, 1)
        page_max = min(paginator.num_pages + 1, page_min + pages_to_display)
        if page_max == paginator.num_pages + 1:
            page_min = max(page_max - pages_to_display, 1)

        c = RequestContext(
            request, {
                '%s_list' % template_object_name: object_list,
                'is_paginated': current_page.has_other_pages(),
                'results_per_page': paginate_by,
                'has_next': current_page.has_next(),
                'has_previous': current_page.has_previous(),
                'page': page,
                'next': current_page.next_page_number(),
                'previous': current_page.previous_page_number(),
                'pages': paginator.num_pages,
                'pagelist': [i for i in range(page_min, page_max)],
                'page_numbers': paginator.page_range,
                'hits': queryset.count(),
                'page_hits_min': (page - 1) * paginate_by + 1,
                'page_hits_max': min(page * paginate_by, queryset.count()),
            }, context_processors
        )
    else:
        c = RequestContext(
            request, {
                '%s_list' % template_object_name: queryset,
                'is_paginated': False
            }, context_processors
        )
        if not allow_empty and len(queryset) == 0:
            raise Http404
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    c['filter_field'] = filter_field
    c['filter_value'] = filter_value
    c['group_by'] = group_by
    c['order_by'] = order_by
    c['url_query'] = '&amp;'.join(url_query)
    c['sort_order_map'] = sort_order_map

    the_query = request.GET.copy()
    c['query'] = query or the_query.urlencode()

    c['path_without_page'] = re.sub('/page[0-9]+', '', request.path)

    if not template_name:
        model = queryset.model
        template_name = "%s/%s_list.html" % (
            model._meta.app_label, model._meta.object_name.lower()
        )
    t = template_loader.get_template(template_name)
    return HttpResponse(t.render(c), content_type=content_type)


def json_show_file(request, token="", **kwargs):
    obj = request.current_page

    try:
        gallery = MediaGallery.objects.get(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )
    except:
        gallery = None

    filters = {
        'id': token,
    }
    if gallery:
        filters['gallery'] = gallery
    try:
        media_file_obj = MediaFile.objects.get(**filters)
    except:
        media_file_obj = None

    kwargs['extra_context'] = {
        'media_file': media_file_obj,
    }
    kwargs['template'] = "media_gallery/includes/media_file.js"
    return direct_to_js_template(request, cache=False, **kwargs)


### COMMENTS ###


@never_cache
def gallery_post_comment(
    request,
    rel_url_part,
    rel_obj_content_type_var=None,
    template_dir=None,
    template_name=None,
    template_loader=loader,
    extra_context=None,
    use_ajax=False,
    slug_field="slug",
    **kwargs
):
    """
    handles posting a comment
    """

    object_model = models.get_model(*rel_obj_content_type_var.split("."))
    obj = object_model.objects.get(**{slug_field: kwargs["slug"]})

    try:
        gallery = MediaGallery.objects.get(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )
    except:
        gallery = None

    if extra_context is None:
        extra_context = {}
    if obj:
        extra_context['object'] = obj

    extra_context[settings.REDIRECT_FIELD_NAME
                 ] = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    extra_context['rel_obj_root_dir'] = get_website_url() + rel_url_part
    extra_context['template_dir'] = template_dir
    extra_context['gallery'] = gallery
    extra_context['object'] = obj

    if template_name is None:
        if template_dir is not None:
            template_name = '%scomments/form.html' % template_dir
        else:
            template_name = 'media_gallery/comments/form.html'

    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')

    if request.method == 'POST':
        from jetson.apps.comments.views.comments import post_comment
        if request.POST.has_key('post'):

            post_comment(
                request, template_name=template_name, use_ajax=use_ajax
            )
            if not use_ajax:
                redirect_to += "#comments"
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponse("reload")

        # the normal preview is done ...
        elif request.POST.has_key('preview'):
            return post_comment(
                request,
                template_name=template_name,
                use_ajax=use_ajax,
                extra_context=extra_context
            )

        #cancel
        else:
            if not use_ajax:
                redirect_to += "#comments"
                return HttpResponseRedirect(redirect_to)

    from django.template import Template
    extra_context['template_dir'] = template_dir
    extra_context['gallery'] = gallery
    t = Template(
        """
        {% load comments %}
        {% comment_form using "media_gallery/comments/form.html" for media_gallery.mediagallery gallery.id %}
        """
    )
    c = RequestContext(request, extra_context)
    return HttpResponse(t.render(c))


def gallery_refuse_comment(
    request,
    rel_url_part,
    comment_id,
    rel_obj_content_type_var=None,
    template_dir=None,
    template_name=None,
    template_loader=loader,
    extra_context=None,
    use_popup=False,
    slug_field="slug",
    **kwargs
):
    """
    Displays the delete comment form and handles the associated action
    """
    object_model = models.get_model(*rel_obj_content_type_var.split("."))
    obj = object_model.objects.get(**{slug_field: kwargs["slug"]})

    try:
        gallery = MediaGallery.objects.get(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )
    except:
        gallery = None

    # check permissions
    if not request.user.has_perm(
        "%s.change_%s" % (obj._meta.app_label, obj.__class__.__name__.lower()),
        obj
    ):
        return access_denied(request)

    if extra_context is None:
        extra_context = {}
    if obj:
        extra_context['object'] = obj

    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if redirect_to == '':
        redirect_to = request.path.split('comment')[0]

    extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
    extra_context['rel_obj_root_dir'] = get_website_url() + rel_url_part
    extra_context['template_dir'] = template_dir
    extra_context['gallery'] = gallery
    extra_context['object'] = obj

    if template_name is None:
        if template_dir is not None:
            template_name = '%scomments/refuse.html' % template_dir
        else:
            template_name = 'media_gallery/comments/refuse.html'

    from jetson.apps.comments.views.comments import refuse_comment
    return refuse_comment(
        request, comment_id, template_name, redirect_to, extra_context,
        use_popup
    )


def gallery_accept_comment(
    request,
    rel_url_part,
    comment_id,
    rel_obj_content_type_var=None,
    template_dir=None,
    template_name=None,
    template_loader=loader,
    extra_context=None,
    use_popup=False,
    slug_field="slug",
    **kwargs
):
    """
    Displays the accept comment form and handles the associated action
    """
    object_model = models.get_model(*rel_obj_content_type_var.split("."))
    obj = object_model.objects.get(**{slug_field: kwargs["slug"]})

    try:
        gallery = MediaGallery.objects.get(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )
    except:
        gallery = None

    # check permissions
    if not request.user.has_perm(
        "%s.change_%s" % (obj._meta.app_label, obj.__class__.__name__.lower()),
        obj
    ):
        return access_denied(request)

    if extra_context is None:
        extra_context = {}
    if obj:
        extra_context['object'] = obj

    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if redirect_to == '':
        redirect_to = request.path.split('comment')[0]

    extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
    extra_context['rel_obj_root_dir'] = get_website_url() + rel_url_part
    extra_context['template_dir'] = template_dir
    extra_context['gallery'] = gallery
    extra_context['object'] = obj

    if template_name is None:
        if template_dir is not None:
            template_name = '%scomments/accept.html' % template_dir
        else:
            template_name = 'media_gallery/comments/accept.html'

    from jetson.apps.comments.views.comments import accept_comment
    return accept_comment(
        request, comment_id, template_name, redirect_to, extra_context,
        use_popup
    )


def gallery_mark_comment_as_spam(
    request,
    rel_url_part,
    comment_id,
    rel_obj_content_type_var=None,
    template_dir=None,
    template_name=None,
    template_loader=loader,
    extra_context=None,
    use_popup=False,
    slug_field="slug",
    **kwargs
):
    """
    Displays the "mark as spam" comment form and handles the associated action
    """
    object_model = models.get_model(*rel_obj_content_type_var.split("."))
    obj = object_model.objects.get(**{slug_field: kwargs["slug"]})

    try:
        gallery = MediaGallery.objects.get(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        )
    except:
        gallery = None

    # check permissions
    if not request.user.has_perm(
        "%s.change_%s" % (obj._meta.app_label, obj.__class__.__name__.lower()),
        obj
    ):
        return access_denied(request)

    if extra_context is None:
        extra_context = {}
    if obj:
        extra_context['object'] = obj

    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if redirect_to == '':
        redirect_to = request.path.split('comment')[0]

    extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
    extra_context['rel_obj_root_dir'] = get_website_url() + rel_url_part
    extra_context['template_dir'] = template_dir
    extra_context['gallery'] = gallery
    extra_context['object'] = obj

    if template_name is None:
        if template_dir is not None:
            template_name = '%scomments/markasspam.html' % template_dir
        else:
            template_name = 'media_gallery/comments/markasspam.html'

    from jetson.apps.comments.views.comments import mark_as_spam_comment
    return mark_as_spam_comment(
        request, comment_id, template_name, redirect_to, extra_context,
        use_popup
    )
