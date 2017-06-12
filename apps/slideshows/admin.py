# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin

from base_libs.admin.options import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
import filebrowser.settings as filebrowser_settings

URL_FILEBROWSER_MEDIA = getattr(filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/')
Slideshow = models.get_model("slideshows", "Slideshow")
Slide = models.get_model("slideshows", "Slide")


class Slide_Inline(ExtendedStackedInline):
    model = Slide
    sortable = True
    allow_add = True
    extra = 1
    fieldsets = get_admin_lang_section(None, ['title', 'description', 'alt', 'button'])
    fieldsets += [
        (None, {'fields': ["path", "link"]}),
    ]
    fieldsets += [(None, {'fields': ("sort_order",)}), ]


class SlideshowOptions(ExtendedModelAdmin):
    save_on_top = True
    inlines = [Slide_Inline]
    list_display = ('id', '__unicode__',)
    list_display_links = ('id', '__unicode__',)


admin.site.register(Slideshow, SlideshowOptions)
