# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('ruhrbuehnen.apps.services.views',
    url(r'^$', 'services', name='services'),
)
