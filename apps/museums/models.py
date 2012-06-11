# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.models import CreationModificationDateMixin
from base_libs.models import SlugMixin

from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # for south

from filebrowser.fields import FileBrowseField

COUNTRY_CHOICES = (
    ('de', _("Germany")),
    ('-', "Other"),
)

class MuseumCategory(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    

class Museum(CreationModificationDateMixin):
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Title"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), max_length=255, blank=True)

    image = FileBrowseField(_('Image'), max_length=255, directory="museums/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = MultilingualTextField(_("Image Caption"), max_length=255, blank=True)

    categories = models.ManyToManyField(MuseumCategory, verbose_name=_("Categories"),)

    street_address = models.CharField(_("Street address"), max_length=255)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255)
    city =  models.CharField(_("City"), default="Berlin", max_length=255)
    country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255)    
    
    phone = models.CharField(_("Phone"), help_text="Ortsvorwahl-Telefonnummer", max_length=255, blank=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True)
    website = URLField("Website", blank=True)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Museum")
        verbose_name_plural = _("Museums")
