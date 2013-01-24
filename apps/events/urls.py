# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.events.views',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^add/$', 'add_event', name='add_event'),    
    url(r'^(?P<slug>[^/]+)/$', 'event_detail', name='event_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_event', name='change_event'),    
)
