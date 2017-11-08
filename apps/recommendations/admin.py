# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ["sysname", "widget_template"]
    search_fields = ["sysname"]
    list_filter = ["widget_template"]
    fieldsets = [
        (_("Content"), {'fields': ["sysname", "widget_template"]}),
    ]
