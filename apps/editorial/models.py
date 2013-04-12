# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.fields import ExtendedTextField

from cms.models import CMSPlugin

from filebrowser.fields import FileBrowseField

class EditorialContent(CMSPlugin):
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

        