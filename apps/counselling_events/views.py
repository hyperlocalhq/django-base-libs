# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
from time import strptime

from django.apps import apps
from django.db import models
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _, ugettext
from django.http import HttpResponse
from django.utils.timezone import now

from base_libs.views import access_denied

from jetson.apps.utils.views import object_list, object_detail

from ccb.apps.site_specific.models import ContextItem
from ccb.apps.events.views import event_list
from ccb.apps.events.models import SECURITY_SUMMAND
from ccb.apps.events.utils import create_ics

Event = apps.get_model("events", "Event")
EventTime = apps.get_model("events", "EventTime")
Institution = apps.get_model("institutions", "Institution")

@never_cache
def event_list(request, criterion="", slug="", show="", start_date=None, end_date=None, unlimited=False, title="",
               **kwargs):
    """Displays the list of events"""

    queryset = kwargs['queryset']

    extra_context = kwargs.setdefault("extra_context", {})
    extra_context['show'] = ("", "/%s" % show)[bool(show and show != "related")]
    extra_context['today'] = datetime.now()
    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"
    kwargs['extra_context'] = extra_context
    kwargs['httpstate_prefix'] = "counselling_events"
    kwargs['queryset'] = queryset

    return object_list(request, **kwargs)


class AbsoluteTimeDistance(models.Func):
    template = "ABS(EXTRACT(epoch FROM NOW() - %(expressions)s))"


@never_cache
def counselling_events_list(request, **kwargs):
    """
    Lists the institution's events
    """
    queryset = kwargs['queryset']

    item = get_object_or_404(
        ContextItem,
        content_type__model="institution",
        slug=u'kreativwirtschaftsberatung_berlin',
    )
    if not request.user.has_perm("institutions.change_institution", item.content_object) and item.status not in (
    "published", "published_commercial"):
        return access_denied(request)

    institution = item.content_object
    other_institutions = list(Institution.objects.filter(slug="kulturfoerderpunkt_berlin"))
    institution_list = [institution] + other_institutions
    queryset = queryset.filter(
        models.Q(event__organizing_institution__in=institution_list) |
        models.Q(event__venue__in=institution_list),
    ).annotate(
        present_then_past=models.Case(
            models.When(end__lt=now(), then=models.Value(1)),
            default=models.Value(0),
            output_field=models.IntegerField(),
        ),
        distance=AbsoluteTimeDistance(models.F('start')),
    ).order_by('present_then_past', 'distance')

    kwargs['template_name'] = 'counselling_events/event_list.html'
    kwargs.setdefault("extra_context", {})
    kwargs['extra_context']['object'] = item.content_object
    kwargs['title'] = _("Events by/at %s") % item.content_object.get_title()

    extra_context = kwargs.setdefault("extra_context", {})
    extra_context['today'] = datetime.now()
    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"
    kwargs['extra_context'] = extra_context
    kwargs['httpstate_prefix'] = "counselling_events"
    kwargs['queryset'] = queryset

    return object_list(request, **kwargs)


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
