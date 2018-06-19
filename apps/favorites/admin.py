# -*- coding: UTF-8 -*-
from copy import deepcopy
from django.db import models
from django.contrib import admin

from base_libs.models.admin import ObjectRelationMixinAdminOptions

Favorite = models.get_model("favorites", "Favorite")

ObjectRelationAdminMixin = ObjectRelationMixinAdminOptions()


class FavoriteOptions(ObjectRelationAdminMixin):
    save_on_top = True
    list_display = ("__unicode__", "get_content_object_display")
    fieldsets = []
    raw_id_fields = ["user"]
    related_lookup_fields = deepcopy(ObjectRelationAdminMixin.related_lookup_fields)
    related_lookup_fields.setdefault('fk', [])
    related_lookup_fields['fk'] += ["user"]


admin.site.register(Favorite, FavoriteOptions)
