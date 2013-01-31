# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.museums.views',
    url(r'^$', 'museum_list', name='museum_list'),
    url(r'^export-json-museums/$', 'export_json_museums', name='export_json_museums'),
    url(r'^add/$', 'add_museum', name='add_museum'),    
    url(r'^(?P<slug>[^/]+)/$', 'museum_detail', name='museum_detail'),    
    url(r'^(?P<slug>[^/]+)/change/$', 'change_museum', name='change_museum'),
    # gallery    
    url(r'^(?P<slug>[^/]+)/gallery/$', 'gallery_overview', name='museum_gallery_overview'),    
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_mediafile', name='museum_add_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<token>[^/]+)/$', 'create_update_mediafile', name='museum_change_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<token>[^/]+)/delete/$', 'delete_mediafile', name='museum_delete_mediafile'),    
)
