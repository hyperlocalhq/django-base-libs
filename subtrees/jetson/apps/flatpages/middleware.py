# -*- coding: UTF-8 -*-
from django.http import Http404
from django.utils.cache import patch_cache_control
from django.utils.cache import patch_vary_headers
from django.conf import settings

from base_libs.middleware import get_current_language


class FlatpageMiddleware(object):
    def process_request(self, request):
        from jetson.apps.flatpages.views import flatpage
        if (
            request.path.startswith(settings.JETSON_MEDIA_URL) or
            request.path.startswith(settings.MEDIA_URL) or
            request.path.startswith(settings.ADMIN_MEDIA_PREFIX) or
            request.path.startswith(settings.UPLOADS_URL)
        ):
            return None

        response = None
        try:
            response = flatpage(request, request.path)
        except Http404:
            pass
        else:
            patch_cache_control(
                response, **{
                    'must_revalidate': True,
                    'max_age': 3600,
                }
            )
            patch_vary_headers(response, [
                'Cookie',
                'Content-Language',
            ])
        return response
