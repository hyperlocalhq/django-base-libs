# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin

from base_libs.models.admin import ObjectRelationMixinAdminOptions

Flagging = models.get_model("flaggings", "Flagging")


class FlaggingOptions(ObjectRelationMixinAdminOptions()):
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    fieldsets = []

admin.site.register(Flagging, FlaggingOptions)

