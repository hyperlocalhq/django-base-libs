# -*- coding: utf-8 -*-

from django.conf.urls import *

from ccb.apps.search.forms import ModelSearchForm
from ccb.apps.search.views import SearchView
from ccb.apps.search.query import MultilingualSearchQuerySet

urlpatterns = patterns('',
                       url(
                           r'^$',
                           SearchView(
                               searchqueryset=MultilingualSearchQuerySet(),
                               limit=4,
                           ),
                           name='haystack_search'
                       ),
                       url(
                           r'^full/$',
                           SearchView(
                               searchqueryset=MultilingualSearchQuerySet(),
                           ),
                           name='haystack_full_search'
                       ),
                       )
