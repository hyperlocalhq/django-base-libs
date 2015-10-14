# -*- coding: UTF-8 -*-
from django.apps import apps

marketplace_models = apps.get_app("marketplace")

def marketplace(request=None):
    d = {
        'URL_ID_JOB_OFFER': marketplace_models.URL_ID_JOB_OFFER,
        'URL_ID_JOB_OFFERS': marketplace_models.URL_ID_JOB_OFFERS,
        }
    return d

