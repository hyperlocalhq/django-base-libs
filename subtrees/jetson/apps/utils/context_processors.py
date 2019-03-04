# -*- coding: UTF-8 -*-
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.safestring import mark_safe
from django.apps import apps
from django.utils.six import string_types

from filebrowser.settings import MEDIA_URL as UPLOADS_URL

from base_libs.utils.misc import get_website_url

from jetson.apps.httpstate import settings as httpstate_settings


def general(request=None):
    import json

    cookie_domain = getattr(
        httpstate_settings,
        "HTTPSTATE_COOKIE_DOMAIN",
        "",
    ) or Site.objects.get_current().domain

    if cookie_domain.startswith("."):
        cookie_domain = cookie_domain[1:]

    d = {
        # SOLID
        'UPLOADS_URL': UPLOADS_URL,
        'JETSON_MEDIA_URL': settings.JETSON_MEDIA_URL,
        'GOOGLE_API_KEY': getattr(settings, "GOOGLE_API_KEY", ""),

        # NEW
        'MEDIA_URL': settings.MEDIA_URL,
        'MEDIA_HOST': getattr(settings, "MEDIA_HOST", ""),
        'COOKIE_DOMAIN': cookie_domain,
        'HTTPS': getattr(settings, "HTTPS_PROTOCOL", "https"),
        'WEBSITE_URL': get_website_url(),
        'LANGUAGES': settings.LANGUAGES,
        'LANGUAGES_JSON': mark_safe(json.dumps(dict(settings.LANGUAGES))),

        # DEPRECATED
        'LOGO_PREVIEW_SIZE': getattr(settings, "LOGO_PREVIEW_SIZE", None),
        # TODO: the LOGO_PREVIEW_SIZE setting requires more thorough refactoring of CCB-related jetson code
        'media_url': settings.MEDIA_URL,
        'media_host': getattr(settings, "MEDIA_HOST", ""),
        'jetson_media_url': settings.JETSON_MEDIA_URL,
        'cookie_domain': cookie_domain,
        'css_url': getattr(settings, "CSS_URL", ""),
        'img_url': getattr(settings, "IMG_URL", ""),
        'https': getattr(settings, "HTTPS_PROTOCOL", "https"),
        'website_url': get_website_url(),
        'languages': mark_safe(json.dumps(dict(settings.LANGUAGES))),
    }
    return d


def prev_next_processor(request):
    """
    adds some template vars used for prev-next navigation
    """
    object_id = request.httpstate.get('current_object_id', None)
    queryset_model = request.httpstate.get('current_queryset_model', None)
    if isinstance(queryset_model, string_types):
        queryset_model = apps.get_model(*queryset_model.split("."))

    queryset_pk_list = request.httpstate.get('current_queryset_pk_list', None)
    queryset_index_dict = request.httpstate.get(
        'current_queryset_index_dict', {}
    )
    source_list = request.httpstate.get('source_list', "")
    paginate_by = request.httpstate.get('paginate_by', None)
    last_query_string = request.httpstate.get('last_query_string', None)

    count = 0
    prev = None
    next = None
    current_list = None
    index = -1

    if queryset_model and queryset_pk_list and object_id in queryset_pk_list:
        count = len(queryset_pk_list)
        ct = ContentType.objects.get_for_model(queryset_model)
        index = queryset_index_dict.get('%s_%s' % (ct.id, object_id), 0)

        if index > 0:
            try:  # try in case if the previous item is deleted in the meantime
                prev = queryset_model._default_manager.get(
                    pk=queryset_pk_list[index - 1],
                )
            except:
                pass
        if index < count - 1:
            try:  # try in case if the next item is deleted in the meantime
                next = queryset_model._default_manager.get(
                    pk=queryset_pk_list[index + 1],
                )
            except:
                pass

        # now make the link to the list...
        current_list = source_list
        if not current_list.endswith("/"):
            current_list += "/"
        if paginate_by:
            page = index / paginate_by + 1
            if last_query_string:
                current_list += "?%s&page=%d" % (last_query_string, page)
            else:
                current_list += "?page=%d" % page

    return {
        'current_count': count,
        'current_index': index + 1,  # we pass the index 1-based to the template
        'prev_item': prev,
        'next_item': next,
        'current_list': current_list,
        'queryset_pk_list': queryset_pk_list,
    }
