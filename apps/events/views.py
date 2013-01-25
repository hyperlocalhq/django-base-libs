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

EventCategory = models.get_model("events", "EventCategory")
Event = models.get_model("events", "Event")

from forms.event import EVENT_FORM_STEPS

STATUS_CHOICES = (
    ("newly_opened", _("Newly opened")),
    ("closing_soon", _("Closing soon")),
    )

class EventSearchForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(Event, "categories"),
        )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        )

def event_list(request):
    qs = Event.objects.filter(status="published")
    
    #if not request.REQUEST.keys():
    #    return redirect("/%s%s?status=newly_opened" % (request.LANGUAGE_CODE, request.path))
    
    form = EventSearchForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(Event, "categories").order_by("title_%s" % request.LANGUAGE_CODE),
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
                # today - 2 weeks < EVENT START <= today
                qs = qs.filter(
                    eventtime__event_date__gt=today-two_weeks,
                    eventtime__event_date__lte=today,
                    )
            elif status == "closing_soon":
                # today <= EVENT END < today + two weeks
                qs = qs.filter(
                    eventtime__event_date__gte=today,
                    eventtime__event_date__lt=today+two_weeks,
                    )
    if status == "closing_soon":
        qs = qs.order_by("eventtime__event_date", "title_%s" % request.LANGUAGE_CODE)
    else:
        qs = qs.order_by("-eventtime__event_date", "title_%s" % request.LANGUAGE_CODE)
        
    extra_context = {}
    extra_context['form'] = form
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="events/event_list.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="event_list",
        context_processors=(prev_next_processor,),
        )

def event_detail(request, slug):
    qs = Event.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="events/event_detail.html",
        context_processors=(prev_next_processor,),
        )

@never_cache
@login_required
def add_event(request):
    return show_form_step(request, EVENT_FORM_STEPS, extra_context={});
    
@never_cache
@login_required
def change_event(request, slug):
    instance = get_object_or_404(Event, slug=slug)
    if not request.user.has_perm("events.change_event", instance):
        return access_denied(request)
    return show_form_step(request, EVENT_FORM_STEPS, extra_context={'event': instance}, instance=instance);

