# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.twitterwall.views',
    url(r'^$', 'twitterwall', name='twitterwall_index'),
    url(r'^tweets/$', 'load_tweets', name='load_tweets'),
)
