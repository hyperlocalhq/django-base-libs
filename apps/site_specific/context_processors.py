# -*- coding: UTF-8 -*-
from django.conf import settings


def site_specific(request=None):
    OPEN_GRAPH_LOCALE_MAPPER = getattr(settings, "OPEN_GRAPH_LOCALE_MAPPER", {"en": "en_US"})

    return {
        'OPEN_GRAPH_LOCALE': OPEN_GRAPH_LOCALE_MAPPER.get(request.LANGUAGE_CODE, "en_US")
    }
