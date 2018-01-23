# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fields import FileBrowseField

from base_libs.models.fields import MultilingualCharField, MultilingualPlainTextField

class FileDescription(models.Model):
    file_path = FileBrowseField(_("File path"), max_length=255, db_index=True)
    title = MultilingualCharField(_("Title"), max_length=300, blank=True)
    description = MultilingualPlainTextField(_("Description"), blank=True)
    author = models.CharField(_('Copyright / Photographer'), max_length=300, blank=True)
    copyright_limitations = models.CharField(_('Copyright limitations'), max_length=300, blank=True)
    
    def __unicode__(self):
        if self.file_path:
            return self.file_path.path
        return u""
        
    class Meta:
        ordering = ['file_path']
        verbose_name = _("File description")
        verbose_name_plural = _("File descriptions")
