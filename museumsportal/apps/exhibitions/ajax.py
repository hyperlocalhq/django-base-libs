# -*- coding: UTF-8 -*-
from django.db import models

from base_libs.middleware import get_current_language

Exhibition = models.get_model("exhibitions", "Exhibition")

def get_published_exhibitions(search):
    language = get_current_language()
    if not search or len(search) < 1:
        return []
    queryset = Exhibition.objects.filter(status="published")
    if search != "all":
        queryset = queryset.filter(**{'title_%s__icontains' % language: search})
    return queryset

