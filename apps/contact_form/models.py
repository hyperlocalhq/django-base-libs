# -*- coding: UTF-8 -*-
import sys

from django.db import models

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.apps import apps
from django.contrib.auth.models import User
from django.utils.functional import lazy
from django.conf import settings

from base_libs.models import SingleSiteMixin
from base_libs.models import SlugMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import PlainTextModelField
from base_libs.middleware import get_current_language


EmailTemplate = apps.get_model("mailing", "EmailTemplate")

verbose_name = _("Contact Form")


class ContactFormCategory(SingleSiteMixin, SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    recipients = models.ManyToManyField(
        User, verbose_name=_("Recipient(s)"), blank=True
    )
    recipient_emails = PlainTextModelField(
        _("Recipient email(s)"), null=True, blank=True
    )
    auto_answer_template = models.ForeignKey(
        EmailTemplate,
        verbose_name=_("Email template for the automatic answer"),
        help_text=_(
            "Nothing is sent back to the sender if the template is not selected"
        ),
        blank=True,
        null=True
    )
    sort_order = models.IntegerField(_("Sort order"), default=0)

    class Meta:
        verbose_name = _("contact form category")
        verbose_name_plural = _("contact form categories")
        ordering = ['sort_order', 'title']

    def __unicode__(self):
        return self.title

    # just for backward compatibility
    def get_title(self, prefix="", postfix=""):
        return self.title
