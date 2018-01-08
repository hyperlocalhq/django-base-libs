# -*- coding: UTF-8 -*-
import re
from datetime import datetime, timedelta
from time import strptime

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.encoding import smart_unicode, force_unicode
from django.contrib.syndication.views import Feed
from django.utils import translation
from django.views.decorators.cache import never_cache
from django.utils.timezone import now as tz_now

from base_libs.utils.misc import get_related_queryset
from base_libs.utils.misc import get_website_url
from base_libs.forms import dynamicforms
from base_libs.views import access_denied

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail, get_abc_list, filter_abc, get_year_list, filter_year, show_form_step
from jetson.apps.events.utils import create_ics

from jetson.apps.events.models import URL_ID_EVENT, URL_ID_EVENTS, SECURITY_SUMMAND
from jetson.apps.events.forms import ADD_EVENT_FORM_STEPS, EventSearchForm
Event = models.get_model("events", "Event")
EventTime = models.get_model("events", "EventTime")

class EventFeed(Feed):
    title = ""
    link = ""
    description = ""
    title_template = "events/feeds/feed_title.html"
    description_template = "events/feeds/feed_description.html"
    
    def __init__(self, request, queryset=Event.objects.none, title="", description="", link=""):
        super(EventFeed, self).__init__("", request)
        if callable(queryset):
            queryset = queryset()
        self.queryset = queryset
        if title:
            self.title = title
        if description:
            self.description = description
        if link:
            self.link = link
    
    def items(self):
        return self.queryset.order_by('-creation_date')[:20]

