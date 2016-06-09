# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('museumsportal.apps.museumssummer.views',
    url(r'^$', 'location_list_map', name='location_list_map'),
    url(r'^(?P<slug>[^/]+)/ajax/map/$', 'location_detail_ajax', name='location_detail_ajax_map'),
)
