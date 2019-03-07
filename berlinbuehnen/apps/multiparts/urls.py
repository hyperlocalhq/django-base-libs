# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.multiparts.views',
    url(r'^$', 'multipart_list', name='multipart_list'),
    url(r'^add/$', 'add_multipart', name='add_multipart'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_multipart', name='change_multipart'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_multipart', name='delete_multipart'),
)
