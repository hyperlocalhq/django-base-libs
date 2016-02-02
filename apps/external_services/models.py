# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from mptt.fields import TreeManyToManyField

from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED
from jetson.apps.external_services.models import *


class ArticleImportSource(Service):
    STATUS_CHOICES = getattr(settings, "PUBLISHING_STATUS_CHOICES", (
        (STATUS_CODE_DRAFT, _("Draft")),
        (STATUS_CODE_PUBLISHED, _("Published")),
    ))

    are_excerpts = models.BooleanField(_("Excerpts"), default=False, help_text=_(
        "Does the feed provide not full content, but excerpts? The link in the list of articles will lead to the external URL if full content is not provided."))

    default_sites = models.ManyToManyField(
        "sites.Site",
        verbose_name=_("Sites"),
        help_text=_("Sites to apply to the imported articles by default."),
        related_name="site_article_import_sources",
        blank=True,
        null=True,
    )

    default_creative_sectors = TreeManyToManyField(
        "structure.Term",
        verbose_name=_("Creative sectors"),
        help_text=_("Creative sectors to apply to the imported articles by default."),
        limit_choices_to={'vocabulary__sysname': 'categories_creativesectors'},
        related_name="cs_ais",
        db_column="default_cs",
        blank=True,
        null=True,
    )

    default_status = models.SmallIntegerField(
        _("status"),
        choices=STATUS_CHOICES,
        default=STATUS_CODE_DRAFT,
        help_text=_("Status to apply to the imported articles by default."),
    )

    content_provider = models.ForeignKey(
        "articles.ArticleContentProvider",
        verbose_name=_("Content provider"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("article-import source")
        verbose_name_plural = _("article-import sources")
        ordering = ("title",)
        db_table = "external_services_ais"


class BulletinImportSource(Service):
    STATUS_CHOICES = (
        ("draft", _("Draft")),
        ("published", _("Published")),
        ("import", _("Imported")),
    )

    default_categories = TreeManyToManyField(
        "structure.Category",
        verbose_name=_("Categories"),
        limit_choices_to={'level': 0},
        help_text=_("Categories to apply to the imported bulletins by default."),
        blank=True,
        null=True,
    )

    default_bulletin_category = models.ForeignKey(
        "bulletin_board.BulletinCategory",
        verbose_name=_("Bulletin category"),
        blank=True,
        null=True,
    )

    default_status = models.CharField(
        _("status"),
        choices=STATUS_CHOICES,
        default="draft",
        max_length=20,
        help_text=_("Status to apply to the imported bulletins by default."),
    )

    content_provider = models.ForeignKey(
        "bulletin_board.BulletinContentProvider",
        verbose_name=_("Content provider"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("bulletin-import source")
        verbose_name_plural = _("bulletin-import sources")
        ordering = ("title",)
        db_table = "external_services_bis"
