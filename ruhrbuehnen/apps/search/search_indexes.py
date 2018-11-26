# -*- coding: UTF-8 -*-
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from haystack import indexes
from aldryn_search.base import AldrynIndexBase

from ruhrbuehnen.apps.productions.models import Production
from ruhrbuehnen.apps.festivals.models import Festival
from ruhrbuehnen.apps.locations.models import Location


class CMSPageIndexBase(AldrynIndexBase):
    def get_model(self):
        pass

    order = 4
    short_name = "pages"
    verbose_name = _("Editorial Content")
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)


class LocationIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 3
    short_name = "locations"
    verbose_name = _("Locations")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        if language == "default":
            language = settings.LANGUAGE_CODE
        # collect multilingual data
        all_text = u"\n".join(
            force_unicode(getattr(obj, field)) for field in (
                "title_%s" % language,
                "subtitle_%s" % language,
                "description_%s" % language,
                "teaser_%s" % language,
                "tickets_calling_prices_%s" % language,
                "tickets_additional_info_%s" % language,
            )
        )

        # collect non multilingual data
        non_multilingual_data = u"\n".join(
            force_unicode(getattr(obj, field)) for field in (
                "street_address",
                "street_address2",
                "tickets_street_address",
                "tickets_street_address2",
                "press_contact_name",
            )
        )
        return all_text + "\n" + non_multilingual_data

    def get_model(self):
        return Location

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().objects.filter(status="published")


class ProductionIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True

    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 1
    short_name = "productions"
    verbose_name = _("Productions")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        if language == "default":
            language = settings.LANGUAGE_CODE
        extra = []
        for location in obj.in_program_of.all():
            extra.append(location.title)
        for location in obj.play_locations.all():
            extra.append(location.title)
        for stage in obj.play_stages.all():
            extra.append(stage.title)
        # collect multilingual data
        all_text = u"\n".join(
            force_unicode(getattr(obj, field)) for field in (
                "prefix_%s" % language,
                "title_%s" % language,
                "subtitle_%s" % language,
                "original_%s" % language,
                "description_%s" % language,
                "teaser_%s" % language,
                "work_info_%s" % language,
                "contents_%s" % language,
                "press_text_%s" % language,
                "credits_%s" % language,
                "concert_program_%s" % language,
                "supporting_program_%s" % language,
                "remarks_%s" % language,
                "duration_text_%s" % language,
                "subtitles_text_%s" % language,
                "age_text_%s" % language,
                "price_information_%s" % language,
                "other_characteristics_%s" % language,
            )
        )

        # collect non multilingual data
        non_multilingual_data = u"\n".join(
            force_unicode(getattr(obj, field)) for field in (
                "ensembles",
                "organizers",
                "in_cooperation_with",
                "location_title",
                "street_address",
                "street_address2",
            )
        )

        event_multilingual_data = []
        event_non_multilingual_data = []
        for event in obj.get_upcoming_occurrences():
            for location in event.play_locations.all():
                extra.append(location.title)
            for stage in event.play_stages.all():
                extra.append(stage.title)
            event_multilingual_data = u"\n".join(
                force_unicode(getattr(obj, field)) for field in (
                    "description_%s" % language,
                    "teaser_%s" % language,
                    "work_info_%s" % language,
                    "contents_%s" % language,
                    "press_text_%s" % language,
                    "credits_%s" % language,
                    "concert_program_%s" % language,
                    "supporting_program_%s" % language,
                    "remarks_%s" % language,
                    "duration_text_%s" % language,
                    "subtitles_text_%s" % language,
                    "age_text_%s" % language,
                    "price_information_%s" % language,
                    "other_characteristics_%s" % language,
                )
            )

            # collect non multilingual data
            event_non_multilingual_data = u"\n".join(
                force_unicode(getattr(obj, field)) for field in (
                    "organizers",
                    "location_title",
                    "street_address",
                    "street_address2",
                )
            )

        # set text of both languages
        return (
            all_text + "\n" + non_multilingual_data + "\n" +
            "\n".join(event_multilingual_data) + "\n" +
            "\n".join(event_non_multilingual_data) + "\n" + "\n".join(extra)
        )

    def get_model(self):
        return Production

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().objects.filter(status="published")


class FestivalIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 2
    short_name = "festivals"
    verbose_name = _("Festivals")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        if language == "default":
            language = settings.LANGUAGE_CODE
        extra = []
        for location in obj.organizers.all():
            extra.append(location.title)
        # collect multilingual data
        all_text = u"\n".join(
            force_unicode(getattr(obj, field)) for field in (
                "title_%s" % language,
                "subtitle_%s" % language,
                "description_%s" % language,
            )
        )

        # collect non multilingual data
        non_multilingual_data = u"\n".join(
            force_unicode(getattr(obj, field)) for field in (
                "street_address",
                "street_address2",
                "tickets_street_address",
                "tickets_street_address2",
                "press_contact_name",
            )
        )
        return all_text + "\n" + non_multilingual_data + "\n" + "\n".join(extra)

    def get_model(self):
        return Festival

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().objects.filter(status="published")
