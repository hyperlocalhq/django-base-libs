# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

Geolocation = models.get_model("geolocation", "Geolocation")


class GeolocationAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ["region1", "region3", "zip_code", "city"]
    search_fields = [
        "region1", "region2", "region3", "region4", "zip_code", "city", "area1",
        "area2"
    ]


admin.site.register(Geolocation, GeolocationAdmin)
