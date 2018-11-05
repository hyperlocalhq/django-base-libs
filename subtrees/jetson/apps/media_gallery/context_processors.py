# -*- coding: UTF-8 -*-
from django.conf import settings
from django.apps import apps

URL_ID_PORTFOLIO = apps.get_app("media_gallery").URL_ID_PORTFOLIO

def media_gallery(request=None):
    d = {
        'URL_ID_PORTFOLIO': URL_ID_PORTFOLIO,
        }
    return d

