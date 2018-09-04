# -*- coding: UTF-8 -*-

from django.conf.urls import *

from feeds import EventRssFeed

from . import views

urlpatterns = [
    url(r'^$', views.event_list, name='event_list'),
    url(r'^map/$', views.event_list_map, name='event_list_map'),
    url(r'^add/$', views.add_event, name='add_event'),
    url(r'^rss/$', EventRssFeed()),
    url(r'^(?P<slug>[^/]+)/$', views.event_detail, name='event_detail'),
    url(r'^(?P<slug>[^/]+)/ajax/$', views.event_detail_ajax, name='event_detail_ajax'),
    url(r'^(?P<slug>[^/]+)/ajax/map/$', views.event_detail_ajax, {'template_name': 'events/event_detail_ajax_map.html'}, name='event_detail_ajax_map'),
    url(r'^(?P<slug>[^/]+)/slideshow/$', views.event_detail_slideshow, name='event_detail_slideshow'),
    url(r'^(?P<slug>[^/]+)/change/$', views.change_event, name='change_event'),
    url(r'^(?P<slug>[^/]+)/delete/$', views.delete_event, name='delete_event'),
    url(r'^(?P<slug>[^/]+)/status/$', views.change_event_status, name='change_event_status'),
    url(r'^(?P<slug>[^/]+)/batch-event-times/$', views.batch_event_times, name='batch_event_times'),
    url(r'^(?P<slug>[^/]+)/products/$', views.event_products, name='event_products'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', views.gallery_overview, name='event_gallery_overview'),
    url(r'^(?P<slug>[^/]+)/gallery/add/$', views.create_update_mediafile, name='event_add_mediafile'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', views.create_update_mediafile, name='event_change_mediafile'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', views.delete_mediafile, name='event_delete_mediafile'),
]
