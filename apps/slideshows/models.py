# -*- coding: UTF-8 -*-
import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from base_libs.models import SysnameMixin
from base_libs.models import PublishingMixin
from base_libs.models.fields import PositionField
from base_libs.models.fields import MultilingualCharField

from filebrowser.fields import FileBrowseField

verbose_name = _("Slideshows")


class Slideshow(SysnameMixin()):
    class Meta:
        verbose_name = _("slideshow")
        verbose_name_plural = _("slideshows")
        ordering = ['sysname']

    def __unicode__(self):
        return self.sysname


class Slide(models.Model):
    slideshow = models.ForeignKey(Slideshow, verbose_name=_("Slideshow"))
    path = FileBrowseField(_('File path'), max_length=255, blank=True,
                           help_text=_("A path to a locally stored image or video."))
    link = models.CharField(_('Link'), max_length=255, blank=True)
    alt = MultilingualCharField(_("Alternative text"), max_length=100, blank=True)
    sort_order = PositionField(_("Sort order"), collection="slideshow")

    class Meta:
        verbose_name = _("slide")
        verbose_name_plural = _("slides")
        ordering = ['sort_order']

    def __unicode__(self):
        return unicode(self.path)
