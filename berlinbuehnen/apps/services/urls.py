# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.productions.views.productions',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^add/$', 'add_production', name='add_production'),
    url(r'^(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)/$', 'event_list', name='event_list_for_a_day'),
    url(r'^(?P<slug>[^/]+)/$', 'event_detail', name='production_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_production', name='change_production'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_production', name='delete_production'),
    url(r'^(?P<slug>[^/]+)/status/$', 'change_production_status', name='change_production_status'),
    url(r'^(?P<slug>[^/]+)/duplicate/$', 'duplicate_production', name='duplicate_production'),
)
