# -*- coding: UTF-8 -*-
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.utils.html import decode_entities

from haystack import indexes
from aldryn_search.base import AldrynIndexBase

from museumsportal.apps.museums.models import Museum
from museumsportal.apps.exhibitions.models import Exhibition
from museumsportal.apps.events.models import Event
from museumsportal.apps.workshops.models import Workshop


class CMSPageIndexBase(AldrynIndexBase):
    order = 3
    short_name = "pages"
    verbose_name = _("Editorial Content")
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    rendered_fr = indexes.CharField(use_template=True, indexed=False)
    rendered_pl = indexes.CharField(use_template=True, indexed=False)
    rendered_tr = indexes.CharField(use_template=True, indexed=False)
    rendered_es = indexes.CharField(use_template=True, indexed=False)
    rendered_it = indexes.CharField(use_template=True, indexed=False)


class MuseumIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    rendered_fr = indexes.CharField(use_template=True, indexed=False)
    rendered_pl = indexes.CharField(use_template=True, indexed=False)
    rendered_tr = indexes.CharField(use_template=True, indexed=False)
    rendered_es = indexes.CharField(use_template=True, indexed=False)
    rendered_it = indexes.CharField(use_template=True, indexed=False)

    order = 1
    short_name = "museums"
    verbose_name = _("Museums")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        # collect multilingual data
        all_text = u"\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "title_%s" % language,
                "subtitle_%s" % language,
                "description_%s" % language,
                "search_keywords_%s" % language,
            )
        )
        all_text = decode_entities(all_text)
        if obj.parent:
            all_text += u"\n" + getattr(obj.parent, "title_%s" % language)

        # collect non multilingual data
        non_multilingual_data = "\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "street_address",
                "tags",
            )
        )
        return all_text + "\n" + non_multilingual_data

    def get_model(self):
        return Museum

    def get_index_queryset(self, language=None):
        return self.get_model().objects.filter(status="published")
        

class ExhibitionIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True

    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    rendered_fr = indexes.CharField(use_template=True, indexed=False)
    rendered_pl = indexes.CharField(use_template=True, indexed=False)
    rendered_tr = indexes.CharField(use_template=True, indexed=False)
    rendered_es = indexes.CharField(use_template=True, indexed=False)
    rendered_it = indexes.CharField(use_template=True, indexed=False)

    order = 2
    short_name = "exhibitions"
    verbose_name = _("Exhibitions")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        # collect multilingual data
        all_text = u"\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "title_%s" % language,
                "subtitle_%s" % language,
                "teaser_%s" % language,
                "description_%s" % language,
                "press_text_%s" % language,
                "catalog_%s" % language,
                "search_keywords_%s" % language,
            )
        )
        all_text = decode_entities(all_text)
        if obj.museum:
            all_text += u"\n" + getattr(obj.museum, "title_%s" % language)

        # collect non multilingual data
        non_multilingual_data = "\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "location_name",
                "street_address",
                "tags",
            )
        )
        # set text of both languages
        return all_text + "\n" + non_multilingual_data

    def get_model(self):
        return Exhibition

    def get_index_queryset(self, language=None):
        return self.get_model().objects.filter(status="published")
        

class EventIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True

    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    rendered_fr = indexes.CharField(use_template=True, indexed=False)
    rendered_pl = indexes.CharField(use_template=True, indexed=False)
    rendered_tr = indexes.CharField(use_template=True, indexed=False)
    rendered_es = indexes.CharField(use_template=True, indexed=False)
    rendered_it = indexes.CharField(use_template=True, indexed=False)

    order = 4
    short_name = "events"
    verbose_name = _("Events")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        # collect multilingual data
        all_text = u"\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "title_%s" % language,
                "subtitle_%s" % language,
                "event_type_%s" % language,
                "description_%s" % language,
                "search_keywords_%s" % language,
            )
        )
        all_text = decode_entities(all_text)
        if obj.museum:
            for lang_code, lang_name in settings.LANGUAGES:
                all_text += u"\n" + getattr(obj.museum, "title_%s" % language)

        # collect non multilingual data
        non_multilingual_data = "\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "location_name",
                "street_address",
                "tags",
            )
        )

        # set text of both languages
        return all_text + "\n" + non_multilingual_data

    def get_model(self):
        return Event

    def get_index_queryset(self, language=None):
        return self.get_model().objects.filter(status="published")
        

class WorkshopIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True

    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    rendered_fr = indexes.CharField(use_template=True, indexed=False)
    rendered_pl = indexes.CharField(use_template=True, indexed=False)
    rendered_tr = indexes.CharField(use_template=True, indexed=False)
    rendered_es = indexes.CharField(use_template=True, indexed=False)
    rendered_it = indexes.CharField(use_template=True, indexed=False)

    order = 5
    short_name = "workshops"
    verbose_name = _("Guided Tours")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        # collect multilingual data
        all_text = u"\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "title_%s" % language,
                "subtitle_%s" % language,
                "workshop_type_%s" % language,
                "description_%s" % language,
                "search_keywords_%s" % language,
            )
        )
        all_text = decode_entities(all_text)
        if obj.museum:
            for lang_code, lang_name in settings.LANGUAGES:
                all_text += u"\n" + getattr(obj.museum, "title_%s" % language)

        # collect non multilingual data
        non_multilingual_data = "\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "location_name",
                "street_address",
                "tags",
            )
        )

        # set text of both languages
        return all_text + "\n" + non_multilingual_data

    def get_model(self):
        return Workshop

    def get_index_queryset(self, language=None):
        return self.get_model().objects.filter(status="published")