@never_cache
def event_list(request, criterion="", slug="", show="", start_date=None, end_date=None, unlimited=False, title="", **kwargs):
    """Displays the list of events"""
    
    abc_list = None
    abc_filter = request.GET.get('by-abc', None)
    
    if show=="own-%s" % URL_ID_EVENTS:
        if not request.user.is_authenticated():
            return access_denied(request)
        PersonGroup = models.get_model("groups_networks", "PersonGroup")
        ct = ContentType.objects.get_for_model(kwargs['queryset'].model)
        owned_inst_ids = [
            el['object_id'] for el in PersonGroup.objects.filter(
                groupmembership__user=request.user,
                content_type=ct,
            ).distinct().values("object_id")
            ]
        kwargs['queryset'] = kwargs['queryset'].filter(
            models.Q(organizing_person=request.user.profile)
            | models.Q(organizing_institution__pk__in=owned_inst_ids)
            )
    elif show!="related":
        kwargs['queryset'] = kwargs['queryset'].filter(
            status="published",
            )

    form = EventSearchForm(data=request.REQUEST)
    if form.is_valid():
        et = form.cleaned_data['event_type']
        if et:
            kwargs['queryset'] = kwargs['queryset'].filter(
                event_type=et,
                )
        is_featured = form.cleaned_data['is_featured']
        if is_featured:
            kwargs['queryset'] = kwargs['queryset'].filter(
                is_featured = True,
                )
        
        kw = form.cleaned_data['keywords']
    queryset = kwargs['queryset']
    date_filter = None
    if start_date:
        try: # convert a string of a format "YYYYMMDD" to date
            start_date = datetime(*strptime(start_date, "%Y%m%d")[:3])
        except ValueError:
            raise Http404, _("Naughty hacker!")
            
        if end_date:
            try: # convert a string of a format "YYYYMMDD" to date
                end_date = datetime(*strptime(end_date, "%Y%m%d")[:3])
            except ValueError:
                raise Http404, _("Naughty hacker!")
                
        if not (end_date or unlimited):
            end_date = start_date + timedelta(days=1)

        if start_date and end_date:
            """
            Get events which start date is within the selected range
            -----[--selected range--]----- time ->
                       [-event-]
                              [-event-]
            """
            date_filter = models.Q(
                start__gte=start_date,
                start__lte=end_date,
                )
            """
            .. which started before and will end after the selected range
            -----[-selected range-]------- time ->
               [------event---------]
            """
            date_filter |= models.Q(
                start__lte=start_date,
                end__gte=end_date,
                )
            """
            .. or which end date is within the selected range
            -----[--selected range--]----- time ->
                     [-event-]
              [-event-]
            """
            date_filter |= models.Q(
                end__gte=start_date,
                end__lte=end_date,
                )
        else:
            """
            Get events which start date is after the selected start
            -----[--selected start-------- time ->
                    [-event-]
            """
            date_filter = models.Q(
                start__gte=start_date,
                )
            """
            .. or which end date is after the selected start
            -----[--selected start-------- time ->
               [-event-]
            """
            date_filter |= models.Q(
                end__gte=start_date,
                )
                
    if date_filter:
        event_time_pks = list(EventTime.objects.filter(date_filter).values_list(
            "event_id",
            flat=True,
            ))
        queryset = queryset.filter(pk__in=event_time_pks)
        
    abc_list = get_abc_list(queryset, "title", abc_filter)
    if abc_filter:
        queryset = filter_abc(queryset, "title", abc_filter)
    
    view_type = request.REQUEST.get('view_type', request.httpstate.get(
        "%s_view_type" % URL_ID_EVENTS,
        "icons",
        ))
    if view_type == "map":
        queryset = queryset.filter(
            postal_address__geoposition__latitude__gte=-90,
            ).distinct()
        
    extra_context = kwargs.setdefault("extra_context", {})
    extra_context['abc_list'] = abc_list
    extra_context['show'] = ("", "/%s" % show)[bool(show and show!="related")]
    extra_context['source_list'] = URL_ID_EVENTS
    extra_context['today'] = tz_now()
    extra_context['form'] = form
    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"
    kwargs['extra_context'] = extra_context
    kwargs['httpstate_prefix'] = URL_ID_EVENTS
    kwargs['queryset'] = queryset
    
    if kwargs.has_key('ical') and kwargs['ical'] == True:
        icalstream = create_ics(kwargs['queryset'])
        response = HttpResponse(icalstream, content_type="text/calendar")
        response['Filename'] = "CCB-events.ics" # IE needs this
        response['Content-Disposition'] = "attachment; filename=CCB-events.ics"
        return response
    elif kwargs.has_key('feed') and kwargs['feed'] == True:
        translation.activate(kwargs['language'])
        feed_part = re.compile("/feed/[^/]+/[^/]+/$")
        url = get_website_url()
        feedgen = EventFeed(
            request,
            queryset=queryset,
            title=title or _("CCB Events"),
            link=kwargs.get(
                "link",
                url[:-1] + feed_part.sub("/", request.path) + "?" + (request.META.get("QUERY_STRING", "") or ""),
                ),
            ).get_feed(kwargs['feed_type'])
    
        response = HttpResponse(content_type=feedgen.mime_type)
        feedgen.write(response, 'utf-8')
        return response
    else:
        return object_list(request, **kwargs)

@never_cache
def event_list_ical(request, **kwargs):
    return event_list(request, ical=True, **kwargs)

@never_cache
def event_list_feed(request, **kwargs):
    return event_list(request, feed=True, **kwargs)

@never_cache
def add_event(request):
    return show_form_step(request, ADD_EVENT_FORM_STEPS, extra_context={})


add_event = login_required(add_event)

def event_detail(request, event_time=None, ical=False, *args, **kwargs):
    event = get_object_or_404(Event, slug=kwargs['slug'])
    if event_time:
        kwargs.setdefault("extra_context", {})
        event_time = kwargs['extra_context']['event_time'] = get_object_or_404(
            EventTime,
            pk=int(event_time)-SECURITY_SUMMAND,
            )
        
    if ical:
        icalstream = create_ics(event_time or event)
        response = HttpResponse(icalstream, content_type="text/calendar")
        response['Filename'] = "event-%s.ics" % event.slug # IE needs this
        response['Content-Disposition'] = "attachment; filename=event-%s.ics" % event.slug
        return response
    else:
        return object_detail(request, *args, **kwargs)

def event_ical(request, *args, **kwargs):
    return event_detail(request, ical=True, *args, **kwargs)
