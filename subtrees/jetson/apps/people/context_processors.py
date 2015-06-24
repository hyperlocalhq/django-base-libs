# -*- coding: UTF-8 -*-
import re

from django.db import models
from django.conf import settings

people_models = models.get_app("people")

def people(request=None):
    d = {
        'URL_ID_PERSON': people_models.URL_ID_PERSON,
        'URL_ID_PEOPLE': people_models.URL_ID_PEOPLE,
        'DEFAULT_LOGO_4_PERSON': people_models.DEFAULT_LOGO_4_PERSON,
        'DEFAULT_FORM_LOGO_4_PERSON': people_models.DEFAULT_FORM_LOGO_4_PERSON,
        'DEFAULT_SMALL_LOGO_4_PERSON': people_models.DEFAULT_SMALL_LOGO_4_PERSON,
        }
    return d

