# -*- coding: UTF-8 -*-
from django.conf import settings


def languages(request=None):
    OPEN_GRAPH_LOCALE_MAPPER = getattr(
        settings, "OPEN_GRAPH_LOCALE_MAPPER", {"en": "en_US"}
    )

    return {
        'FRONTEND_LANGUAGES':
            settings.FRONTEND_LANGUAGES,
        'OPEN_GRAPH_LOCALE':
            OPEN_GRAPH_LOCALE_MAPPER.get(request.LANGUAGE_CODE, "en_US")
    }


def environment(request=None):
    return {
        'ENVIRONMENT': getattr(settings, 'ENVIRONMENT'),
    }
