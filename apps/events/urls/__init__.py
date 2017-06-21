# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url, include
from django.conf import settings
from jetson.apps.utils.views import object_detail
from jetson.apps.utils.context_processors import prev_next_processor
from kb.apps.events.utils import Event
from kb.apps.media_gallery.sites import PortfolioSite

event_list_info = {
    'queryset': Event.objects.all(),
    'template_name': 'events/event_list.html',
    'paginate_by': 24,
    'allow_empty': True,
    'context_processors': (prev_next_processor,),
}

event_details_info = {
    'queryset': Event.objects.all(),
    'slug_field': 'slug',
    'template_name': 'events/event_details.html',
    'context_processors': (prev_next_processor,),
    'context_item_type': 'event',
}

OPTIONAL_DATE_REGEX = (
    r'('
    r'(?P<start_date>\d{8})'
    r'((?P<unlimited>...)|-(?P<end_date>\d{8}))?/'
    r')?'
)

urlpatterns = (
    url(
        r'^$',
        'kb.apps.events.views.event_list',
        event_list_info,
        name="event_list_global",
    ),
    url(
        r'^'
        r'((?P<show>favorites|memos|own-events)/)'
        + OPTIONAL_DATE_REGEX +
        r'$',
        'kb.apps.events.views.event_list',
        event_list_info,
        name="event_list_global",
    ),
    url(
        r'^'
        r'((?P<show>favorites|memos|own-events)/)?'
        + OPTIONAL_DATE_REGEX +
        r'ical/'
        r'$',
        'kb.apps.events.views.event_list_ical',
        event_list_info,
    ),
    url(
        r'^'
        r'((?P<show>favorites|memos|own-events)/)?'
        + OPTIONAL_DATE_REGEX +
        r'feeds/'
        r'(?P<feed_type>[^/]+)/'
        r'$',
        'kb.apps.events.views.event_list_feed',
        event_list_info,
    ),
    url(r'^add/$', 'kb.apps.events.views.add_event'),

    # events have their dates prefixed (or not, if there aren't any)
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'((?P<event_time>\d+)/)?'
        r'$',
        'kb.apps.events.views.event_detail',
        event_details_info,
        name="event_detail",
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'claim/'
        r'$',
        'kb.apps.site_specific.views.claim_object',
        {'ot_url_part': 'event'},
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'delete/'
        r'$',
        'kb.apps.site_specific.views.delete_object',
        {'ot_url_part': 'event'},
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'map/'
        r'$',
        object_detail,
        dict(event_details_info, template_name="events/event_map.html"),
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'reviews/'
        r'$',
        object_detail,
        dict(
            event_details_info,
            template_name="events/event_reviews.html",
        ),
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'network/'
        r'$',
        object_detail,
        dict(
            event_details_info,
            template_name="events/event_network.html",
        ),
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'((?P<event_time>\d+)/)?'
        r'ical/'
        r'$',
        'kb.apps.events.views.event_ical',
    ),

    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'portfolio/',
        include(PortfolioSite(
            object_detail_dict=event_details_info,
            app_name="events",
            name="event",
        ).urls),
    )
)
