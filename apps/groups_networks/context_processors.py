# -*- coding: UTF-8 -*-
from django.apps import apps

groups_networks_models = apps.get_app("groups_networks")

def groups_networks(request=None):
    d = {
        'URL_ID_PERSONGROUP': groups_networks_models.URL_ID_PERSONGROUP,
        'URL_ID_PERSONGROUPS': groups_networks_models.URL_ID_PERSONGROUPS,
        'DEFAULT_LOGO_4_PERSONGROUP': groups_networks_models.DEFAULT_LOGO_4_PERSONGROUP,
        'DEFAULT_FORM_LOGO_4_PERSONGROUP': groups_networks_models.DEFAULT_FORM_LOGO_4_PERSONGROUP,
        'DEFAULT_SMALL_LOGO_4_PERSONGROUP': groups_networks_models.DEFAULT_SMALL_LOGO_4_PERSONGROUP,
        }
    return d

