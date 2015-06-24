# -*- coding: UTF-8 -*-
from django.conf import settings

from jetson.apps.marketplace.models import URL_ID_JOB_OFFER, URL_ID_JOB_OFFERS

def marketplace(request=None):
    d = {
        'URL_ID_JOB_OFFER': URL_ID_JOB_OFFER,
        'URL_ID_JOB_OFFERS': URL_ID_JOB_OFFERS,
        }
    return d

