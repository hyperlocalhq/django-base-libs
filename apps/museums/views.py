# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc

from base_libs.forms import dynamicforms
from base_libs.utils.misc import get_related_queryset

MuseumCategory = models.get_model("museums", "MuseumCategory")
Museum = models.get_model("museums", "Museum")

class MuseumSearchForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Museum, "categories"),
        )
    open_on_mondays = forms.BooleanField(
        required=False,
        )
    free_entrance = forms.BooleanField(
        required=False,
        )

def museum_list(request):
    qs = Museum.objects.filter(status="published")

    form = MuseumSearchForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': MuseumCategory.objects.all(),
            'open_on_mondays': _("Open on Mondays"),
            'free_entrance': _("Free entrance"),
            },
        }
    
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs  = qs .filter(
                categories=cat,
                ).distinct()
        open_on_mondays = form.cleaned_data['open_on_mondays']
        if open_on_mondays:
            facets['selected']['open_on_mondays'] = True
            qs  = qs .filter(
                open_on_mondays=True,
                )
        free_entrance = form.cleaned_data['free_entrance']
        if free_entrance:
            facets['selected']['free_entrance'] = True
            qs  = qs .filter(
                free_entrance=True,
                )
    
    abc_filter = request.GET.get('by-abc', None)
    abc_list = get_abc_list(qs, "title", abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "title", abc_filter)
    
    
    extra_context = {}
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
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
