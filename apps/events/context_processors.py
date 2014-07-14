# -*- coding: UTF-8 -*-
from django.conf import settings

from ccb.apps.events.models import URL_ID_EVENT, URL_ID_EVENTS, DEFAULT_LOGO_4_EVENT, DEFAULT_FORM_LOGO_4_EVENT, DEFAULT_SMALL_LOGO_4_EVENT

def events(request=None):
    d = {
        'URL_ID_EVENT': URL_ID_EVENT,
        'URL_ID_EVENTS': URL_ID_EVENTS,
        'DEFAULT_LOGO_4_EVENT': DEFAULT_LOGO_4_EVENT,
        'DEFAULT_FORM_LOGO_4_EVENT': DEFAULT_FORM_LOGO_4_EVENT,
        'DEFAULT_SMALL_LOGO_4_EVENT': DEFAULT_SMALL_LOGO_4_EVENT,
        }
    return d

