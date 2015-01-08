# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.productions.views',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)/$', 'event_list', name='event_list_for_a_day'),
    url(r'^(?P<slug>[^/]+)/(?P<event_id>[^/]+)/$', 'event_detail', name='event_detail'),
)
