# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.utils.functional import LazyObject


class SearchResults(LazyObject):
    def _setup(self):
        pass

    def __init__(self, search_object):
        super(SearchResults, self).__init__()
        self._wrapped = search_object

    def __len__(self):
        return self._wrapped.count()

    def __getitem__(self, index):
        search_results = self._wrapped[index]
        if isinstance(index, slice):
            search_results = list(search_results)
        return search_results
