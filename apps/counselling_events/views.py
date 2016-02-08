# -*- coding: UTF-8 -*-

from django.apps import apps
from django.db import models
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from base_libs.views import access_denied

from jetson.apps.utils.views import object_detail

from ccb.apps.site_specific.models import ContextItem
from ccb.apps.events.views import event_list
from ccb.apps.events.models import SECURITY_SUMMAND
from ccb.apps.events.utils import create_ics

Event = apps.get_model("events", "Event")
EventTime = apps.get_model("events", "EventTime")


@never_cache
def counselling_events_list(request, **kwargs):
    """
    Lists the institution's events
    """
    item = get_object_or_404(
        ContextItem,
        content_type__model__in=("person", "institution"),
        slug=u'kreativwirtschaftsberatung_berlin',
    )
    if item.is_person():
        if not request.user.has_perm("people.change_person", item.content_object) and item.status not in (
        "published", "published_commercial"):
            return access_denied(request)
        person = item.content_object
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(organizing_person=person)
        ).order_by('-creation_date')
    else:
        if not request.user.has_perm("institutions.change_institution", item.content_object) and item.status not in (
        "published", "published_commercial"):
            return access_denied(request)
        institution = item.content_object
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(organizing_institution=institution) |
            models.Q(venue=institution),
        ).order_by('-creation_date')

    kwargs['template_name'] = 'counselling_events/event_list.html'
    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = item.content_object
    kwargs['title'] = _("Events by/at %s") % item.content_object.get_title()
    return event_list(request, show="related", **kwargs)


def counselling_event_detail(request, event_time=None, ical=False, *args, **kwargs):
    event = get_object_or_404(Event, slug=kwargs['slug'])
    if event_time:
        kwargs.setdefault("extra_context", {})
        event_time = kwargs['extra_context']['event_time'] = get_object_or_404(
            EventTime,
            pk=int(event_time) - SECURITY_SUMMAND,
        )

    if ical:
        icalstream = create_ics(event_time or event)
        response = HttpResponse(icalstream, content_type="text/calendar")
        response['Filename'] = "event-%s.ics" % event.slug  # IE needs this
        response['Content-Disposition'] = "attachment; filename=event-%s.ics" % event.slug
        return response
    else:
        return object_detail(request, *args, **kwargs)


def counselling_event_ical(request, *args, **kwargs):
    return counselling_event_detail(request, ical=True, *args, **kwargs)
