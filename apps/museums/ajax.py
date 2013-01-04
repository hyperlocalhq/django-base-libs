# -*- coding: UTF-8 -*-
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.db import models

Museum = models.get_model("museums", "Museum")

def get_published_museums(search):
    if not search or len(search) < 1:
        return []
    queryset = Museum.objects.filter(status="published")
    if search != "all":
        queryset = queryset.filter(title__istartswith=search)
    return queryset

