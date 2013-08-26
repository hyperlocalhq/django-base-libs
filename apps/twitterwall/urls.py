# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.twitterwall.views',
    url(r'^$', 'twitterwall', name='twitterwall_index'),
    url(r'^tweets/$', 'load_tweets', name='load_tweets'),
    url(r'^box/$', 'twitterwall_box', name='twitterwall_box'),
    url(r'^box/tweets/$', 'load_box_tweets', name='load_box_tweets'),
)
