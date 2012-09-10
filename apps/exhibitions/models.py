# -*- coding: UTF-8 -*-

from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from base_libs.models.models import UrlMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models import SlugMixin

from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # for south
from base_libs.middleware import get_current_language

from filebrowser.fields import FileBrowseField

from cms.models import CMSPlugin


STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('expired', _("Expired")),
    ('import', _("Imported")),
    ) 

class ExhibitionCategory(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class ExhibitionManager(models.Manager):
    def newly_opened(self):
        return self.filter(newly_opened=True, status="published").order_by("-featured", "-start")
        
    def featured(self):
        return self.filter(featured=True, status="published")
        
    def closing_soon(self):
        return self.filter(closing_soon=True, status="published").order_by("-featured", "end")
    
    def past(self, timestamp=date.today):
        """ Past events """
        if callable(timestamp):
            timestamp = timestamp()
        return self.filter(
            end__lt=timestamp,
            ).distinct()
            
    def update_expired(self):
        queryset = self.past().exclude(
            status="expired",
            )
        for obj in queryset:
            obj.status = "expired"
            obj.save()

class Exhibition(CreationModificationDateMixin, SlugMixin(), UrlMixin):
    museum = models.ForeignKey("museums.Museum", verbose_name=_("Museum"),)
    
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    website = MultilingualCharField(_("Website"), max_length=255, blank=True)

    start = models.DateField(_("Start"))
    end = models.DateField(_("End"))

    image = FileBrowseField(_('Image'), max_length=255, directory="exhibitions/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    image_caption = MultilingualTextField(_("Image Caption"), max_length=255, blank=True)

    newly_opened = models.BooleanField(_("Newly opened"))
    featured = models.BooleanField(_("Featured"))
    closing_soon = models.BooleanField(_("Closing soon"))
    
    categories = models.ManyToManyField(ExhibitionCategory, verbose_name=_("Categories"), blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")
    
    objects = ExhibitionManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Exhibition")
        verbose_name_plural = _("Exhibitions")

    def get_url_path(self):
        try:
            path = reverse("%s:exhibition_detail" % get_current_language(), kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

class NewlyOpenedExhibition(CMSPlugin):
    exhibition = models.ForeignKey(Exhibition, limit_choices_to={'newly_opened': True})
    
    def __unicode__(self):
        return self.exhibition.title
        
    class Meta:
        ordering = ['exhibition__title']
        verbose_name = _("Newly opened exhibition")
        verbose_name_plural = _("Newly opened exhibitions")
    
