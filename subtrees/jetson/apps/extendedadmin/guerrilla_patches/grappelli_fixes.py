# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from grappelli.views import related


def _get_searched_queryset(self, qs):
    import operator
    from django.db import models
    from django.db.models.query import QuerySet
    from django.utils.encoding import smart_text
    AUTOCOMPLETE_SEARCH_FIELDS = related.AUTOCOMPLETE_SEARCH_FIELDS

    model = self.model
    term = self.GET["term"]

    try:
        term = model.autocomplete_term_adjust(term)
    except AttributeError:
        pass

    try:
        search_fields = model.autocomplete_search_fields()
    except AttributeError:
        try:
            search_fields = AUTOCOMPLETE_SEARCH_FIELDS[model._meta.app_label][
                model._meta.model_name]
        except KeyError:
            search_fields = ()

    if search_fields:
        for word in term.split():
            search = [
                models.Q(**{smart_text(item): smart_text(word)})
                for item in search_fields
            ]
            search_qs = QuerySet(model)
            search_qs.query.select_related = qs.query.select_related
            search_qs = search_qs.filter(reduce(operator.or_, search))
            qs &= search_qs
    else:
        qs = model.objects.none()
    return qs


related.AutocompleteLookup.get_searched_queryset = _get_searched_queryset
