# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.productions.views',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^add/$', 'add_production', name='add_production'),
    url(r'^(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)/$', 'event_list', name='event_list_for_a_day'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_production', name='change_production'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_production', name='delete_production'),
    url(r'^(?P<slug>[^/]+)/status/$', 'change_production_status', name='change_production_status'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'gallery_overview', name='production_gallery_overview'),
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_mediafile', name='production_add_mediafile'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_mediafile', name='production_change_mediafile'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_mediafile', name='production_delete_mediafile'),
    # events
    url(r'^(?P<slug>[^/]+)/events/$', 'events_overview', name='production_events_overview'),
    url(r'^(?P<slug>[^/]+)/events/add/$', 'add_events', name='add_events'),
    url(r'^(?P<slug>[^/]+)/(?P<event_id>[^/]+)/$', 'event_detail', name='event_detail'),
    url(r'^(?P<slug>[^/]+)/(?P<event_id>[^/]+)/change/basic-info/$', 'change_event_basic_info', name='change_event_basic_info'),
    url(r'^(?P<slug>[^/]+)/(?P<event_id>[^/]+)/change/description/$', 'change_event_description', name='change_event_description'),
    url(r'^(?P<slug>[^/]+)/(?P<event_id>[^/]+)/change/gallery/$', 'change_event_gallery', name='change_event_gallery'),
    url(r'^(?P<slug>[^/]+)/(?P<event_id>[^/]+)/delete/$', 'delete_event', name='delete_event'),
)
