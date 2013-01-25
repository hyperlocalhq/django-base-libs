# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta

from django.db import models
from django.http import HttpResponse
from django import forms
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404

from base_libs.templatetags.base_tags import decode_entities
from base_libs.forms import dynamicforms
from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.misc import get_related_queryset
from base_libs.views.views import access_denied

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.context_processors import prev_next_processor

WorkshopCategory = models.get_model("workshops", "WorkshopCategory")
Workshop = models.get_model("workshops", "Workshop")

from forms.workshop import WORKSHOP_FORM_STEPS

STATUS_CHOICES = (
    ("newly_opened", _("Newly opened")),
    ("closing_soon", _("Closing soon")),
    )

class WorkshopSearchForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Workshop, "categories"),
        )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        )

def workshop_list(request):
    qs = Workshop.objects.filter(status="published")
    
    #if not request.REQUEST.keys():
    #    return redirect("/%s%s?status=newly_opened" % (request.LANGUAGE_CODE, request.path))
    
    form = WorkshopSearchForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(Workshop, "categories").order_by("title_%s" % request.LANGUAGE_CODE),
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
                # today - 2 weeks < WORKSHOP START <= today
                qs = qs.filter(
                    workshoptime__workshop_date__gt=today-two_weeks,
                    workshoptime__workshop_date__lte=today,
                    )
            elif status == "closing_soon":
                # today <= WORKSHOP END < today + two weeks
                qs = qs.filter(
                    workshoptime__workshop_date__gte=today,
                    workshoptime__workshop_date__lt=today+two_weeks,
                    )
    if status == "closing_soon":
        qs = qs.order_by("workshoptime__workshop_date", "title_%s" % request.LANGUAGE_CODE)
    else:
        qs = qs.order_by("-workshoptime__workshop_date", "title_%s" % request.LANGUAGE_CODE)
        
    extra_context = {}
    extra_context['form'] = form
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="workshops/workshop_list.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="workshop_list",
        context_processors=(prev_next_processor,),
        )

def workshop_detail(request, slug):
    qs = Workshop.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="workshops/workshop_detail.html",
        context_processors=(prev_next_processor,),
        )

@never_cache
@login_required
def add_workshop(request):
    return show_form_step(request, WORKSHOP_FORM_STEPS, extra_context={});
    
@never_cache
@login_required
def change_workshop(request, slug):
    instance = get_object_or_404(Workshop, slug=slug)
    if not request.user.has_perm("workshops.change_workshop", instance):
        return access_denied(request)
    return show_form_step(request, WORKSHOP_FORM_STEPS, extra_context={'workshop': instance}, instance=instance);

