# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.twitterwall.views',
    url(r'^$', 'twitterwall', name='twitterwall_index'),
)
