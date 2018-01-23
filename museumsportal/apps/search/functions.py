# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from haystack import connections
from haystack.exceptions import NotHandled

from base_libs.middleware import get_current_language


def get_search_indexes(language):
    """
    A generator, returning an iterable of model and index tuples for all searchable models
    :param language: language code of the current language
    :return: like ((Museum, MuseumIndex), (Exhibition, ExhibitionIndex), ...)
    """
    unified_index = connections[language].get_unified_index()
    for model in models.get_models():
        try:
            index = unified_index.get_index(model)
        except NotHandled:
            pass
        else:
            yield model, index


class DictionaryCache(object):
    models = {}  # like {'museums.museum': 'museums'}
    indexes = {}  # like {'museums': 'museums.museum'}

    def __call__(self):
        if not self.models and not self.indexes:
            language = get_current_language()
            for model, index in get_search_indexes(language):
                model_str = "%s.%s" % (model._meta.app_label, model._meta.module_name)
                self.models[model_str] = getattr(index, "short_name", "other")
                self.indexes[self.models[model_str]] = model_str
        return self.models, self.indexes

get_dictionaries = DictionaryCache()


def get_model_short_name(name):
    short_model_names, indexes = get_dictionaries()
    return short_model_names[name]


def get_model_from_short_name(name):
    short_model_names, indexes = get_dictionaries()
    return indexes[name]


class ModelChoiceCache(object):
    """
    Model choices used in the search form
    """
    sorted_models = []  # like [('museums.museum', 'Museums'), ('exhibitions.exhibition', 'Exhibitions'),...]
    model_list = []

    def __call__(self, site=None):
        if not self.model_list:
            language = get_current_language()

            self.model_list = sorted([
                (m, getattr(k, "verbose_name", _("Other Content")), getattr(k, "order", 10))
                for m, k in get_search_indexes(language)
            ], key=lambda x: x[2])

        self.sorted_models = [
            (
                get_model_short_name("%s.%s" % (m[0]._meta.app_label, m[0]._meta.module_name)),
                capfirst(unicode(m[1])),
            )
            for m in self.model_list
        ]

        return self.sorted_models

model_choices = ModelChoiceCache()
