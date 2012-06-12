# -*- coding: utf-8 -*-

from django.db import models

from jetson.apps.utils.views import object_list, object_detail

Museum = models.get_model("museums", "Museum")

def museum_list(request):
    qs = Museum.objects.filter(status="published")
    return object_list(
        request,
        queryset=qs,
        template_name="museums/museum_list.html",
        )

def museum_detail(request, slug):
    qs = Museum.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="museums/museum_detail.html",
        )
