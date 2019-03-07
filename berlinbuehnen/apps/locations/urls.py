# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.locations.views',
    url(r'^$', 'location_list', name='location_list'),
    url(r'^map/$', 'location_list_map', name='location_list_map'),
    url(r'^add/$', 'add_location', name='add_location'),
    url(r'^(?P<slug>[^/]+)/$', 'location_detail', name='location_detail'),
    url(r'^(?P<slug>[^/]+)/ajax/map/$', 'location_detail_ajax', name='location_detail_ajax'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_location', name='change_location'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_location', name='delete_location'),
    url(r'^(?P<slug>[^/]+)/status/$', 'change_location_status', name='change_location_status'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'image_overview', name='location_image_overview'),
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_image', name='location_add_image'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_image', name='location_change_image'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_image', name='location_delete_image'),
)
