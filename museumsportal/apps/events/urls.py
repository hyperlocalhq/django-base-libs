# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

from feeds import EventRssFeed

urlpatterns = patterns('museumsportal.apps.events.views',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^map/$', 'event_list_map', name='event_list_map'),
    url(r'^add/$', 'add_event', name='add_event'),
    url(r'^rss/$', EventRssFeed()),
    url(r'^(?P<slug>[^/]+)/$', 'event_detail', name='event_detail'),
    url(r'^(?P<slug>[^/]+)/ajax/$', 'event_detail_ajax', name='event_detail_ajax'),
    url(r'^(?P<slug>[^/]+)/ajax/map/$', 'event_detail_ajax', {'template_name': 'events/event_detail_ajax_map.html'}, name='event_detail_ajax_map'),
    url(r'^(?P<slug>[^/]+)/slideshow/$', 'event_detail_slideshow', name='event_detail_slideshow'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_event', name='change_event'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_event', name='delete_event'),    
    url(r'^(?P<slug>[^/]+)/status/$', 'change_event_status', name='change_event_status'),    
    url(r'^(?P<slug>[^/]+)/batch-event-times/$', 'batch_event_times', name='batch_event_times'),    
    url(r'^(?P<slug>[^/]+)/products/$', 'event_products', name='event_products'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'gallery_overview', name='event_gallery_overview'),    
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_mediafile', name='event_add_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_mediafile', name='event_change_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_mediafile', name='event_delete_mediafile'),    
)
