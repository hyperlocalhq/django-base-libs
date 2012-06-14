# -*- coding: utf-8 -*-

from django.db import models
from django import forms

from jetson.apps.utils.views import object_list, object_detail

from base_libs.forms import dynamicforms
from base_libs.utils.misc import get_related_queryset

MuseumCategory = models.get_model("museums", "MuseumCategory")
Museum = models.get_model("museums", "Museum")

class MuseumSearchForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Museum, "categories"),
        )

def museum_list(request):
    qs = Museum.objects.filter(status="published")
    
    form = MuseumSearchForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': MuseumCategory.objects.all(),
            },
        }
    
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs  = qs .filter(
                categories=cat,
                ).distinct()
    
    extra_context = {}
    extra_context['form'] = form
    extra_context['facets'] = facets
    
    return object_list(
        request,
        queryset=qs,
        template_name="museums/museum_list.html",
        paginate_by=200,
        extra_context=extra_context,
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
