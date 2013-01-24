# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.workshops.views',
    url(r'^$', 'workshop_list', name='workshop_list'),
    url(r'^add/$', 'add_workshop', name='add_workshop'),    
    url(r'^(?P<slug>[^/]+)/$', 'workshop_detail', name='workshop_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_workshop', name='change_workshop'),    
)
