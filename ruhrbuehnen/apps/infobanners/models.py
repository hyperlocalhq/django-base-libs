# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models import SysnameMixin
from base_libs.models import PublishingMixin
from base_libs.models.fields import MultilingualTextField


class InfoBanner(SysnameMixin(db_index=True), PublishingMixin):
    content = MultilingualTextField(_('Content'))
    token = models.CharField(
        _('Token'), max_length=200, blank=True, editable=False
    )

    class Meta:
        verbose_name = _("Information Banner")
        verbose_name_plural = _("Information Banners")
        ordering = ['sysname']

    def __unicode__(self):
        return self.sysname

    def generate_new_token(self):
        import string
        import random
        self.token = "".join(
            [random.choice(string.lowercase) for i in xrange(20)]
        )

    def save(self, *args, **kwargs):
        self.generate_new_token()
        super(InfoBanner, self).save(*args, **kwargs)
