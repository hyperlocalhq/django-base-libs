# -*- coding: UTF-8 -*-

from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.twitterwall, name='twitterwall_index'),
    url(r'^tweets/$', views.load_tweets, name='load_tweets'),
    url(r'^box/$', views.twitterwall_box, name='twitterwall_box'),
    url(r'^box/tweets/$', views.load_box_tweets, name='load_box_tweets'),
]
