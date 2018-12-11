# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.functional import allow_lazy
from django.utils import six
from django.conf import settings

from base_libs.models.fields import ExtendedTextField

from cms.models import CMSPlugin

def truncate_words(s, num, end_text='...'):
    truncate = end_text and ' %s' % end_text or ''
    return Truncator(s).words(num, truncate=truncate)
truncate_words = allow_lazy(truncate_words, six.text_type)


class RichText(CMSPlugin):
    """
    Plugin for storing rich-text content
    """
    body = ExtendedTextField(_("body"))
    
    search_fields = ('body',)
    
    def __unicode__(self):
        return u"%s" % (truncate_words(strip_tags(self.body), 3)[:30]+"...")