# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from base_libs.models.models import SysnameMixin
from base_libs.models.models import CreationModificationDateMixin

WIDGET_TEMPLATE_CHOICES = (
    ('recommendations/includes/latest_profiles.html', _("Latest Profiles")),
    ('recommendations/includes/latest_bulletins.html', _("Latest Bulletins")),
    ('recommendations/includes/news_of_the_category.html', _("Latest News of the Category")),
)

@python_2_unicode_compatible
class Recommendation(CreationModificationDateMixin, SysnameMixin()):
    widget_template = models.CharField(_("Widget Template", max_length=255, choices=WIDGET_TEMPLATE_CHOICES))

    class Meta:
        verbose_name = _("Editorial Recommendation")
        verbose_name_plural = _("Editorial Recommendations")
        ordering = ("sysname",)

    def __str__(self):
        return self.sysname
