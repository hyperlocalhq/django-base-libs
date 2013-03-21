# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.encoding import force_unicode
from django.conf import settings

from base_libs.templatetags.base_tags import decode_entities

from haystack import indexes, site
from cms_search.search_helpers.indexes import MultiLanguageIndex

Museum = models.get_model("museums", "Museum")
Exhibition = models.get_model("exhibitions", "Exhibition")
Event = models.get_model("events", "Event")
Workshop = models.get_model("workshops", "Workshop")

class MuseumIndex(MultiLanguageIndex):
    text = indexes.CharField(document=True, use_template=False)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    class HaystackTrans:
        fields = ()
        
    def prepare(self, obj):
        self.prepared_data = super(MuseumIndex, self).prepare(obj)
        # collect multilingual data
        all_text = ""
        for lang_code, lang_name in settings.LANGUAGES:
            text = "\n".join(
                force_unicode(getattr(obj, field))
                for field in (
                    "title_%s" % lang_code,
                    "subtitle_%s" % lang_code,
                    "description_%s" % lang_code,
                    "press_text_%s" % lang_code,
                    )
                )
            text = decode_entities(text)
            all_text += text
        if obj.parent:
            for lang_code, lang_name in settings.LANGUAGES:
                all_text += "\n" + getattr(obj.parent, "title_%s" % lang_code)

        # collect non multilingual data
        non_multilingual_data = "\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "street_address",
                )
            )

        # set text of both languages
        self.prepared_data['text'] = all_text + "\n" + non_multilingual_data
        return self.prepared_data
        
    def get_queryset(self):
        return Museum.objects.filter(status="published")
        
site.register(Museum, MuseumIndex)

class ExhibitionIndex(MultiLanguageIndex):
    text = indexes.CharField(document=True, use_template=False)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    class HaystackTrans:
        fields = ()
        
    def prepare(self, obj):
        self.prepared_data = super(ExhibitionIndex, self).prepare(obj)
        # collect multilingual data
        all_text = ""
        for lang_code, lang_name in settings.LANGUAGES:
            text = "\n".join(
                force_unicode(getattr(obj, field))
                for field in (
                    "title_%s" % lang_code,
                    "subtitle_%s" % lang_code,
                    "teaser_%s" % lang_code,
                    "description_%s" % lang_code,
                    "press_text_%s" % lang_code,
                    "catalog_%s" % lang_code,
                    )
                )
            text = decode_entities(text)
            all_text += text
        if obj.museum:
            for lang_code, lang_name in settings.LANGUAGES:
                all_text += "\n" + getattr(obj.museum, "title_%s" % lang_code)

        # collect non multilingual data
        non_multilingual_data = "\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "location_name",
                "street_address",
                )
            )

        # set text of both languages
        self.prepared_data['text'] = all_text + "\n" + non_multilingual_data
        return self.prepared_data
        
    def get_queryset(self):
        return Exhibition.objects.filter(status="published")
        
site.register(Exhibition, ExhibitionIndex)

class EventIndex(MultiLanguageIndex):
    text = indexes.CharField(document=True, use_template=False)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    class HaystackTrans:
        fields = ()
        
    def prepare(self, obj):
        self.prepared_data = super(EventIndex, self).prepare(obj)
        # collect multilingual data
        all_text = ""
        for lang_code, lang_name in settings.LANGUAGES:
            text = "\n".join(
                force_unicode(getattr(obj, field))
                for field in (
                    "title_%s" % lang_code,
                    "subtitle_%s" % lang_code,
                    "event_type_%s" % lang_code,
                    "description_%s" % lang_code,
                    )
                )
            text = decode_entities(text)
            all_text += text
        if obj.museum:
            for lang_code, lang_name in settings.LANGUAGES:
                all_text += "\n" + getattr(obj.museum, "title_%s" % lang_code)

        # collect non multilingual data
        non_multilingual_data = "\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "location_name",
                "street_address",
                )
            )

        # set text of both languages
        self.prepared_data['text'] = all_text + "\n" + non_multilingual_data
        return self.prepared_data
        
    def get_queryset(self):
        return Event.objects.filter(status="published")
        
site.register(Event, EventIndex)

class WorkshopIndex(MultiLanguageIndex):
    text = indexes.CharField(document=True, use_template=False)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    class HaystackTrans:
        fields = ()
        
    def prepare(self, obj):
        self.prepared_data = super(WorkshopIndex, self).prepare(obj)
        # collect multilingual data
        all_text = ""
        for lang_code, lang_name in settings.LANGUAGES:
            text = "\n".join(
                force_unicode(getattr(obj, field))
                for field in (
                    "title_%s" % lang_code,
                    "subtitle_%s" % lang_code,
                    "workshop_type_%s" % lang_code,
                    "description_%s" % lang_code,
                    )
                )
            text = decode_entities(text)
            all_text += text
        if obj.museum:
            for lang_code, lang_name in settings.LANGUAGES:
                all_text += "\n" + getattr(obj.museum, "title_%s" % lang_code)

        # collect non multilingual data
        non_multilingual_data = "\n".join(
            force_unicode(getattr(obj, field))
            for field in (
                "location_name",
                "street_address",
                )
            )

        # set text of both languages
        self.prepared_data['text'] = all_text + "\n" + non_multilingual_data
        return self.prepared_data
        
    def get_queryset(self):
        return Workshop.objects.filter(status="published")
        
site.register(Workshop, WorkshopIndex)

