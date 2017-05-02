# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('berlinbuehnen.apps.services.views',
    url(r'^$', 'services', name='services'),
)
