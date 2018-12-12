# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin


class CMSAdZone(CMSPlugin):
    zone = models.ForeignKey("advertising.AdZone", verbose_name=_("Zone"))
    category = models.ForeignKey(
        "advertising.AdCategory",
        verbose_name=_("Category"),
        blank=True,
        null=True
    )

    def __unicode__(self):
        if self.category:
            return " | ".join((self.zone.title, self.category.title))
        return self.zone.title
