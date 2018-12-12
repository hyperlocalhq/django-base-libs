# -*- coding: UTF-8 -*-
from django.conf import settings


def languages(request=None):
    return {
        'FRONTEND_LANGUAGES': settings.FRONTEND_LANGUAGES,
    }
