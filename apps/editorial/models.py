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

