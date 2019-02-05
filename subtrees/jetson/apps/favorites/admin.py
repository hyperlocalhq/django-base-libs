# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin

from base_libs.models.admin import ObjectRelationMixinAdminOptions

Favorite = models.get_model("favorites", "Favorite")


class FavoriteOptions(ObjectRelationMixinAdminOptions()):
    save_on_top = True
    list_display = (
        '__unicode__', 'get_content_object_display', 'creation_date'
    )
    fieldsets = []


admin.site.register(Favorite, FavoriteOptions)
