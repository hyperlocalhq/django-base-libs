# -*- coding: UTF-8 -*-
from django.apps import apps

events_models = apps.get_app("events")


def events(request=None):
    d = {
        'URL_ID_EVENT': events_models.URL_ID_EVENT,
        'URL_ID_EVENTS': events_models.URL_ID_EVENTS,
        'DEFAULT_LOGO_4_EVENT': events_models.DEFAULT_LOGO_4_EVENT,
        'DEFAULT_FORM_LOGO_4_EVENT': events_models.DEFAULT_FORM_LOGO_4_EVENT,
        'DEFAULT_SMALL_LOGO_4_EVENT': events_models.DEFAULT_SMALL_LOGO_4_EVENT,
    }
    return d
