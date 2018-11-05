# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.conf import settings

from base_libs.models.fields import ExtendedTextField

from cms.models import CMSPlugin

try:
    from django.utils.text import truncate_words
except ImportError:
    from django.utils.text import Truncator
    def truncate_words(text, count):
        return Truncator(text).words(count)


class RichText(CMSPlugin):
    """
    Plugin for storing rich-text content
    """
    body = ExtendedTextField(_("body"))
    
    search_fields = ('body',)
    
    def __unicode__(self):
        from django.utils.text import Truncator
        return u"%s" % (Truncator(strip_tags(self.body)).words(3)[:30]+"...")