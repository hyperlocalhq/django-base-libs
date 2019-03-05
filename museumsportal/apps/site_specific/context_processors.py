# -*- coding: UTF-8 -*-
from django.conf import settings


def languages(request=None):
    import json

    from django.utils.safestring import mark_safe

    OPEN_GRAPH_LOCALE_MAPPER = getattr(settings, "OPEN_GRAPH_LOCALE_MAPPER", {"en": "en_US"})

    return {
        'FRONTEND_LANGUAGES':
            settings.FRONTEND_LANGUAGES,
        'FRONTEND_LANGUAGES_JSON':
            mark_safe(json.dumps(dict(settings.FRONTEND_LANGUAGES))),
        'OPEN_GRAPH_LOCALE':
            OPEN_GRAPH_LOCALE_MAPPER.get(request.LANGUAGE_CODE, "en_US")
    }
