# -*- coding: UTF-8 -*-
import os
import re
import sys
from datetime import datetime, date

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields import FieldDoesNotExist

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.utils.encoding import force_unicode
from django.conf import settings
from django.utils.timezone import now as tz_now
from django.apps import apps

from base_libs.models.models import UrlMixin
from base_libs.models import CreationModificationDateMixin
from base_libs.models.models import SlugMixin
from base_libs.utils.misc import get_unique_value
from base_libs.utils.misc import get_website_url
from base_libs.utils.betterslugify import better_slugify
from base_libs.middleware import get_current_language
from base_libs.middleware import get_current_user
from base_libs.models.query import ExtendedQuerySet
from base_libs.models.fields import PlainTextModelField
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField  # for south

from filebrowser.fields import FileBrowseField

from jetson.apps.structure.models import Term
from jetson.apps.structure.models import ContextCategory
from jetson.apps.structure.models import Category
from jetson.apps.i18n.models import Language
from jetson.apps.utils.models import MONTH_CHOICES
from jetson.apps.image_mods.models import FileManager

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

verbose_name = _("Resources")

### Document class ###

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('published_commercial', _("Published-Commercial")),
    ('not_listed', _("Not Listed")),
)

YEAR_OF_PUBLISHING_CHOICES = [
    (i, i) for i in range(tz_now().year - 10,
                          tz_now().year + 10)
]

DAY_CHOICES = [(i, i) for i in range(1, 32)]

URL_ID_DOCUMENT = getattr(settings, "URL_ID_DOCUMENT", "document")
URL_ID_DOCUMENTS = getattr(settings, "URL_ID_DOCUMENTS", "documents")
DEFAULT_LOGO_4_DOCUMENT = getattr(
    settings,
    "DEFAULT_LOGO_4_DOCUMENT",
    "%ssite/img/website/placeholder/document.png" % settings.STATIC_URL,
)
DEFAULT_FORM_LOGO_4_DOCUMENT = getattr(
    settings,
    "DEFAULT_FORM_LOGO_4_DOCUMENT",
    "%ssite/img/website/placeholder/document_f.png" % settings.STATIC_URL,
)
DEFAULT_SMALL_LOGO_4_DOCUMENT = getattr(
    settings,
    "DEFAULT_SMALL_LOGO_4_DOCUMENT",
    "%ssite/img/website/placeholder/document_s.png" % settings.STATIC_URL,
)


class Medium(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Medium")
        verbose_name_plural = _("Mediums")


class DocumentType(MPTTModel, SlugMixin()):
    sort_order = models.IntegerField(
        _("sort order"),
        blank=True,
        editable=False,
        default=0,
    )
    parent = TreeForeignKey(
        'self',
        #related_name="%(class)s_children",
        related_name="child_set",
        blank=True,
        null=True,
    )
    title = MultilingualCharField(_('title'), max_length=255)

    objects = TreeManager()

    class Meta:
        verbose_name = _("document type")
        verbose_name_plural = _("document types")
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __unicode__(self):
        return self.title

    def get_title(self, prefix="", postfix=""):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            DocumentType.objects.insert_node(self, self.parent)
        super(DocumentType, self).save(*args, **kwargs)


class DocumentManager(models.Manager):
    """
    for comments, see institutions.InstitutionManager
    """

    def get_queryset(self):
        return ExtendedQuerySet(self.model)

    def _get_title_fields(self, prefix=''):
        language = get_current_language()
        if language and language != 'en':
            return ["%stitle_%s" % (prefix, language), "%stitle" % prefix]
        else:
            return ["%stitle" % prefix]

    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'creation_date_desc': (
                1,
                _('Creation date'),
                ['-creation_date'],
            ),
            'alphabetical_asc':
                (
                    2,
                    _('Alphabetical'),
                    self._get_title_fields(),
                ),
        }
        return sort_order_mapper

    def latest_published(self):
        return self.filter(
            status__in=("published", "published_commercial"),
        ).order_by("-creation_date")


