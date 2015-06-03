# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import ObjectRelationMixinAdminForm

Favorite = models.get_model("favorites", "Favorite")

class FavoriteAdminForm(ObjectRelationMixinAdminForm()):
    pass

class FavoriteOptions(ObjectRelationMixinAdminOptions()):
    form = FavoriteAdminForm
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    fieldsets = []

admin.site.register(Favorite, FavoriteOptions)
