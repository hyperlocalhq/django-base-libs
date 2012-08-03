# -*- coding: utf-8 -*-
from django.db import models
from django.utils import simplejson
from django.http import HttpResponse

from datetime import datetime

from base_libs.utils.misc import ExtendedJSONEncoder

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

def export_json_exhibitions(request):
    #create queryset
    qs = Exhibition.objects.filter(status="published")
    
    exhibitions = []
    for ex in qs:
        data ={
            'museum': ex.museum,
            'title': ex.title,
            'subtitle': ex.subtitle,
            'description': ex.description,
            'website': ex.website,
            'start': ex.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': ex.end.strftime('%Y-%m-%dT%H:%M:%S'),
            'newly_opened': ex.newly_opened,
            'featured': ex.featured,
            'image_caption': ex.image_caption,
        }
        exhibitions.append(data)
    json = simplejson.dumps(
        exhibitions,
        #datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        ensure_ascii=False,
        cls=ExtendedJSONEncoder
        )
    return HttpResponse(json, mimetype='text/javascript; charset=utf-8')
