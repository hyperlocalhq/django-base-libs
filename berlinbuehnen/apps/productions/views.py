# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.conf import settings

from base_libs.views.views import access_denied

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc
from jetson.apps.utils.context_processors import prev_next_processor

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

from models import Production, Event

class EventFilterForm(forms.Form):
    pass


def event_list(request, year=None, month=None, day=None):
    #qs = Event.objects.filter(production__status="published")
    qs = Event.objects.all()

    form = EventFilterForm(data=request.REQUEST)
    
    facets = {
        'selected': {},
        'categories': {
        },
    }
    
    if form.is_valid():
        pass
        # cat = form.cleaned_data['category']
        # if cat:
        #     facets['selected']['category'] = cat
        #     qs = qs.filter(
        #         categories=cat,
        #     ).distinct()
        #

    abc_filter = request.GET.get('abc', None)
    if abc_filter:
        facets['selected']['abc'] = abc_filter
    abc_list = get_abc_list(qs, "production__title_%s" % request.LANGUAGE_CODE, abc_filter)
    if abc_filter:
        qs = filter_abc(qs, "production__title_%s" % request.LANGUAGE_CODE, abc_filter)

    # qs = qs.extra(select={
    #     'title_uni': "IF (events_event.title_%(lang_code)s = '', events_event.title_de, events_event.title_%(lang_code)s)" % {
    #         'lang_code': request.LANGUAGE_CODE,
    #     }
    # }).order_by("title_uni")

    #qs = qs.prefetch_related("season_set", "mediafile_set", "categories", "accessibility_options").defer("tags")
    
    extra_context = {}
    extra_context['form'] = form
    extra_context['abc_list'] = abc_list
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="events/event_list.html",
        paginate_by=24,
        extra_context=extra_context,
        httpstate_prefix="event_list",
        context_processors=(prev_next_processor,),
    )


def event_detail(request, slug, event_id):
    if "preview" in request.REQUEST:
        qs = Event.objects.all()
        obj = get_object_or_404(qs, production__slug=slug, pk=event_id)
        if not request.user.has_perm("events.change_event", obj):
            return access_denied(request)
    else:
        #qs = Event.objects.filter(production__status="published")
        qs = Event.objects.all()
    return object_detail(
        request,
        queryset=qs,
        object_id=event_id,
        template_name="events/event_detail.html",
        context_processors=(prev_next_processor,),
    )
