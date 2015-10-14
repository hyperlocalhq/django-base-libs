# -*- coding: UTF-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from haystack import indexes

from jetson.apps.image_mods.models import FileManager

Article = models.get_model("articles", "Article")
Event = models.get_model("events", "Event")
FlatPage = models.get_model("flatpages", "FlatPage")
Institution = models.get_model("institutions", "Institution")
JobOffer = models.get_model("marketplace", "JobOffer")
Person = models.get_model("people", "Person")
Document = models.get_model("resources", "Document")
Post = models.get_model("blog", "Post")
QuestionAnswer = models.get_model("faqs", "QuestionAnswer")
MediaGallery = models.get_model("media_gallery", "MediaGallery")


class QuestionAnswerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_en = indexes.CharField(use_template=True)
    text_de = indexes.CharField(use_template=True)
    title_en = indexes.CharField(model_attr="question_en")  # , boost=1.1)
    title_de = indexes.CharField(model_attr="question_de")  # , boost=1.1)
    description_en = indexes.CharField(use_template=True)
    description_de = indexes.CharField(use_template=True)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    url_path = indexes.CharField(indexed=False)
    image_path = indexes.CharField(indexed=False)

    order = 0
    short_name = "faq"
    verbose_name = _("Questions and Answers")

    def get_model(self):
        return QuestionAnswer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_url_path(self, obj):
        return obj.get_url_path()

    def prepare_image_path(self, obj):
        return settings.STATIC_URL + "site/img/website/placeholder/faqs_s.png"


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_en = indexes.CharField(use_template=True)
    text_de = indexes.CharField(use_template=True)
    title_en = indexes.CharField(model_attr="title")  # , boost=1.1)
    title_de = indexes.CharField(model_attr="title")  # , boost=1.1)
    description_en = indexes.CharField(use_template=True)
    description_de = indexes.CharField(use_template=True)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    url_path = indexes.CharField(indexed=False)
    image_path = indexes.CharField(indexed=False)

    order = 1
    short_name = "infolink"
    verbose_name = _("Infolinks")

    def get_model(self):
        return Document

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(
            status="published",
        )

    def prepare_url_path(self, obj):
        return obj.get_url_path()

    def prepare_image_path(self, obj):
        if obj.image:
            image_path = FileManager.modified_path(obj.image.path, "at")
            if image_path:
                return "%s%s" % (settings.UPLOADS_URL, image_path)
        return settings.STATIC_URL + "site/img/website/placeholder/document_s.png"


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_en = indexes.CharField(use_template=True)
    text_de = indexes.CharField(use_template=True)
    title_en = indexes.CharField(model_attr="title")  # , boost=1.1)
    title_de = indexes.CharField(model_attr="title")  # , boost=1.1)
    description_en = indexes.CharField(use_template=True)
    description_de = indexes.CharField(use_template=True)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    url_path = indexes.CharField(indexed=False)
    image_path = indexes.CharField(indexed=False)

    order = 2
    short_name = "news"
    verbose_name = _("News")

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().published_objects.all()

    def prepare_url_path(self, obj):
        return obj.get_url_path()

    def prepare_image_path(self, obj):
        if obj.image:
            image_path = FileManager.modified_path(obj.image.path, "at")
            if image_path:
                return "%s%s" % (settings.UPLOADS_URL, image_path)
        return settings.STATIC_URL + "site/img/website/placeholder/news_s.png"


class JobOfferIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_en = indexes.CharField(use_template=True)
    text_de = indexes.CharField(use_template=True)
    title_en = indexes.CharField(model_attr="position")  # , boost=1.1)
    title_de = indexes.CharField(model_attr="position")  # , boost=1.1)
    description_en = indexes.CharField(use_template=True)
    description_de = indexes.CharField(use_template=True)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    url_path = indexes.CharField(indexed=False)
    image_path = indexes.CharField(indexed=False)

    order = 3
    short_name = "job"
    verbose_name = _("Job Offers")

    def get_model(self):
        return JobOffer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().published_objects.all()

    def prepare_url_path(self, obj):
        return obj.get_url_path()

    def prepare_image_path(self, obj):
        return settings.STATIC_URL + "site/img/website/placeholder/jobs_s.png"


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_en = indexes.CharField(use_template=True)
    text_de = indexes.CharField(use_template=True)
    title_en = indexes.CharField(model_attr="title")  # , boost=1.1)
    title_de = indexes.CharField(model_attr="title")  # , boost=1.1)
    description_en = indexes.CharField(use_template=True)
    description_de = indexes.CharField(use_template=True)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    url_path = indexes.CharField(indexed=False)
    image_path = indexes.CharField(indexed=False)

    order = 4
    short_name = "event"
    verbose_name = _("Events")

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(
            status="published",
        )

    def prepare_url_path(self, obj):
        return obj.get_url_path()

    def prepare_image_path(self, obj):
        if obj.image:
            image_path = FileManager.modified_path(obj.image.path, "at")
            if image_path:
                return "%s%s" % (settings.UPLOADS_URL, image_path)
        return settings.STATIC_URL + "site/img/website/placeholder/event_s.png"


class InstitutionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_en = indexes.CharField(use_template=True)
    text_de = indexes.CharField(use_template=True)
    title_en = indexes.CharField(model_attr="title")  # , boost=1.1)
    title_de = indexes.CharField(model_attr="title")  # , boost=1.1)
    description_en = indexes.CharField(use_template=True)
    description_de = indexes.CharField(use_template=True)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    url_path = indexes.CharField(indexed=False)
    image_path = indexes.CharField(indexed=False)

    order = 5
    short_name = "institution"
    verbose_name = _("Institutions")

    def get_model(self):
        return Institution

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(
            status__in=("published", "published_commercial"),
        )

    def prepare_url_path(self, obj):
        return obj.get_url_path()

    def prepare_image_path(self, obj):
        if obj.image:
            image_path = FileManager.modified_path(obj.image.path, "at")
            if image_path:
                return "%s%s" % (settings.UPLOADS_URL, image_path)
        return settings.STATIC_URL + "site/img/website/placeholder/institution_s.png"


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_en = indexes.CharField(use_template=True)
    text_de = indexes.CharField(use_template=True)
    title_en = indexes.CharField(use_template=True)  # , boost=1.1)
    title_de = indexes.CharField(use_template=True)  # , boost=1.1)
    description_en = indexes.CharField(use_template=True)
    description_de = indexes.CharField(use_template=True)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    url_path = indexes.CharField(indexed=False)
    image_path = indexes.CharField(indexed=False)

    order = 6
    short_name = "person"
    verbose_name = _("People")

    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status="published")

    def prepare_url_path(self, obj):
        return obj.get_url_path()

    def prepare_image_path(self, obj):
        if obj.image:
            image_path = FileManager.modified_path(obj.image.path, "at")
            if image_path:
                return "%s%s" % (settings.UPLOADS_URL, image_path)
        return settings.STATIC_URL + "site/img/website/placeholder/person_s.png"


class MediaGalleryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_en = indexes.CharField(use_template=True)
    text_de = indexes.CharField(use_template=True)
    title_en = indexes.CharField(model_attr="title_en")  # , boost=1.1)
    title_de = indexes.CharField(model_attr="title_de")  # , boost=1.1)
    description_en = indexes.CharField(use_template=True)
    description_de = indexes.CharField(use_template=True)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    url_path = indexes.CharField(indexed=False)
    image_path = indexes.CharField(indexed=False)

    order = 7
    short_name = "gallery"
    verbose_name = _("Portfolios")

    def get_model(self):
        return MediaGallery

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().published_objects.all()

    def prepare_url_path(self, obj):
        return obj.get_url_path()

    def prepare_image_path(self, obj):
        if obj.cover_image:
            image_path = FileManager.modified_path(obj.cover_image.path, "at")
            if image_path:
                return "%s%s" % (settings.UPLOADS_URL, image_path)
        else:
            try:
                first_image_path = FileManager.modified_path(obj.mediafile_set.all()[0].path.path, "at")
            except Exception:
                first_image_path = False
            if first_image_path:
                return "%s%s" % (settings.UPLOADS_URL, first_image_path)
        return "%s%s" % (settings.STATIC_URL, "site/img/website/placeholder/other_content_s.png")


class FlatPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_en = indexes.CharField(use_template=True)
    text_de = indexes.CharField(use_template=True)
    title_en = indexes.CharField(model_attr="title_en")  # , boost=1.1)
    title_de = indexes.CharField(model_attr="title_de")  # , boost=1.1)
    description_en = indexes.CharField(use_template=True)
    description_de = indexes.CharField(use_template=True)
    rendered_en = indexes.CharField(use_template=True, indexed=False)
    rendered_de = indexes.CharField(use_template=True, indexed=False)
    url_path = indexes.CharField(indexed=False)
    image_path = indexes.CharField(indexed=False)

    order = 8
    short_name = "page"
    verbose_name = _("Other Content")

    def get_model(self):
        return FlatPage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().site_published_objects.all()

    def prepare_url_path(self, obj):
        return obj.get_url_path()

    def prepare_image_path(self, obj):
        return "%s%s" % (settings.STATIC_URL, "site/img/website/placeholder/other_content_s.png")


# class PostIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     text_en = indexes.CharField(use_template=True)
#     text_de = indexes.CharField(use_template=True)
#     title_en = indexes.CharField(model_attr="title")  # , boost=1.1)
#     title_de = indexes.CharField(model_attr="title")  # , boost=1.1)
#     description_en = indexes.CharField(use_template=True)
#     description_de = indexes.CharField(use_template=True)
#     rendered_en = indexes.CharField(use_template=True, indexed=False)
#     rendered_de = indexes.CharField(use_template=True, indexed=False)
#     url_path = indexes.CharField(indexed=False)
#     image_path = indexes.CharField(indexed=False)
#
#     order = 11
#     short_name = "blog_post"
#
#     def get_model(self):
#         return Post
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().published_objects.all()
#
#     def prepare_url_path(self, obj):
#         return obj.get_url_path()
#
#     def prepare_image_path(self, obj):
#         return "%s%s" % (settings.STATIC_URL, "site/img/website/placeholder/other_content_s.png")
