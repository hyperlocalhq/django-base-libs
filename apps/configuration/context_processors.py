# -*- coding: UTF-8 -*-
import re

from django.conf import settings

from jetson.apps.configuration.models import SiteSettings


def configuration(request=None):
    site_settings = SiteSettings.objects.get_current()
    d = {
        'site_settings': site_settings,
    }
    return d
