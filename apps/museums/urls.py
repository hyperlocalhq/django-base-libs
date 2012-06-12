# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.museums.views',
    url(r'^$', 'museum_list', name='museum_list'),
    url(r'^(?P<slug>[^/]+)/$', 'museum_detail', name='museum_detail'),
)
