# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from base_libs.models import CreationModificationDateMixin

verbose_name = _("Facebook App")

try:
    APP_ID = settings.FACEBOOK_APP_ID
except Exception:
    raise ImproperlyConfigured, "settings.FACEBOOK_APP_ID should be defined"

try:
    APP_SECRET = settings.FACEBOOK_APP_SECRET
except Exception:
    raise ImproperlyConfigured, "settings.FACEBOOK_APP_SECRET should be defined"

REQUIRED_PERMISSIONS = getattr(settings, "FACEBOOK_APP_REQUIRED_PERMISSIONS", [
    "email",
    "manage_pages",
    # "create_event",
    "publish_stream",
    "offline_access",
    "user_photos",
])


class FacebookAppSettings(CreationModificationDateMixin):
    user = models.ForeignKey(User)
    fb_id = models.BigIntegerField(_("User ID on Facebook"))
    name = models.CharField(_("Full name"), max_length=255)
    profile_url = models.URLField(_("User Link"), max_length=255)
    access_token = models.CharField(_("Access Token"), max_length=255)

    class Meta:
        verbose_name = _("Facebook App Settings")
        verbose_name_plural = _("Facebook App Settings")

    def __unicode__(self):
        return unicode(self.user)


class FacebookPage(CreationModificationDateMixin):
    owner_settings = models.ForeignKey(FacebookAppSettings)
    institution = models.ForeignKey("institutions.Institution")
    fb_id = models.BigIntegerField(_("Page ID on Facebook"))
    name = models.CharField(_("Full name"), max_length=255)
    profile_url = models.URLField(_("Page Link"), max_length=255)
    access_token = models.CharField(_("Page Access Token"), max_length=255)

    class Meta:
        verbose_name = _("Facebook Page")
        verbose_name_plural = _("Facebook Pages")

    def __unicode__(self):
        return unicode(self.name)
