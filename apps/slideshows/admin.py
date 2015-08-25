# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.conf import settings

from base_libs.admin.options import ExtendedStackedInline
from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import ObjectRelationMixinAdminForm
from base_libs.models.admin import get_admin_lang_section
from base_libs.middleware import get_current_language
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
    fieldsets = get_admin_lang_section(None, ['alt'])
    fieldsets += [
        (None, {'fields': ["path", "link"]}),
    ]
    fieldsets += [(None, {'fields': ("sort_order",)}), ]


class SlideshowOptions(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )

    save_on_top = True
    inlines = [Slide_Inline]
    list_display = ('id', '__unicode__',)
    list_display_links = ('id', '__unicode__',)


admin.site.register(Slideshow, SlideshowOptions)
