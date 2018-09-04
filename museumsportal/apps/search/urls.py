# -*- coding: utf-8 -*-

from django.conf.urls import *

from museumsportal.apps.search.views import SearchView
from museumsportal.apps.search.query import MultilingualSearchQuerySet


urlpatterns = [
    url(
        r'^$',
        SearchView(
            load_all=False,
            searchqueryset=MultilingualSearchQuerySet(),
            limit=4,
        ),
        name='haystack_search'
    ),
    url(
        r'^full/$',
        SearchView(
            load_all=False,
            searchqueryset=MultilingualSearchQuerySet(),
        ),
        name='haystack_full_search'
    ),
]