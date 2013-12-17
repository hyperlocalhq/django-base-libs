# -*- coding: UTF-8 -*-

from django.conf import settings
from django.utils.translation import get_language

from haystack.query import SearchQuerySet, DEFAULT_OPERATOR
from haystack.views import SearchView


class MultilingualSearchQuerySet(SearchQuerySet):
    def auto_query(self, query_string):
        return self.filter(content=self.query.clean(query_string))

    def filter(self, **kwargs):
        """Narrows the search based on certain attributes and the default operator."""
        if 'content' in kwargs:
            kwd = kwargs.pop('content')
            kwdkey = "text_%s" % str(get_language()[:2])
            kwargs[kwdkey] = kwd
        if getattr(settings, 'HAYSTACK_DEFAULT_OPERATOR', DEFAULT_OPERATOR) == 'OR':
            return self.filter_or(**kwargs)
        else:
            return self.filter_and(**kwargs)


