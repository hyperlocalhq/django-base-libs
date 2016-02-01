# -*- coding: UTF-8 -*-

from django.apps import apps
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

from haystack import indexes
from aldryn_search.base import AldrynIndexBase

Article = apps.get_model("articles", "Article")
Event = apps.get_model("events", "Event")
Institution = apps.get_model("institutions", "Institution")
JobOffer = apps.get_model("marketplace", "JobOffer")
Person = apps.get_model("people", "Person")
Post = apps.get_model("blog", "Post")
Bulletin = apps.get_model("bulletin_board", "Bulletin")
MediaGallery = apps.get_model("media_gallery", "MediaGallery")


class ArticleIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 7
    short_name = "news"
    verbose_name = _("News")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        if language == "default":
            language = settings.LANGUAGE_CODE
        strings = [
            force_unicode(getattr(obj, field))
            for field in (
                "title",
                "subtitle",
                "description",
                "content",
            )
        ]
        return "\n".join(strings)

    def get_model(self):
        return Article

    def get_index_queryset(self, language=None):
        """Used when the entire index for model is updated."""
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().published_objects.filter(language=language)


class JobOfferIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 4
    short_name = "job"
    verbose_name = _("Job Offers")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.position

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        if language == "default":
            language = settings.LANGUAGE_CODE
        strings = []
        strings.append(obj.position)
        strings.append(obj.description)
        if obj.job_type:
            strings.append(getattr(obj.job_type, "title_%s" % language))
        strings += obj.get_additional_search_data()
        for cat in obj.qualifications.all():
            strings.append(getattr(cat, "title_%s" % language))
        for cat in obj.job_sectors.all():
            strings.append(getattr(cat, "title_%s" % language))
        return "\n".join(strings)

    def get_model(self):
        return JobOffer

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().published_objects.all()


class EventIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 6
    short_name = "event"
    verbose_name = _("Events")

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
        strings = [
            force_unicode(getattr(obj, field))
            for field in (
                "title_%s" % language,
                "description_%s" % language,
            )
        ]
        strings.append(obj.slug)
        strings += obj.get_additional_search_data()
        for cat in obj.get_object_types():
            strings.append(getattr(cat, "title_%s" % language))
        for cat in obj.categories.all():
            strings.append(getattr(cat, "title_%s" % language))

        return "\n".join(strings)

    def get_model(self):
        return Event

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().objects.filter(
            status="published",
        )


class InstitutionIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 1
    short_name = "institution"
    verbose_name = _("Institutions")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.get_title()

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        if language == "default":
            language = settings.LANGUAGE_CODE
        strings = []
        # collect multilingual data
        strings.append(obj.get_title())
        strings += [
            force_unicode(getattr(obj, field))
            for field in (
                "description_%s" % language,
            )
        ]
        strings += obj.get_additional_search_data()
        for cat in obj.get_object_types():
            strings.append(getattr(cat, "title_%s" % language))
        for cat in obj.categories.all():
            strings.append(getattr(cat, "title_%s" % language))

        return "\n".join(strings)

    def get_model(self):
        return Institution

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().objects.filter(
            status__in=("published", "published_commercial"),
        )


class PersonIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 2
    short_name = "person"
    verbose_name = _("People")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.get_title()

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        if language == "default":
            language = settings.LANGUAGE_CODE
        strings = []
        strings.append(obj.user.get_full_name())
        strings.append(obj.user.username)
        strings.append(obj.user.email)
        # collect multilingual data
        strings += [
            force_unicode(getattr(obj, field))
            for field in (
                "description_%s" % language,
            )
        ]
        strings += obj.get_additional_search_data()
        for cat in obj.get_object_types():
            strings.append(getattr(cat, "title_%s" % language))
        for cat in obj.categories.all():
            strings.append(getattr(cat, "title_%s" % language))

        return u"\n".join(strings)

    def get_model(self):
        return Person

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().objects.filter(status="published")


class MediaGalleryIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 3
    short_name = "gallery"
    verbose_name = _("Portfolios")

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
        strings = [
            force_unicode(getattr(obj, field))
            for field in (
                "title_%s" % language,
                "description_%s" % language,
                "content_object_repr_%s" % language,
            )
        ]
        return "\n".join(strings)

    def get_model(self):
        return MediaGallery

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().published_objects.all()


class PostIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 8
    short_name = "blog_post"
    verbose_name = _("Blog Posts")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.body

    def get_search_data(self, obj, language, request):
        if language == "default":
            language = settings.LANGUAGE_CODE
        strings = [
            force_unicode(getattr(obj, field))
            for field in (
                "title",
                "body",
                "tags",
            )
        ]
        return "\n".join(strings)

    def get_model(self):
        return Post

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().published_objects.all()


class BulletinIndex(AldrynIndexBase, indexes.Indexable):
    INDEX_TITLE = True
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 5
    short_name = "bulletin"
    verbose_name = _("Bulletin Board")

    def get_url(self, obj):
        return obj.get_url()

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description

    def get_search_data(self, obj, language, request):
        if language == "default":
            language = settings.LANGUAGE_CODE
        strings = [
            force_unicode(getattr(obj, field))
            for field in (
                "title",
                "description",
                "contact_person",
                "institution_title",
            )
        ]
        if obj.institution:
            strings.append(obj.institution.title)
        if obj.bulletin_category:
            strings.append(getattr(obj.bulletin_category, "title_%s" % language))
        for cat in obj.categories.all():
            strings.append(getattr(cat, "title_%s" % language))

        return "\n".join(strings)

    def get_model(self):
        return Bulletin

    def get_index_queryset(self, language=None):
        if language == "default":
            return self.get_model().objects.none()
        return self.get_model().objects.filter(status="published")


class CMSPageIndexBase(AldrynIndexBase):
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)

    order = 9
    short_name = "page"
    verbose_name = _("Editorial Content")
