# -*- coding: UTF-8 -*-
from django.contrib import admin

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin

from .models import Tile


class TileAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('id', '__unicode__',)
    list_display_links = ('id', '__unicode__',)

    fieldsets = [
        (None, {'fields': ["sysname", "path", "icon"]}),
    ]
    fieldsets += get_admin_lang_section(None, ['link', 'title', 'description'])


admin.site.register(Tile, TileAdmin)
