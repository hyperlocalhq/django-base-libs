# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField

from filebrowser.fields import FileBrowseField

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
)


class Sponsor(CreationModificationDateMixin):
    title = MultilingualCharField(_('Title'), max_length=255, blank=True)
    image = FileBrowseField(_('File path'), max_length=255, directory="sponsors/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."), blank=True)
    website = URLField(_("Website"), blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    class Meta:
        ordering = ["title"]
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")

    def __unicode__(self):
        return self.title or (self.image and self.image.filename) or self.pk
