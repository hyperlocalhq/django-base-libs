# -*- coding: UTF-8 -*-
import re

from django.db import models
from django.conf import settings

facebook_app_models = models.get_app("facebook_app")

def facebook(request=None):
    d = {
        'FACEBOOK_APP_ID': facebook_app_models.APP_ID,
        'FACEBOOK_APP_REQUIRED_PERMISSIONS': ",".join(
            facebook_app_models.REQUIRED_PERMISSIONS
            ),
        }
    return d

