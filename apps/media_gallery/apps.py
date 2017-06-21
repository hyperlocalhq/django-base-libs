# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MediaGalleryAppConfig(AppConfig):
    name = "kb.apps.media_gallery"
    verbose_name = _("Media Gallery")