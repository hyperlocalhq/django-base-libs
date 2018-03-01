# -*- coding: UTF-8 -*-

from django.db import models

Country = models.get_model("i18n", "Country")

from base_libs.middleware import get_current_language


def get_countries(search):
    
    if not search or len(search) < 1:
        return Country.objects.none()
    
    queryset = Country.objects.filter()
    
    language = get_current_language()

    if search != "all":
        if language == "en":
            queryset = queryset.filter(name__istartswith=search)
        else:
            queryset = queryset.filter(name_de__istartswith=search)
        
    return queryset

