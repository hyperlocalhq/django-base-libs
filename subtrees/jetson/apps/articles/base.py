# -*- coding: UTF-8 -*-
import sys

from django.db import models

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.conf import settings

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import PublishingMixin
from base_libs.models.models import ViewsMixin
from base_libs.models.models import HierarchyMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField
from base_libs.utils.misc import get_website_url
from base_libs.utils.misc import html_to_plain_text
from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED
from base_libs.middleware import get_current_language

from filebrowser.fields import FileBrowseField
from filebrowser.settings import MEDIA_ROOT as UPLOADS_ROOT
from filebrowser.settings import MEDIA_URL as UPLOADS_URL

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey

verbose_name = _("Articles")

URL_ID_ARTICLES = getattr(
    settings,
    "URL_ID_ARTICLES",
    "articles",
)


class ArticleTypeBase(
    MPTTModel, CreationModificationDateMixin, UrlMixin, SlugMixin()
):
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
    title = MultilingualCharField(_('title'), max_length=512)

    objects = TreeManager()

    class Meta:
        abstract = True
        verbose_name = _('Article Type')
        verbose_name_plural = _('Article Types')
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __unicode__(self):
        return force_unicode(self.title)

    __unicode__.admin_order_field = 'path'

    def get_url_path(self):
        return "%s/" % self.slug


class ArticleManager(models.Manager):
    def latest_published(self):
        return self.model.published_objects.order_by("-published_from")

    def featured_published(self):
        return self.model.published_objects.filter(
            is_featured=True,
        ).order_by("-published_from")


def guess_language_code(*args):
    """
    Takes a bunch of values and checks what language is probably used there
    from all settings.LANGUAGES
    """
    from guess_language import guessLanguageTag
    lang_dict = dict(((t[0], 0) for t in settings.LANGUAGES))
    # check how often each language is guessed
    for v in args:
        v = html_to_plain_text(v)
        guessed_code = guessLanguageTag(v)
        if guessed_code in lang_dict:
            lang_dict[guessed_code] += 1
    # consider the most often guess as the most probable language
    most_likely = sorted(lang_dict.items(), key=lambda x: x[1], reverse=True)
    return most_likely[0][0]


class ArticleBase(
    CreationModificationDateMixin, PublishingMixin, ViewsMixin, UrlMixin,
    SlugMixin()
):
    """
    Abstract model to be extended by a model called "Article" in the models.py
    """

    article_type = TreeForeignKey(
        "articles.ArticleType", verbose_name=_("Type"), blank=True, null=True
    )
    title = models.CharField(_('title'), max_length=255, default="")
    subtitle = models.CharField(
        _('subtitle'), max_length=255, blank=True, default=""
    )
    description = ExtendedTextField(_('summary'), blank=True, default="")
    content = ExtendedTextField(_('entry'), default="")
    image_title = models.CharField(
        _('image title'), max_length=50, blank=True, default=""
    )
    image_description = ExtendedTextField(
        _('image description'), blank=True, default=""
    )
    image = FileBrowseField(
        _('overview image'),
        max_length=255,
        directory="articles/",
        extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
        blank=True
    )
    is_featured = models.BooleanField(_("Featured"), default=False)
    language = models.CharField(
        _("Language"),
        choices=settings.LANGUAGES,
        blank=True,
        default="",
        max_length=5
    )

    objects = ArticleManager()

    class Meta:
        abstract = True
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        ordering = ("-published_from", "-creation_date")

    def __unicode__(self):
        return self.title

    # just for backwards compatibility
    def get_title(self):
        return self.title

    def get_subtitle(self):
        return self.subtitle

    def get_description(self):
        return mark_safe(self.description)

    def get_content(self):
        return mark_safe(self.content)

    def get_image_title(self):
        return self.image_title

    def get_image_description(self, language=None):
        return mark_safe(self.image_description)

    def get_type(self):
        if self.article_type:
            return self.article_type.slug
        return ""

    def is_news(self):
        return self.article_type.slug == u'news'

    def is_short_news(self):
        return self.article_type.slug == u'short_news'

    def is_interview(self):
        return self.article_type.slug == u'interviews'

    def get_relative_url(self):
        #from django.conf import settings
        return "%s/%s/" % (self.pubdate.strftime("%Y/%m/%d").lower(), self.slug)

    def guess_language(self):
        return guess_language_code(
            self.title,
            self.subtitle,
            self.description,
            self.content,
        )

    def get_url_path(self):
        kwargs = {
            'article_slug': self.slug,
            'year': str(self.published_from.year),
            'month': str(self.published_from.month),
            'day': str(self.published_from.day),
        }
        if self.article_type:
            kwargs['type_sysname'] = self.article_type.slug

        try:
            return reverse(
                "%s:article_object_detail" % get_current_language(),
                kwargs=kwargs
            )
        except:
            return reverse("article_object_detail", kwargs=kwargs)
