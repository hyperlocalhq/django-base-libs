# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext as _
from django.db import models


class PrivacySettings(models.Model):
    user = models.OneToOneField("auth.User", verbose_name=_("User"), on_delete=models.CASCADE)
    display_to_public = models.BooleanField(_("Display profile to public"), default=True)
    display_username = models.BooleanField(_("Display username instead of full name"), default=False)

    class Meta:
        verbose_name = _("Privacy Settings")
        verbose_name_plural = _("Privacy Settings")
        ordering = ['user__username']

    def __unicode__(self):
        return self.user.username