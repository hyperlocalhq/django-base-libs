# -*- coding: UTF-8 -*-
import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from base_libs.models import SingleSiteMixin
from base_libs.models import SysnameMixin
from base_libs.models import PublishingMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # needed for south to work

from jetson.apps.utils.models import XFieldList

verbose_name = _("Blocks")

class InfoBlock(SingleSiteMixin, SysnameMixin(db_index=True), PublishingMixin):
    title = MultilingualCharField(_('title'), max_length=512, blank=True)
    content = MultilingualTextField(_('content'), help_text=_("It can contain template tags and variables"))
    class Meta:
        verbose_name = _("information block")
        verbose_name_plural = _("information blocks")
        ordering = XFieldList(['title_', 'content_'])
        
    def __unicode__(self):
        return self.sysname

    # just for backward compatibility
    def get_title(self):
        return self.title
    
    def get_content(self):
        return mark_safe(self.content)

    def _get_stripped_content(self):
        return re.sub('<[^>]*>', '', self.get_content())
    _get_stripped_content.short_description = _("Content")
    _get_stripped_content.allow_tags = True
