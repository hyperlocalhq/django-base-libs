# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models import SysnameMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import PositionField

from filebrowser.fields import FileBrowseField

CATEGORY_STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not-listed', _("Not listed at partners")),
)

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
)


class PartnerCategory(SysnameMixin(blank=True, unique=False)):
    title = MultilingualCharField(_("Title"), max_length=255)
    sort_order = PositionField(_("Sort order"))
    status = models.CharField(_("Status"), max_length=20, choices=CATEGORY_STATUS_CHOICES, blank=True, default="draft")
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        verbose_name = _("Partner category")
        verbose_name_plural = _("Partner categories")
        ordering = ("sort_order",)
        
    def get_published_partners(self):
        return self.partner_set.filter(status="published").order_by("sort_order")


class Partner(models.Model):
    category = models.ForeignKey(PartnerCategory)
    title = MultilingualCharField(_("Title"), max_length=255)
    website_url = models.URLField(_("Website URL"), max_length=255, blank=True)
    image = FileBrowseField(_('Default Image'), max_length=255, directory="partners/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    sort_order = PositionField(_("Sort order"), collection="category")
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
        ordering = ("title",)

