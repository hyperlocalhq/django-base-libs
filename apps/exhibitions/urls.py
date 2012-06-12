# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.exhibitions.views',
    url(r'^$', 'exhibition_list', name='exhibition_list'),
    url(r'^(?P<slug>[^/]+)/$', 'exhibition_detail', name='exhibition_detail'),
)
