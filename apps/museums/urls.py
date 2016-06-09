# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('museumsportal.apps.museums.views',
    url(r'^$', 'museum_list', name='museum_list'),
    url(r'^map/$', 'museum_list_map', name='museum_list_map'),
    url(r'^export-json-museums/$', 'export_json_museums', name='export_json_museums'),
    url(r'^add/$', 'add_museum', name='add_museum'),    
    url(r'^(?P<slug>[^/]+)/$', 'museum_detail', name='museum_detail'),    
    url(r'^(?P<slug>[^/]+)/ajax/$', 'museum_detail_ajax', name='museum_detail_ajax'),
    url(r'^(?P<slug>[^/]+)/ajax/map/$', 'museum_detail_ajax', {'template_name': 'museums/museum_detail_ajax_map.html'}, name='museum_detail_ajax_map'),
    url(r'^(?P<slug>[^/]+)/slideshow/$', 'museum_detail_slideshow', name='museum_detail_slideshow'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_museum', name='change_museum'),
    url(r'^(?P<slug>[^/]+)/products/$', 'museum_products', name='museum_products'),
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'gallery_overview', name='museum_gallery_overview'),    
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_mediafile', name='museum_add_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_mediafile', name='museum_change_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_mediafile', name='museum_delete_mediafile'),    
)