class DocumentBase(CreationModificationDateMixin, UrlMixin):
    """
    The base class for the document. Wherever document is located - jetson or site-specific project - it should be in an app called "resources" and it should be called "Document"
    """

    title = MultilingualCharField(_("Title"), max_length=255)
    slug = models.CharField(_("Slug"), max_length=255)
    description = MultilingualTextField(_("Description"), blank=True)
    document_type = TreeForeignKey(
        DocumentType,
        verbose_name=_("Document type"),
        related_name="type_documents"
    )
    medium = models.ForeignKey(
        Medium,
        verbose_name=_("Medium"),
        blank=True,
        null=True,
        related_name="medium_documents"
    )
    url_link = URLField(_("URL"), blank=True)
    document_file = FileBrowseField(
        _('Document file'), max_length=255, blank=True
    )
    authors = models.ManyToManyField(
        "people.Person",
        verbose_name=_("Authors"),
        blank=True,
        related_name="author_documents"
    )
    authors_plain = PlainTextModelField(
        _("External authors"),
        help_text=_("Comma-separated list"),
        blank=True,
        max_length=255
    )
    publisher = models.ForeignKey(
        "institutions.Institution",
        verbose_name=_("Publisher"),
        blank=True,
        null=True
    )
    published_yyyy = models.IntegerField(
        _("Year of Publishing"),
        blank=True,
        null=True,
        choices=YEAR_OF_PUBLISHING_CHOICES
    )
    published_mm = models.SmallIntegerField(
        _("Month of Publishing"), blank=True, null=True, choices=MONTH_CHOICES
    )
    published_dd = models.SmallIntegerField(
        _("Day of Publishing"), blank=True, null=True, choices=DAY_CHOICES
    )
    playing_time = models.TimeField(_("Playing time"), blank=True, null=True)
    isbn10 = models.CharField(_("ISBN-10"), max_length=13, blank=True)
    isbn13 = models.CharField(_("ISBN-13"), max_length=17, blank=True)
    pages = models.PositiveIntegerField(
        _("Pages"), default=0, blank=True, null=True
    )
    file_size = models.PositiveIntegerField(
        _("File size (MB)"), default=0, blank=True, null=True
    )
    languages = models.ManyToManyField(
        Language,
        verbose_name=_("Languages"),
        limit_choices_to={'display': True},
        blank=True
    )

    context_categories = TreeManyToManyField(
        ContextCategory,
        verbose_name=_("Context categories"),
        limit_choices_to={'is_applied4document': True},
        blank=True
    )

    image = FileBrowseField(
        _('Image'),
        max_length=255,
        directory="%s/" % URL_ID_DOCUMENTS,
        extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
        blank=True
    )

    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        default="draft"
    )

    row_level_permissions = True

    objects = DocumentManager()

    class Meta:
        abstract = True
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ['title', 'creation_date']

    def __unicode__(self):
        return force_unicode(self.get_title())

    def is_document(self):
        return True

    def get_slug(self):
        return self.slug

    def has_maps(self):
        return False

    def has_photos(self):
        return False

    def has_videos(self):
        return False

    def get_title(self, language=None):
        language = language or get_current_language()
        return getattr(self, "title_%s" % language, "") or self.title

    get_title = lazy(get_title, unicode)

    def get_description(self, language=None):
        language = language or get_current_language()
        return mark_safe(
            getattr(self, "description_%s" % language, "") or self.description
        )

    def get_absolute_url(self):
        return "%s/%s/%s/" % (get_website_url(), URL_ID_DOCUMENT, self.slug)

    def get_url_path(self):
        return "/%s/%s/" % (URL_ID_DOCUMENT, self.slug)

    def get_context_categories(self):
        return self.context_categories.all()

    def get_languages(self):
        return Language.objects.distinct().extra(
            tables=['resources_document_languages'],
            where=[
                'i18n_language.id=resources_document_languages.language_id',
                'resources_document_languages.document_id=%d' % (self.id or 0)
            ],
        )

    def get_authors(self):
        Person = apps.get_model("people", "Person")
        person_db_table = Person._meta.db_table
        return Person.objects.distinct().extra(
            tables=['resources_document_authors'],
            where=[
                '%s.id=resources_document_authors.person_id' % person_db_table,
                'resources_document_authors.document_id=%d' % (self.id or 0)
            ],
        )

    def get_published_date(self):
        if not hasattr(self, "_published_date_cache"):
            try:
                self._published_date_cache = date(
                    self.published_yyyy,
                    self.published_mm,
                    self.published_dd,
                )
            except:
                self._published_date_cache = None
        return self._published_date_cache

    def get_object_types(self):
        return self.document_type and [self.document_type] or []

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title
        self.slug = get_unique_value(
            type(self),
            better_slugify(self.slug),
            separator="-",
            instance_pk=self.id
        )
        if hasattr(self, "title_en") and not self.title_en:
            self.title_en = self.title_de
        super(DocumentBase, self).save(*args, **kwargs)

    save.alters_data = True

    def delete(self, *args, **kwargs):
        FileManager.delete_file(self.get_filebrowser_dir())
        super(DocumentBase, self).delete(*args, **kwargs)

    delete.alters_data = True

    def is_claimable(self, user=None):
        user = get_current_user(user)
        return True

    def get_filebrowser_dir(self):
        return "%s/%s/" % (
            URL_ID_DOCUMENTS,
            self.slug,
        )
