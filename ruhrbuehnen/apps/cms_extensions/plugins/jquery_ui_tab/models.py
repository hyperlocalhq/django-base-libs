# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.models.models import SysnameMixin
from base_libs.models.fields import ExtendedTextField

from cms.models import CMSPlugin


class JQueryUITab(CMSPlugin, SysnameMixin()):
    """
    Plugin for storing tab content
    """
    title = models.CharField(_("Tab title"), max_length=40)
    content = ExtendedTextField(_("content"))

    search_fields = ('content', )  # TODO: What is it?

    def __unicode__(self):
        return self.title
