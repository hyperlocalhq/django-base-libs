# -*- coding: UTF-8 -*-
from django.apps import apps

institutions_models = apps.get_app("institutions")

def institutions(request=None):
    d = {
        'URL_ID_INSTITUTION': institutions_models.URL_ID_INSTITUTION,
        'URL_ID_INSTITUTIONS': institutions_models.URL_ID_INSTITUTIONS,
        'DEFAULT_LOGO_4_INSTITUTION': institutions_models.DEFAULT_LOGO_4_INSTITUTION,
        'DEFAULT_FORM_LOGO_4_INSTITUTION': institutions_models.DEFAULT_FORM_LOGO_4_INSTITUTION,
        'DEFAULT_SMALL_LOGO_4_INSTITUTION': institutions_models.DEFAULT_SMALL_LOGO_4_INSTITUTION,
        }
    return d

