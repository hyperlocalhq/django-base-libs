# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from base_libs.models.models import SysnameMixin
from base_libs.models.models import CreationModificationDateMixin


@python_2_unicode_compatible
class Recommendation(CreationModificationDateMixin, SysnameMixin()):
    STATUS_CHOICE_DRAFT, STATUS_CHOICE_PUBLISHED, = "d", "p"
    STATUS_CHOICES = (
        (STATUS_CHOICE_DRAFT, _("Draft")),
        (STATUS_CHOICE_PUBLISHED, _("Published")),
    )
    WIDGET_TEMPLATE_CHOICES = getattr(settings, "RECOMMENDATIONS_WIDGET_TEMPLATE_CHOICES", [])

    widget_template = models.CharField(_("Widget Template"), max_length=255)
    status = models.CharField(_("Publishing status"), max_length=1, choices=STATUS_CHOICES, default=STATUS_CHOICE_DRAFT)

    class Meta:
        verbose_name = _("Editorial Recommendation")
        verbose_name_plural = _("Editorial Recommendations")
        ordering = ("sysname",)

    def __str__(self):
        return self.sysname

    def get_widget_template_display(self):
        return _(dict(self.WIDGET_TEMPLATE_CHOICES).get(self.widget_template, ""))
