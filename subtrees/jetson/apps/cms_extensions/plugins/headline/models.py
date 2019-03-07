# -*- coding: utf-8 -*-
import sys

from django.db import models

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin


class Headline(CMSPlugin):
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    subtitle = models.CharField(
        verbose_name=_("Subtitle"), max_length=200, blank=True
    )

    def __unicode__(self):
        return self.title
