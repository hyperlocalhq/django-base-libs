# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext

from ccb.apps.facebook_app.models import FacebookAppSettings

admin.site.register(FacebookAppSettings)
