# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from museumsportal.apps.search.views import SearchView
from museumsportal.apps.search.query import MultilingualSearchQuerySet


urlpatterns = patterns(
    '',
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
