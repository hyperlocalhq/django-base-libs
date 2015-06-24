# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import ObjectRelationMixinAdminForm

Priority = models.get_model("priorities", "Priority")

class PriorityAdminForm(ObjectRelationMixinAdminForm()):
    pass

class PriorityOptions(ObjectRelationMixinAdminOptions()):
    form = PriorityAdminForm
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    fieldsets = []
    
admin.site.register(Priority, PriorityOptions)

