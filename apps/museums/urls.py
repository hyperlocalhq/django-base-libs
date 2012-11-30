# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.museums.views',
    url(r'^$', 'museum_list', name='museum_list'),
    url(r'^export-json-museums/$', 'export_json_museums', name='export_json_museums'),
    url(r'^add/$', 'add_museum', name='add_museum'),    
    url(r'^(?P<slug>[^/]+)/$', 'museum_detail', name='museum_detail'),    
    url(r'^(?P<slug>[^/]+)/change/$', 'change_museum', name='change_museum'),    
)
