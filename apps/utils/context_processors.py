# -*- coding: UTF-8 -*-
import re

from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models

from filebrowser.settings import MEDIA_URL as UPLOADS_URL

from base_libs.utils.misc import get_website_url
from base_libs.utils.misc import get_website_ssl_url
from base_libs.models.base_libs_settings import JQUERY_URL
from base_libs.models.base_libs_settings import JQUERY_UI_URL

from jetson.apps.httpstate import settings as httpstate_settings

def general(request=None):
    cookie_domain = getattr(httpstate_settings, "HTTPSTATE_COOKIE_DOMAIN", "") or Site.objects.get_current().domain
    if cookie_domain.startswith("."):
        cookie_domain = cookie_domain[1:]
    d = {
        'media_url': settings.MEDIA_URL,
        'jetson_media_url': settings.JETSON_MEDIA_URL,
        'JETSON_MEDIA_URL': settings.JETSON_MEDIA_URL,
        'cookie_domain': cookie_domain,
        'css_url': getattr(settings, "CSS_URL", ""),
        'img_url': getattr(settings, "IMG_URL", ""),
        'https': getattr(settings, "HTTPS_PROTOCOL", "https"),
        'website_url' : get_website_url(),
        'website_ssl_url' : get_website_ssl_url(),
        'UPLOADS_URL': UPLOADS_URL,
        'JQUERY_URL': JQUERY_URL,
        'JQUERY_UI_URL': JQUERY_UI_URL,
        'languages': settings.LANGUAGES,
        }
    settings_to_add = (
        "LOGO_PREVIEW_SIZE",
        )
    for s in settings_to_add:
        d[s] = getattr(settings, s, "")
    return d

def prev_next_processor(request):
    """
    adds some template vars used for prev-next navigation
    """
    object_id = request.httpstate.get('current_object_id', None)
    queryset_model = request.httpstate.get('current_queryset_model', None)
    if isinstance(queryset_model, basestring):
        queryset_model = models.get_model(*queryset_model.split("."))

    queryset_pk_list = request.httpstate.get('current_queryset_pk_list', None)
    queryset_index_dict = request.httpstate.get('current_queryset_index_dict', {})
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
            try: # try in case if the previous item is deleted in the meantime
                prev = queryset_model._default_manager.get(
                    pk=queryset_pk_list[index-1],
                    )
            except:
                pass
        if index < count-1:
            try: # try in case if the next item is deleted in the meantime
                next = queryset_model._default_manager.get(
                    pk=queryset_pk_list[index+1],
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
    
    return {'current_count' : count,
            'current_index' : index + 1,   # we pass the index 1-based to the template
            'prev_item': prev,
            'next_item': next,
            'current_list': current_list,
            'queryset_pk_list': queryset_pk_list,
            }

