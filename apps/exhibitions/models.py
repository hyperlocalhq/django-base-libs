# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.models import CreationModificationDateMixin
from base_libs.models import SlugMixin

from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # for south

from filebrowser.fields import FileBrowseField

class Exhibition(CreationModificationDateMixin):
    museum = models.ForeignKey("museums.Museum", verbose_name=_("Museum"),)
    
    title = MultilingualCharField(_("Title"), max_length=255)
    description = MultilingualTextField(_("Description"), max_length=255, blank=True)
    website = MultilingualCharField(_("Website"), max_length=255, blank=True)

    start = models.DateField(_("Start"))
    end = models.DateField(_("End"))

    image = FileBrowseField(_('Image'), max_length=255, directory="exhibitions/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = MultilingualTextField(_("Image Caption"), max_length=255, blank=True)

    newly_opened = models.BooleanField(_("Newly opened"))
    featured = models.BooleanField(_("Featured"))
    closing_soon = models.BooleanField(_("Closing soon"))
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Museum")
        verbose_name_plural = _("Museums")

