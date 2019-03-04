# -*- coding: UTF-8 -*-
import re
import sys
from django.db import models

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.utils.safestring import mark_safe
from django.conf import settings

from base_libs.models import SingleSiteMixin
from base_libs.models import SysnameMixin
from base_libs.models import PublishingMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField  # needed for south to work

verbose_name = _("FormBlocks")


class FormBlock(SingleSiteMixin, SysnameMixin(db_index=True)):
    content = MultilingualTextField(
        _('content'), help_text=_("It can contain template tags and variables")
    )

    class Meta:
        verbose_name = _("form block")
        verbose_name_plural = _("form blocks")
        ordering = ['sysname']

    def __unicode__(self):
        return self.sysname

    def get_content(self):
        return mark_safe(self.content)

    def _get_stripped_content(self):
        return re.sub('<[^>]*>', ' ', self.get_rendered_content())

    _get_stripped_content.short_description = _("Content")
    _get_stripped_content.allow_tags = True
