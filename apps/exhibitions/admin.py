# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section

from jetson.apps.media_gallery.admin import GenericMediaFileInline

ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")
Exhibition = models.get_model("exhibitions", "Exhibition")

class ExhibitionCategoryAdmin(ExtendedModelAdmin):
        
    save_on_top = True
    list_display = ['title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', )}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}


admin.site.register(ExhibitionCategory, ExhibitionCategoryAdmin)


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
    list_editable = ('status', 'newly_opened', 'featured', 'closing_soon')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', 'newly_opened', 'featured', 'closing_soon')
    search_fields = ('title_de','title_en', 'subtitle_de','subtitle_en', 'slug', 'museum__title_de', 'museum__title_en',)
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'teaser', 'description', 'press_text', 'website'])
    fieldsets += [(None, {'fields': ('slug', 'image')}),]
    fieldsets += get_admin_lang_section(_("Image Caption"), ['image_caption', ])
    fieldsets += [(_("Location"), {'fields': ('museum', 'location_name', 'street_address','street_address2','postal_code','city', 'district', 'country','latitude','longitude')}),]
    fieldsets += [(_("Time"), {'fields': ('start','end',)}),]
    fieldsets += [(_("Prices"), {'fields': ('museum_prices', 'free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass', get_admin_lang_section(_("Price info"), ['admission_price_info', 'reduced_price_info', 'arrangements_for_children', 'free_entrance_for', 'family_ticket', 'group_ticket', 'free_entrance_times', 'yearly_ticket', 'other_tickets' ]))}),]
    fieldsets += [(_("Categories"), {'fields': ('categories', 'tags', 'newly_opened','featured','closing_soon')}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories",)
    
    inlines = [ExhibitionMediaFileInline]

    def get_museum_display(self, obj):
        return '<a href="/admin/museums/museum/%d/">%s</a>' % (obj.museum.id, obj.museum.title)
    get_museum_display.allow_tags = True
    get_museum_display.short_description = _("Museum")

admin.site.register(Exhibition, ExhibitionAdmin)

