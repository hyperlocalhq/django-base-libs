# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatewords

from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import PositionField
from base_libs.models.fields import ExtendedTextField

from filebrowser.fields import FileBrowseField

from cms.models import CMSPlugin
from cms.models.fields import PageField


IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.gif', '.png']

LINK_TEXT_CHOICES = (
    ("Yes, please", _("Yes, please")),
    ("more", _("more")),
)


### BANNERS ###

class Banner(CreationModificationDateMixin):
    title = MultilingualCharField(_("Title"), max_length=200)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=200, blank=True)
    short_description = MultilingualTextField(_("Short Description"), blank=True)
    header_bg_color = models.CharField(_("Header Background Color"), max_length=20, help_text=_("""Use RGB or HTML format, like "rgb(0, 0, 255)" or "#0000ff"."""))
    header_icon = FileBrowseField(_("Header Icon"), max_length=255, directory="services/", extensions=IMAGE_EXTENSIONS, help_text=_("A path to a locally stored image."), blank=True)

    def __unicode__(self):
        if (self.subtitle):
            return u"{title} - {subtitle}".format(title=self.title, subtitle=self.subtitle)
        return self.title

    class Meta:
        ordering = ["title_{}".format(settings.LANGUAGE_CODE)]
        verbose_name = _("Service Page Banner")
        verbose_name_plural = _("Service Page Banners")


class IndexItem(CMSPlugin):
    WIDTH_CHOICES = (
        ('single', _("Single")),
        ('double', _("Double")),
    )
    banner = models.ForeignKey(Banner, verbose_name=_("Banner"))
    width = models.CharField(_("Width"), max_length=20, default="single", choices=WIDTH_CHOICES)
    internal_link = PageField(
        verbose_name=_("Internal link"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    external_link = models.URLField(_("External Link"), max_length=255, blank=True)

    def __unicode__(self):
        return self.banner.title

    class Meta:
        verbose_name = _("Index Page Item")
        verbose_name_plural = _("Index Page Items")


class ServicePageBanner(CMSPlugin):
    banner = models.ForeignKey(Banner, verbose_name=_("Banner"))

    def __unicode__(self):
        return self.banner.title

    class Meta:
        verbose_name = _("Service Page Banner")
        verbose_name_plural = _("Service Page Banners")


### SERVICE LISTS ###

class ServiceGridItem(CMSPlugin):
    title = models.CharField(_("Title"), max_length=200)
    subtitle = models.CharField(_("Subtitle"), max_length=200, blank=True)
    short_description = ExtendedTextField(_("Short Description"), blank=True)
    image = FileBrowseField(_("Header Icon"), max_length=255, directory="services/", extensions=IMAGE_EXTENSIONS, help_text=_("A path to a locally stored image."), blank=True)

    internal_link = PageField(
        verbose_name=_("Internal link"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    external_link = models.URLField(_("External Link"), max_length=255, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Grid Item")
        verbose_name_plural = _("Grid Items")


class ServiceListItem(CMSPlugin):
    title = models.CharField(_("Title"), max_length=200)
    subtitle = models.CharField(_("Subtitle"), max_length=200, blank=True)
    location = models.ForeignKey("locations.Location", verbose_name=_("Location"), help_text=_("Theater linked to this service"), blank=True, null=True)
    short_description = ExtendedTextField(_("Short Description"), blank=True)
    external_link = models.URLField(_("External Link"), max_length=255, blank=True)
    image = FileBrowseField(_("Image"), max_length=255, directory="services/", extensions=IMAGE_EXTENSIONS, help_text=_("A path to a locally stored image."), blank=True)
    link_text = models.CharField(_("Link Text"), max_length=20, default="Yes, please", choices=LINK_TEXT_CHOICES)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("List Item")
        verbose_name_plural = _("List Items")


### LINKS ###

class LinkCategory(CMSPlugin):
    title = models.CharField(_("Title"), max_length=200)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Link Category")
        verbose_name_plural = _("Link Categories")

    def copy_relations(self, old_instance):
        self.link_set.all().delete()
        for old_link in old_instance.link_set.all():
            new_link = Link(
                category=self,
                title=old_link.title,
                url=old_link.url,
                short_description=old_link.short_description,
                sort_order=old_link.sort_order,
            )
            new_link.save()


class Link(CreationModificationDateMixin):
    category = models.ForeignKey(LinkCategory, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=200)
    url = models.URLField(_("URL"))
    short_description = models.TextField(_("Short Description"), blank=True)
    sort_order = PositionField(_("Sort order"), collection="category")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["sort_order"]
        verbose_name = _("Link")
        verbose_name_plural = _("Links")


### ARTICLES ###

class TitleAndText(CMSPlugin):
    WIDTH_CHOICES = (
        ('full', _("Full")),
        ('half', _("Half")),
    )
    title = models.CharField(_("Title"), max_length=200, blank=True)
    subtitle = models.CharField(_("Subtitle"), max_length=200, blank=True)
    body = ExtendedTextField(_("Body"))

    internal_link = PageField(
        verbose_name=_("Internal link"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    external_link = models.URLField(_("External Link"), max_length=255, blank=True)
    link_text = models.CharField(_("Link Text"), max_length=20, default="Yes, please", choices=LINK_TEXT_CHOICES)

    width = models.CharField(_("Width"), max_length=20, default="full", choices=WIDTH_CHOICES)

    search_fields = ("title", "subtitle", "body")

    def __unicode__(self):
        return "%s" % (truncatewords(strip_tags(self.body), 3)[:30] + "...")


class ImageAndText(CMSPlugin):
    LAYOUT_CHOICES = (
        ("image-left", _("Image on the left")),
        ("image-right", _("Image on the right")),
        ("image-top", _("Image at the top")),
        ("image-bottom", _("Image at the bottom")),
    )
    title = models.CharField(_("Title"), max_length=200, blank=True)
    subtitle = models.CharField(_("Subtitle"), max_length=200, blank=True)
    body = ExtendedTextField(_("Body"))

    internal_link = PageField(
        verbose_name=_("Internal link"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    external_link = models.URLField(_("External Link"), max_length=255, blank=True)
    link_text = models.CharField(_("Link Text"), max_length=20, default="Yes, please", choices=LINK_TEXT_CHOICES)

    image = FileBrowseField(_("Image"), max_length=255, extensions=IMAGE_EXTENSIONS)
    alt = models.CharField(_("Alternative text"), max_length=200, blank=True)
    layout = models.CharField(_("Layout"), max_length=20, default="image-left", choices=LAYOUT_CHOICES)

    search_fields = ("title", "body", "alt")

    def __unicode__(self):
        return self.title
