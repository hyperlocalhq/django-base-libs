# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section

MuseumCategory = models.get_model("museums", "MuseumCategory")
MuseumService = models.get_model("museums", "MuseumService")
Museum = models.get_model("museums", "Museum")

class MuseumCategoryAdmin(ExtendedModelAdmin):
        
    save_on_top = True
    list_display = ['title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order')}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}


admin.site.register(MuseumCategory, MuseumCategoryAdmin)

class MuseumServiceAdmin(ExtendedModelAdmin):
        
    save_on_top = True
    list_display = ['title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order', )}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}


admin.site.register(MuseumService, MuseumServiceAdmin)


class MuseumAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'creation_date', 'status', 'is_geoposition_set')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', 'categories', 'open_on_mondays', 'free_entrance')
    search_fields = ('title', 'subtitle', 'slug')
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'teaser', 'description', 'press_text'])
    fieldsets += [(None, {'fields': ('slug', 'image', get_admin_lang_section(_("Image Caption"), ['image_caption', ]))}),]
    fieldsets += [(_("Categories"), {'fields': ('categories', 'services', 'tags', 'open_on_mondays')}),]
    fieldsets += [(_("Prices"), {'fields': ('free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass', get_admin_lang_section(_("Price info"), ['admission_price_info', 'reduced_price_info', 'arrangements_for_children', 'free_entrance_for', 'family_ticket', 'group_ticket', 'free_entrance_times', 'yearly_ticket', 'other_tickets' ]))}),]
    fieldsets += [(_("Location"), {'fields': ('street_address','street_address2','postal_code','city', 'district', 'country','latitude','longitude')}),]
    fieldsets += [(_("Contact"), {'fields': ('phone','fax','email','website', 'group_bookings_phone', 'service_phone')}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories", "services",)
    
    def is_geoposition_set(self, obj):
        if obj.latitude:
            return '<img alt="True" src="%sgrappelli/img/admin/icon-yes.gif" />' % settings.STATIC_URL
        return '<img alt="False" src="%sgrappelli/img/admin/icon-no.gif">' % settings.STATIC_URL
    is_geoposition_set.allow_tags = True
    is_geoposition_set.short_description = _("Geoposition?")
        

admin.site.register(Museum, MuseumAdmin)
