# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.models import CMSPlugin

from filebrowser.fields import FileBrowseField

CSS_CLASS_CHOICES = getattr(
    settings, "CMS_PLUGIN_FILEBROWSER_IMAGE_CSS_CLASS_CHOICES", None
)


class FilebrowserImage(CMSPlugin):
    image = FileBrowseField(
        verbose_name=_("Image"),
        max_length=255,
        extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']
    )
    alt = models.CharField(_('Alternative text'), max_length=200, blank=True)
    css_class = models.CharField(
        _('CSS class'), max_length=200, blank=True, choices=CSS_CLASS_CHOICES
    )
    mod = models.ForeignKey(
        "image_mods.ImageModification",
        verbose_name=_('Apply modification'),
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.alt or self.image.filename
