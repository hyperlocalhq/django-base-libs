# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section

from jetson.apps.media_gallery.admin import GenericMediaFileInline

Exhibition = models.get_model("exhibitions", "Exhibition")

class ExhibitionMediaFileInline(GenericMediaFileInline):
    fieldsets = [
        (None, {'fields': ("path", )}),
        ]
    fieldsets += get_admin_lang_section(_("Description"), ['title', 'description'], True)
    fieldsets += [(None, {'fields': ("sort_order", )}),]
    sortable_field_name = "sort_order"
    classes = ('collapse open',)

class ExhibitionAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'start', 'end', 'status', 'newly_opened', 'featured', 'closing_soon')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', 'newly_opened', 'featured', 'closing_soon')
    search_fields = ('title', 'subtitle', 'slug')
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'description', 'website'])
    fieldsets += [(None, {'fields': ('slug', 'museum', 'image')}),]
    fieldsets += get_admin_lang_section(_("Image Caption"), ['image_caption', ])
    fieldsets += [(_("Time"), {'fields': ('start','end',)}),]
    fieldsets += [(_("Status"), {'fields': ('newly_opened','featured','closing_soon','status')}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    
    inlines = [ExhibitionMediaFileInline]


admin.site.register(Exhibition, ExhibitionAdmin)

