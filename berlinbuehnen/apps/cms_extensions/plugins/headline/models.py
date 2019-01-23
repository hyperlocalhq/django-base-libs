# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin

class Headline(CMSPlugin):
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    subtitle = models.CharField(verbose_name=_("Subtitle"), max_length=200, blank=True)
    
    def __unicode__(self):
        return self.title