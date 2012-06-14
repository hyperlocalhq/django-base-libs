# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.models import CreationModificationDateMixin
from base_libs.models import SlugMixin

from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # for south

from filebrowser.fields import FileBrowseField

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('expired', _("Expired")),
    ('import', _("Imported")),
    ) 

class ExhibitionManager(models.Manager):
    def newly_opened(self):
        return self.filter(newly_opened=True, status="published")
        
    def featured(self):
        return self.filter(featured=True, status="published")
        
    def closing_soon(self):
        return self.filter(closing_soon=True, status="published").order_by("end")
        

class Exhibition(CreationModificationDateMixin, SlugMixin()):
    museum = models.ForeignKey("museums.Museum", verbose_name=_("Museum"),)
    
    title = MultilingualCharField(_("Title"), max_length=255)
    description = MultilingualTextField(_("Description"), blank=True)
    website = MultilingualCharField(_("Website"), max_length=255, blank=True)

    start = models.DateField(_("Start"))
    end = models.DateField(_("End"))

    image = FileBrowseField(_('Image'), max_length=255, directory="exhibitions/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = MultilingualTextField(_("Image Caption"), max_length=255, blank=True)

    newly_opened = models.BooleanField(_("Newly opened"))
    featured = models.BooleanField(_("Featured"))
    closing_soon = models.BooleanField(_("Closing soon"))
    
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")
    
    objects = ExhibitionManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Exhibition")
        verbose_name_plural = _("Exhibitions")

