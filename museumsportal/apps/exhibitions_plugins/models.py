# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.fields import ExtendedTextField

from cms.models import CMSPlugin

class NewlyOpenedExhibitionExt(CMSPlugin):
    exhibition = models.ForeignKey("exhibitions.Exhibition", limit_choices_to={'newly_opened': True})
    teaser_text = ExtendedTextField(_("Teaser"), blank=True)
    
    def __unicode__(self):
        return self.exhibition.title
        
    class Meta:
        ordering = ['exhibition__title']
        verbose_name = _("Newly opened exhibition with teaser")
        verbose_name_plural = _("Newly opened exhibitions with teasers")

