# -*- coding: UTF-8 -*-
from django.apps import apps

resources_models = apps.get_app("resources")

def resources(request=None):
    d = {
        'URL_ID_DOCUMENT': resources_models.URL_ID_DOCUMENT,
        'URL_ID_DOCUMENTS': resources_models.URL_ID_DOCUMENTS,
        'DEFAULT_LOGO_4_DOCUMENT': resources_models.DEFAULT_LOGO_4_DOCUMENT,
        'DEFAULT_FORM_LOGO_4_DOCUMENT': resources_models.DEFAULT_FORM_LOGO_4_DOCUMENT,
        'DEFAULT_SMALL_LOGO_4_DOCUMENT': resources_models.DEFAULT_SMALL_LOGO_4_DOCUMENT,
        }
    return d

