# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.models.fields import ExtendedTextField

from cms.models import CMSPlugin

from filebrowser.fields import FileBrowseField

COLUMN_WIDTHS = (
    (3, _('25% of the full width')),
    (4, _('33.3% of the full width')),
    (6, _('50% of the full width')),
    (8, _('66.6% of the full width')),
    (9, _('75% of the full width')),
    (12, _('Full width')),
)


class EditorialContent(CMSPlugin):
    title = models.CharField(_("Title"), max_length=255)
    subtitle = models.CharField(_("Subtitle"), max_length=255, blank=True)
    description = ExtendedTextField(_("Description"), blank=True)
    website = models.CharField(_("Website"), max_length=255, blank=True)

    image = FileBrowseField(_('Image'), max_length=255, extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = ExtendedTextField(_("Image Caption"), max_length=255, blank=True)

    col_xs_width = models.PositiveIntegerField(_("Column width for phones"), blank=True, null=True, choices=COLUMN_WIDTHS)
    col_sm_width = models.PositiveIntegerField(_("Column width for tablets"), blank=True, null=True, choices=COLUMN_WIDTHS)
    col_md_width = models.PositiveIntegerField(_("Column width for small desktops"), blank=True, null=True, choices=COLUMN_WIDTHS)
    col_lg_width = models.PositiveIntegerField(_("Column width for large desktops"), blank=True, null=True, choices=COLUMN_WIDTHS)
    css_class = models.CharField(_("CSS Class"), max_length=255, blank=True)

    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Editorial content")
        verbose_name_plural = _("Editorial contents")


class TeaserBlock(CMSPlugin):
    title = models.CharField(_("Title"), max_length=255)
    subtitle = models.CharField(_("Subtitle"), max_length=255, blank=True)
    description = ExtendedTextField(_("Description"), blank=True)
    website = models.CharField(_("Website"), max_length=255, blank=True)

    image = FileBrowseField(_('Image'), max_length=255, extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = ExtendedTextField(_("Image Caption"), max_length=255, blank=True)

    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Teaser")
        verbose_name_plural = _("Teasers")


class Footnote(CMSPlugin):
    title = models.CharField(_("Title"), max_length=255, default="Literatur")
    description = ExtendedTextField(_("Description"), blank=True)

    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Footnote")
        verbose_name_plural = _("Footnotes")


class Intro(CMSPlugin):
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    subtitle = models.CharField(verbose_name=_("Subtitle"), max_length=200, blank=True)
    description = ExtendedTextField(_("Description"), blank=True)
    subdescription = ExtendedTextField(_("Subdescription"), blank=True)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Intro")
        verbose_name_plural = _("Intros")


class FrontpageTeaser(CMSPlugin):
    title = models.CharField(_("Title"), max_length=255)
    title2 = models.CharField(_("Title 2"), max_length=255, blank=True)
    title3 = models.CharField(_("Title 3"), max_length=255, blank=True)
    description = ExtendedTextField(_("Description"), blank=True)
    website = models.CharField(_("Website"), max_length=255, blank=True)

    image = FileBrowseField(_('Image'), max_length=255, extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = ExtendedTextField(_("Image Caption"), max_length=255, blank=True)

    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Frontpage Teaser")
        verbose_name_plural = _("Frontpage Teasers")

        