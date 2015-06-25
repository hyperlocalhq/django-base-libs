# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings

def get_user_language(user):
    """ Returns the iso2 code of user's preferred language or default website language """
    Language = models.get_model("i18n", "Language")
    langs = Language.objects.filter(
        person__user = user,
        ).values_list("iso2_code", flat=True)
    if langs:
        return langs[0]
    return settings.LANGUAGE_CODE
    
