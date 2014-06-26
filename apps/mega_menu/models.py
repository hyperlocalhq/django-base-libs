# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from filebrowser.fields import FileBrowseField

from base_libs.models.models import SysnameMixin
from base_libs.models.fields import ExtendedTextField

verbose_name = _("Mega Drop-down Menu")


class MenuBlock(SysnameMixin(unique=False)):
    title = models.CharField(_("Title"), max_length=255)
    language = models.CharField(_("Language"), max_length=5, choices=settings.LANGUAGES)
    left_column = ExtendedTextField(_("Left Column Content"), blank=True)
    center_column = ExtendedTextField(_("Center Column Content"), blank=True)
    right_column_headline = models.CharField(_("Headline"), max_length=255, blank=True)
    right_column_description = ExtendedTextField(_("Description"), blank=True)
    right_column_image = FileBrowseField(_("Image"), max_length=255, directory="menu/", extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    right_column_link = models.CharField(_("Link"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Menu Block")
        verbose_name_plural = _("Menu Blocks")

    def __unicode__(self):
        return self.title