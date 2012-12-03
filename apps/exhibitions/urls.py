# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.exhibitions.views',
    url(r'^$', 'exhibition_list', name='exhibition_list'),
    url(r'^export-json-exhibitions/$', 'export_json_exhibitions', name='export_json_exhibitions'),
    url(r'^add/$', 'add_exhibition', name='add_exhibition'),    
    url(r'^(?P<slug>[^/]+)/$', 'exhibition_detail', name='exhibition_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_exhibition', name='change_exhibition'),    
)
