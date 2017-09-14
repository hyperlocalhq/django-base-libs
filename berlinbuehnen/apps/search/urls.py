# -*- coding: utf-8 -*-

from django.conf.urls import *

from .views import SearchView
from .query import MultilingualSearchQuerySet


urlpatterns = patterns(
    '',
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
)
