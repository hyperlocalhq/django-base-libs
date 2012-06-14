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

class ExhibitionAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'get_museum_display', 'start', 'end', 'status', 'newly_opened', 'featured', 'closing_soon')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', 'newly_opened', 'featured', 'closing_soon')
    search_fields = ('title_de','title_en', 'subtitle_de','subtitle_en', 'slug', 'museum__title_de', 'museum__title_en',)
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description', 'website'])
    fieldsets += [(None, {'fields': ('slug', 'museum', 'image')}),]
    fieldsets += get_admin_lang_section(_("Image Caption"), ['image_caption', ])
    fieldsets += [(_("Time"), {'fields': ('start','end',)}),]
    fieldsets += [(_("Status"), {'fields': ('newly_opened','featured','closing_soon','status')}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    
    inlines = [ExhibitionMediaFileInline]

    def get_museum_display(self, obj):
        return '<a href="/admin/museums/museum/%d/">%s</a>' % (obj.museum.id, obj.museum.title)
    get_museum_display.allow_tags = True
    get_museum_display.short_description = _("Museum")

admin.site.register(Exhibition, ExhibitionAdmin)

