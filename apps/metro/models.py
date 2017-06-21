# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models import SysnameMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualPlainTextField
from base_libs.models.fields import MultilingualURLField
from filebrowser.fields import FileBrowseField

verbose_name = _("Metro")


class Tile(SysnameMixin()):
    path = FileBrowseField(_('File path'), max_length=255, blank=True, help_text=_("A path to a locally stored image."))
    link = MultilingualURLField(_('Link'), max_length=255, blank=True)
    title = MultilingualCharField(_("Title"), max_length=200, blank=True)
    description = MultilingualPlainTextField(_("Description"), blank=True)
    icon = models.CharField(_('Icon'), max_length=30, blank=True, help_text=_("The name of an icon (counselling version)."))

    class Meta:
        verbose_name = _("tile")
        verbose_name_plural = _("tiles")
        ordering = ["sysname"]

    def __unicode__(self):
        return unicode(self.sysname)
