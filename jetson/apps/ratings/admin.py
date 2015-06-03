# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import ObjectRelationMixinAdminForm

Rating = models.get_model("ratings", "Rating")

class RatingAdminForm(ObjectRelationMixinAdminForm()):
    pass

class RatingOptions(ObjectRelationMixinAdminOptions()):
    form = RatingAdminForm
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    fieldsets = []
    
admin.site.register(Rating, RatingOptions)
