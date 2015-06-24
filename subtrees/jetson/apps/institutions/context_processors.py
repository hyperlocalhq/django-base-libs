# -*- coding: UTF-8 -*-
import re

from django.conf import settings

from jetson.apps.institutions import models

def institutions(request=None):
    d = {
        'URL_ID_INSTITUTION': models.URL_ID_INSTITUTION,
        'URL_ID_INSTITUTIONS': models.URL_ID_INSTITUTIONS,
        'DEFAULT_LOGO_4_INSTITUTION': models.DEFAULT_LOGO_4_INSTITUTION,
        'DEFAULT_FORM_LOGO_4_INSTITUTION': models.DEFAULT_FORM_LOGO_4_INSTITUTION,
        'DEFAULT_SMALL_LOGO_4_INSTITUTION': models.DEFAULT_SMALL_LOGO_4_INSTITUTION,
        }
    return d

