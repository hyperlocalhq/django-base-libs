# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import TemplateView

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_detail
from jetson.apps.utils.context_processors import prev_next_processor
from ccb.apps.events.utils import Event
from ccb.apps.media_gallery.sites import PortfolioSite
from ccb.apps.site_specific import views as site_specific_views
from ccb.apps.events import views as events_views

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
        events_views.event_list,
        event_list_info,
        name="event_list_global",
    ),
    url(
        r'^'
        r'((?P<show>favorites|memos|own-events)/)'
        + OPTIONAL_DATE_REGEX +
        r'$',
        login_required(events_views.event_list),
        event_list_info,
        name="event_list_global",
    ),
    url(
        r'^'
        r'((?P<show>favorites|memos|own-events)/)?'
        + OPTIONAL_DATE_REGEX +
        r'ical/'
        r'$',
        events_views.event_list_ical,
        event_list_info,
    ),
    url(
        r'^'
        r'((?P<show>favorites|memos|own-events)/)?'
        + OPTIONAL_DATE_REGEX +
        r'feeds/'
        r'(?P<feed_type>[^/]+)/'
        r'$',
        events_views.event_list_feed,
        event_list_info,
    ),
    url(r'^add/$', events_views.add_event),

    # success pages
    url(r'^created/$', TemplateView.as_view(template_name='events/event_created.html'), name="event_created"),
    url(r'^deleted/$', TemplateView.as_view(template_name='events/event_deleted.html'), name="event_deleted"),

    # events have their dates prefixed (or not, if there aren't any)
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'((?P<event_time>\d+)/)?'
        r'$',
        events_views.event_detail,
        event_details_info,
        name="event_detail",
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'claim/'
        r'$',
        site_specific_views.claim_object,
        {'ot_url_part': 'event'},
    ),
    url(
        r'^'
        r'event/'
        r'(?P<slug>[^/]+)/'
        r'delete/'
        r'$',
        site_specific_views.delete_object,
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
        'ccb.apps.events.views.event_ical',
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
