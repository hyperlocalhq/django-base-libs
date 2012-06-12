# -*- coding: utf-8 -*-

from django.db import models

from jetson.apps.utils.views import object_list, object_detail

Exhibition = models.get_model("exhibitions", "Exhibition")

def exhibition_list(request):
    qs = Exhibition.objects.filter(status="published")
    return object_list(
        request,
        queryset=qs,
        template_name="exhibitions/exhibition_list.html",
        )

def exhibition_detail(request, slug):
    qs = Exhibition.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="exhibitions/exhibition_detail.html",
        )
