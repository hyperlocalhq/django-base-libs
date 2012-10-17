# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta

from django.db import models
from django.http import HttpResponse
from django import forms
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

from base_libs.templatetags.base_tags import decode_entities
from base_libs.forms import dynamicforms
from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.misc import get_related_queryset

from jetson.apps.utils.views import object_list, object_detail

ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")
Exhibition = models.get_model("exhibitions", "Exhibition")

STATUS_CHOICES = (
    ("newly_opened", _("Newly opened")),
    ("closing_soon", _("Closing soon")),
    )

class ExhibitionSearchForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Exhibition, "categories"),
        )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        )

def exhibition_list(request):
    qs = Exhibition.objects.filter(status="published")
    
    form = ExhibitionSearchForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(Exhibition, "categories").order_by("title_%s" % request.LANGUAGE_CODE),
            'statuses': STATUS_CHOICES,
            },
        }

    status = None
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories=cat,
                ).distinct()
        status = form.cleaned_data['status']
        if status:
            facets['selected']['status'] = status
            today = date.today()
            two_weeks = timedelta(days=14)
            if status == "newly_opened":
                # today - 2 weeks < EXHIBITION START <= today
                qs = qs.filter(
                    start__gt=today-two_weeks,
                    start__lte=today,
                    )
            elif status == "closing_soon":
                # today <= EXHIBITION END < today + two weeks
                qs = qs.filter(
                    end__gte=today,
                    end__lt=today+two_weeks,
                    )
    if status == "closing_soon":
        qs = qs.order_by("end", "title_%s" % request.LANGUAGE_CODE)
    else:
        qs = qs.order_by("-start", "title_%s" % request.LANGUAGE_CODE)
        
    extra_context = {}
    extra_context['form'] = form
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="exhibitions/exhibition_list.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="exhibition_list",
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
            'description': decode_entities(ex.description),
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
