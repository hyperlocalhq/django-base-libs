# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField

from filebrowser.fields import FileBrowseField


class SponsorBase(CreationModificationDateMixin):
    title = MultilingualCharField(_('Title'), max_length=255, blank=True)
    image = FileBrowseField(
        _('Image'),
        max_length=255,
        directory="sponsors/",
        extensions=['.jpg', '.jpeg', '.gif', '.png'],
        help_text=_("A path to a locally stored image."),
        blank=True
    )
    website = URLField(_("Website"), blank=True)

    class Meta:
        abstract = True
        ordering = ["title"]
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")

    def __unicode__(self):
        return self.title or (self.image and self.image.filename) or self.pk
