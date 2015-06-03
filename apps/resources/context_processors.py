# -*- coding: UTF-8 -*-
from django.conf import settings

from jetson.apps.resources.models import URL_ID_DOCUMENT, URL_ID_DOCUMENTS, DEFAULT_LOGO_4_DOCUMENT, DEFAULT_FORM_LOGO_4_DOCUMENT, DEFAULT_SMALL_LOGO_4_DOCUMENT

def resources(request=None):
    d = {
        'URL_ID_DOCUMENT': URL_ID_DOCUMENT,
        'URL_ID_DOCUMENTS': URL_ID_DOCUMENTS,
        'DEFAULT_LOGO_4_DOCUMENT': DEFAULT_LOGO_4_DOCUMENT,
        'DEFAULT_FORM_LOGO_4_DOCUMENT': DEFAULT_FORM_LOGO_4_DOCUMENT,
        'DEFAULT_SMALL_LOGO_4_DOCUMENT': DEFAULT_SMALL_LOGO_4_DOCUMENT,
        }
    return d

