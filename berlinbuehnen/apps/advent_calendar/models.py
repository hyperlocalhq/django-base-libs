# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from base_libs.models import (
    CreationModificationMixin,
    SlugMixin,
    MultilingualCharField,
    MultilingualTextField,
)
from filebrowser.fields import FileBrowseField


@python_2_unicode_compatible
class Day(CreationModificationMixin, SlugMixin()):
    day = models.DateField(_("Date"))
    title = MultilingualCharField(_("Title"), max_length=200)
    description = MultilingualTextField(_("Description"))
    preview_image = FileBrowseField(
        _('Preview Image'), max_length=255, directory="advent-calendar/",
        extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True,
    )
    image = FileBrowseField(
        _('Active Image'), max_length=255, directory="advent-calendar/",
        extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True,
    )

    class Meta:
        verbose_name = _("Day")
        verbose_name_plural = _("Days")
        ordering = ("-day",)

    def __str__(self):
        return self.day.strftime('%Y-%m-%d')

    def is_past(self):
        return self.day < now().date()

    def is_present(self):
        return self.day == now().date()

    def is_future(self):
        return self.day > now().date()
