# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.locations.views',
    url(r'^$', 'location_list', name='location_list'),
    url(r'^add/$', 'add_location', name='add_location'),
    url(r'^(?P<slug>[^/]+)/$', 'location_detail', name='location_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_location', name='change_location'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_location', name='delete_location'),
    url(r'^(?P<slug>[^/]+)/status/$', 'change_location_status', name='change_location_status'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'gallery_overview', name='location_gallery_overview'),
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_mediafile', name='location_add_mediafile'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_mediafile', name='location_change_mediafile'),
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_mediafile', name='location_delete_mediafile'),
)
