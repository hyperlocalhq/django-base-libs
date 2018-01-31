# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.models import CMSPlugin
from cms.models.fields import PageField

from filebrowser.fields import FileBrowseField
from base_libs.models.fields import ExtendedTextField

class PageTeaser(CMSPlugin):
    category = models.CharField(verbose_name=_("Category"), max_length=50, blank=True)
    image = FileBrowseField(verbose_name=_("Image"), max_length=255, extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    alt = models.CharField(_('Alternative text'), max_length=200, blank=True)
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    short_description = ExtendedTextField(_("Short Description"), blank=True)
    internal_link = PageField(verbose_name=_("Internal link"), blank=True, null=True, on_delete=models.SET_NULL)
    link_external = models.URLField(_("External Link"), max_length=255, blank=True)
    link_text = models.CharField(verbose_name=_("Link Text"), max_length=30, default=_("read on"))

    def __unicode__(self):
        return self.title
