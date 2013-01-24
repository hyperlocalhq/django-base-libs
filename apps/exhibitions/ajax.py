# -*- coding: UTF-8 -*-
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.db import models

Exhibition = models.get_model("exhibitions", "Exhibition")

def get_published_exhibitions(search):
    if not search or len(search) < 1:
        return []
    queryset = Exhibition.objects.filter(status="published")
    if search != "all":
        queryset = queryset.filter(title__istartswith=search)
    return queryset

