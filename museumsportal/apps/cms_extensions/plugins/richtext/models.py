# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.utils.text import truncate_words
from django.conf import settings

from base_libs.models.fields import ExtendedTextField

from cms.models import CMSPlugin

class RichText(CMSPlugin):
    """
    Plugin for storing rich-text content
    """
    body = ExtendedTextField(_("body"))
    
    search_fields = ('body',)
    
    def __unicode__(self):
        return u"%s" % (truncate_words(strip_tags(self.body), 3)[:30]+"...")