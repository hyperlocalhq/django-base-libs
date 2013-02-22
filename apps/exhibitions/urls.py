# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.exhibitions.views',
    url(r'^$', 'exhibition_list', name='exhibition_list'),
    url(r'^vernissages/$', 'vernissage_list', name='vernissage_list'),
    url(r'^export-json-exhibitions/$', 'export_json_exhibitions', name='export_json_exhibitions'),
    url(r'^add/$', 'add_exhibition', name='add_exhibition'),    
    url(r'^(?P<slug>[^/]+)/$', 'exhibition_detail', name='exhibition_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_exhibition', name='change_exhibition'),    
    # gallery
    url(r'^(?P<slug>[^/]+)/gallery/$', 'gallery_overview', name='exhibition_gallery_overview'),    
    url(r'^(?P<slug>[^/]+)/gallery/add/$', 'create_update_mediafile', name='exhibition_add_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/$', 'create_update_mediafile', name='exhibition_change_mediafile'),    
    url(r'^(?P<slug>[^/]+)/gallery/file_(?P<mediafile_token>[^/]+)/delete/$', 'delete_mediafile', name='exhibition_delete_mediafile'),    
)
