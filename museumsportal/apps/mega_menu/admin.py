# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _


from base_libs.admin import ExtendedModelAdmin

MenuBlock = models.get_model("mega_menu", "MenuBlock")


class MenuBlockAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('id', 'title', 'sysname', 'language')
    list_display_links = ('title', )
    list_filter = ('language',)
    search_fields = ('title', 'sysname', 'left_column', 'center_column', 'right_column_headline', 'right_column_description')
    
    fieldsets = [(None, {'fields': ('title', 'sysname', 'language')}),]
    fieldsets += [(_("Left Column"), {'fields': ('left_column', )}),]
    fieldsets += [(_("Center Column"), {'fields': ('center_column', )}),]
    fieldsets += [(_("Right Column"), {'fields': ('right_column_headline', 'right_column_description', 'right_column_image', 'right_column_link')}),]

    prepopulated_fields = {"sysname": ("title",),}

admin.site.register(MenuBlock, MenuBlockAdmin)
