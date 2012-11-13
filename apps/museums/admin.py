# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section

MuseumCategory = models.get_model("museums", "MuseumCategory")
Museum = models.get_model("museums", "Museum")

class MuseumCategoryAdmin(ExtendedModelAdmin):
        
    save_on_top = True
    list_display = ['title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', )}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}


admin.site.register(MuseumCategory, MuseumCategoryAdmin)


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
    fieldsets += [(None, {'fields': ('slug', 'image')}),]
    fieldsets += get_admin_lang_section(_("Image Caption"), ['image_caption', ])
    fieldsets += [(_("Categories"), {'fields': ('categories', 'open_on_mondays', 'free_entrance')}),]
    fieldsets += [(_("Location"), {'fields': ('street_address','street_address2','postal_code','city','country','latitude','longitude', 'public_transport')}),]
    fieldsets += [(_("Contact"), {'fields': ('phone','fax','email','website',)}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories",)
    
    def is_geoposition_set(self, obj):
        if obj.latitude:
            return '<img alt="True" src="%sgrappelli/img/admin/icon-yes.gif" />' % settings.STATIC_URL
        return '<img alt="False" src="%sgrappelli/img/admin/icon-no.gif">' % settings.STATIC_URL
    is_geoposition_set.allow_tags = True
    is_geoposition_set.short_description = _("Geoposition?")
        

admin.site.register(Museum, MuseumAdmin)
