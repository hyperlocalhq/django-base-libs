# -*- coding: UTF-8 -*-

from django.db import models

facebook_app_models = models.get_app("facebook_app")


def facebook(request=None):
    d = {
        'FACEBOOK_APP_ID': facebook_app_models.APP_ID,
        'FACEBOOK_APP_REQUIRED_PERMISSIONS': ",".join(
            facebook_app_models.REQUIRED_PERMISSIONS
        ),
    }
    return d
