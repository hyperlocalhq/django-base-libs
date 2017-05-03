# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import requests

from django.http import HttpResponse


def iframely_wrapper(request):
    headers = {
        'user-agent': request.META['HTTP_USER_AGENT'],
        'referer': "http://127.0.0.1/",
    }
    target_response = requests.get(
        "http://ckeditor.iframe.ly/api/oembed",
        params=request.GET.copy(),
        headers=headers,
    )
    result_response = HttpResponse(
        target_response.text,
        content_type="text/javascript; encoding={}".format(target_response.encoding),
        status=target_response.status_code,
    )
    return result_response