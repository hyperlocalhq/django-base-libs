# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import ObjectRelationMixinAdminForm

Flagging = models.get_model("flaggings", "Flagging")

class FlaggingAdminForm(ObjectRelationMixinAdminForm()):
    pass

class FlaggingOptions(ObjectRelationMixinAdminOptions()):
    form = FlaggingAdminForm
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    fieldsets = []

admin.site.register(Flagging, FlaggingOptions)

