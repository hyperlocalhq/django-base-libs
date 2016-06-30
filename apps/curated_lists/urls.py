# -*- coding: UTF-8 -*-

from django.conf.urls import *

urlpatterns = patterns('ccb.apps.curated_lists.views',
    url(r'^$', 'featured_curated_lists', name='featured_curated_lists'),
)
