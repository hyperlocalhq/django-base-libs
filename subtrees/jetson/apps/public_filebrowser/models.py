# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from filebrowser.fields import FileBrowseField

verbose_name = _("Public Filebrowser")

class DirectoryAccess(models.Model):
    group = models.ForeignKey("auth.Group")
    accessible_root = FileBrowseField(_('Accessible root directory'), max_length=255)

    class Meta:
        verbose_name = _("Directory access")
        verbose_name_plural = _("Directory access")
        ordering = ("accessible_root",)
        
    def __unicode__(self):
        return u"%s: %s" % (self.group, self.accessible_root)        
