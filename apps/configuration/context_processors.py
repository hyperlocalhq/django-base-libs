# -*- coding: UTF-8 -*-
from museumsportal.apps.configuration.models import SiteSettings

def configuration(request=None):
    site_settings = SiteSettings.objects.get_current()
    d = {
        'site_settings': site_settings,
        }
    return d

