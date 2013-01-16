# -*- coding: utf-8 -*-
from django.db import models
from django.http import HttpResponse
from django import forms
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404

from base_libs.templatetags.base_tags import decode_entities
from base_libs.forms import dynamicforms
from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.misc import get_related_queryset
from base_libs.views.views import access_denied

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.context_processors import prev_next_processor

MuseumCategory = models.get_model("museums", "MuseumCategory")
Museum = models.get_model("museums", "Museum")

from forms.museum import MUSEUM_FORM_STEPS

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
            'categories': MuseumCategory.objects.all().order_by("title_%s" % request.LANGUAGE_CODE),
            'open_on_mondays': _("Open on Mondays"),
            'free_entrance': _("Free entrance"),
            },
        }
    
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories=cat,
                ).distinct()
        open_on_mondays = form.cleaned_data['open_on_mondays']
        if open_on_mondays:
            facets['selected']['open_on_mondays'] = True
            qs = qs.filter(
                open_on_mondays=True,
                )
        free_entrance = form.cleaned_data['free_entrance']
        if free_entrance:
            facets['selected']['free_entrance'] = True
            qs = qs.filter(
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
        httpstate_prefix="museum_list",
        context_processors=(prev_next_processor,),
        )

def museum_detail(request, slug):
    qs = Museum.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="museums/museum_detail.html",
        context_processors=(prev_next_processor,),
        )

def export_json_museums(request):    
    #create queryset
    qs = Museum.objects.filter(status="published")
   
    museums = []
    for m in qs:        
        data ={
            'title': m.title,
            'subtitle': m.subtitle,
            'description': decode_entities(m.description),
            'image_caption': m.image_caption,
            'street_address': m.street_address,
            'street_address2': m.street_address2,
            'postal_code': m.postal_code,
            'city': m.city,
            'country': m.country,
            'latitude': m.latitude,
            'longitude': m.longitude,
            'phone': m.phone,
            'fax': m.fax,
            'email': m.email,
            'website': m.website,
            'open_on_mondays': m.open_on_mondays,
            'free_entrance': m.free_entrance,
            'status': m.status,
        }
        categories = []
        for cat in m.categories.all():
            categories.append({
                'id': cat.id,
                'title': cat.title,
            })
        data['categories'] = categories
        museums.append(data)
    
    json = simplejson.dumps(museums, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json, mimetype='text/javascript; charset=utf-8')

@never_cache
@login_required
def add_museum(request):
    return show_form_step(request, MUSEUM_FORM_STEPS, extra_context={});
    
@never_cache
@login_required
def change_museum(request, slug):
    instance = get_object_or_404(Museum, slug=slug)
    if not request.user.has_perm("museums.change_museum", instance):
        return access_denied(request)
    return show_form_step(request, MUSEUM_FORM_STEPS, extra_context={'museum': instance}, instance=instance);

