# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.events.views',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^add/$', 'add_event', name='add_event'),    
    url(r'^(?P<slug>[^/]+)/$', 'event_detail', name='event_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_event', name='change_event'),    
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'gallery_overview', name='event_gallery_overview'),    
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_mediafile', name='event_add_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_mediafile', name='event_change_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_mediafile', name='event_delete_mediafile'),    
)
