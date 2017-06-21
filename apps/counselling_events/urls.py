# -*- coding: UTF-8 -*-
from django.conf.urls import *
from jetson.apps.utils.context_processors import prev_next_processor
from kb.apps.events.models import Event, EventTime

event_list_info = {
    'queryset': EventTime.objects.filter(event__status__in=["published", "expired"]),
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
    'paginate_by': 24,
}

event_details_info = {
    'queryset': Event.objects.all(),
    'slug_field': 'slug',
    'template_name': 'counselling_events/event_details.html',
    'context_processors': (prev_next_processor,),
    'context_item_type': 'event',
}


urlpatterns = [
    url(
        r'^$',
        'kb.apps.counselling_events.views.counselling_events_list',
        event_list_info,
        name="counselling_event_list"
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'((?P<event_time>\d+)/)?'
        r'$',
        'kb.apps.counselling_events.views.counselling_event_detail',
        event_details_info,
        name="event_detail",
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'((?P<event_time>\d+)/)?'
        r'ical/'
        r'$',
        'kb.apps.counselling_events.views.counselling_event_ical',
    ),
]
