# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin

from base_libs.models.admin import ObjectRelationMixinAdminOptions

Priority = models.get_model("priorities", "Priority")


class PriorityOptions(ObjectRelationMixinAdminOptions()):
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    fieldsets = []
    
admin.site.register(Priority, PriorityOptions)

