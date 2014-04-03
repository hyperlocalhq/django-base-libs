# -*- coding: UTF-8 -*-
from museumsportal.apps.media_gallery.models import URL_ID_PORTFOLIO

def media_gallery(request=None):
    d = {
        'URL_ID_PORTFOLIO': URL_ID_PORTFOLIO,
        }
    return d

