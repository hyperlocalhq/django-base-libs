# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatewords

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualURLField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import PositionField
from base_libs.models.fields import ExtendedTextField  # for south

from filebrowser.fields import FileBrowseField

from cms.models.fields import PlaceholderField
from cms.models import CMSPlugin


IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.gif', '.png']


### BASE PAGE CLASS ###

class ServicePage(CreationModificationDateMixin, SlugMixin(), UrlMixin):
    STATUS_CHOICES = (
        ("draft", _("Draft")),
        ("published", _("Published")),
        ("trashed", _("Trashed")),
    )
    title = MultilingualCharField(_("Title"), max_length=200)
    short_description = MultilingualTextField(_("Short Description"), blank=True)
    header_bg_color = models.CharField(_("Header Background Color"), max_length=20, help_text=_("""Use RGB or HTML format, like "rgb(0, 0, 255)" or "#0000ff"."""))
    header_icon = FileBrowseField(_("Header Icon"), max_length=255, directory="services/", extensions=IMAGE_EXTENSIONS, help_text=_("A path to a locally stored image."))

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title_{}".format(settings.LANGUAGE_CODE)]
        verbose_name = _("Service Page")
        verbose_name_plural = _("Service Pages")

    def get_url_path(self):
        return ""


class IndexItem(CMSPlugin):
    WIDTH_CHOICES = (
        ('single', _("Single")),
        ('double', _("Double")),
    )
    service_page = models.ForeignKey(ServicePage, verbose_name=_("Service Page"))
    width = models.CharField(_("Width"), max_length=20, default="sigle", choices=WIDTH_CHOICES)

    search_fields = ('title', 'body',)

    def __unicode__(self):
        return self.service_page.title


### SERVICES OVERVIEW ###

class ServicesOverviewPage(ServicePage):
    class Meta:
        verbose_name = _("Services Overview Page")
        verbose_name_plural = _("Services Overview Pages")


class ServicesCategory(CreationModificationDateMixin, SlugMixin()):
    page = models.ForeignKey(ServicesOverviewPage, on_delete=models.CASCADE)
    title = MultilingualCharField(_("Title"), max_length=200)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=200, blank=True)
    short_description = MultilingualTextField(_("Short Description"), blank=True)
    image = FileBrowseField(_("Header Icon"), max_length=255, directory="services/", extensions=IMAGE_EXTENSIONS, help_text=_("A path to a locally stored image."))
    sort_order = PositionField(_("Sort order"), collection="page")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title_{}".format(settings.LANGUAGE_CODE)]
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")


class Service(CreationModificationDateMixin):
    category = models.ForeignKey(ServicesCategory, on_delete=models.CASCADE)
    title = MultilingualCharField(_("Title"), max_length=200)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=200, blank=True)
    location = models.ForeignKey("locations.Location", verbose_name=_("Location"), help_text=_("Theater linked to this service"))
    short_description = MultilingualTextField(_("Short Description"), blank=True)
    external_link = MultilingualURLField(_("External Link"), max_length=255)
    image = FileBrowseField(_("Header Icon"), max_length=255, directory="services/", extensions=IMAGE_EXTENSIONS, help_text=_("A path to a locally stored image."))
    sort_order = PositionField(_("Sort order"), collection="category")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["sort_order", "title_{}".format(settings.LANGUAGE_CODE)]
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


### LINKS ###

class LinksPage(ServicePage):
    content = PlaceholderField(slotname="links_page_content")

    class Meta:
        verbose_name = _("Links Page")
        verbose_name_plural = _("Links Pages")


class LinkCategory(CMSPlugin):
    title = models.CharField(_("Title"), max_length=200)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Link Category")
        verbose_name_plural = _("Link Categories")


class Link(CreationModificationDateMixin):
    category = models.ForeignKey(LinkCategory, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=200)
    url = models.URLField(_("URL"))
    short_description = models.TextField(_("Short Description"), blank=True)
    sort_order = PositionField(_("Sort order"), collection="category")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = _("Link")
        verbose_name_plural = _("Links")


### ARTICLES ###

class ArticlesPage(ServicePage):
    content = PlaceholderField(slotname="articles_page_content")

    class Meta:
        verbose_name = _("Articles Page")
        verbose_name_plural = _("Articles Pages")


class TitleAndText(CMSPlugin):
    WIDTH_CHOICES = (
        ('full', _("Full")),
        ('half', _("Half")),
    )
    title = models.CharField(_("Title"), max_length=200, blank=True)
    subtitle = models.CharField(_("Subtitle"), max_length=200, blank=True)
    body = ExtendedTextField(_("Body"))

    width = models.CharField(_("Width"), max_length=20, default="full", choices=WIDTH_CHOICES)

    search_fields = ("title", "subtitle", "body")

    def __unicode__(self):
        return "%s" % (truncatewords(strip_tags(self.body), 3)[:30] + "...")


class ImageAndText(CMSPlugin):
    LAYOUT_CHOICES = (
        ("image-left", _("Image on the left")),
        ("image-right", _("Image on the right")),
    )
    title = models.CharField(_("Title"), max_length=200, blank=True)
    subtitle = models.CharField(_("Subtitle"), max_length=200, blank=True)
    body = ExtendedTextField(_("Body"))

    image = FileBrowseField(_("Image"), max_length=255, extensions=IMAGE_EXTENSIONS)
    alt = models.CharField(_("Alternative text"), max_length=200, blank=True)
    layout = models.CharField(_("Layout"), max_length=20, default="image-left", choices=LAYOUT_CHOICES)

    search_fields = ("title", "body", "alt")

    def __unicode__(self):
        return self.title
