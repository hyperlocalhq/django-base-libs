# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

AgeGroup = models.get_model("workshops", "AgeGroup")
WorkshopCategory = models.get_model("workshops", "WorkshopCategory")
Workshop = models.get_model("workshops", "Workshop")
WorkshopTime = models.get_model("workshops", "WorkshopTime")

class AgeGroupAdmin(ExtendedModelAdmin):
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}),]

admin.site.register(AgeGroup, AgeGroupAdmin)

class WorkshopCategoryAdmin(TreeEditor, ExtendedModelAdmin):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(WorkshopCategory, WorkshopCategoryAdmin)

class WorkshopTimeInline(admin.StackedInline):
    model = WorkshopTime
    extra = 0

class WorkshopAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'creation_date', 'status', 'is_geoposition_set')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', 'categories',)
    search_fields = ('title', 'subtitle', 'slug')
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description'])
    fieldsets += [(None, {'fields': ('slug', 'image')}),]
    fieldsets += [(_("Time"), {'fields': ('workshop_date', 'start', 'end')}),]
    fieldsets += [(_("Categories"), {'fields': ('categories', 'tags', 'languages', 'other_languages', 'age_groups')}),]
    fieldsets += [(_("Location"), {'fields': ('museum', 'location_name','street_address','street_address2','postal_code','city', 'district', 'country','latitude','longitude', 'exhibition')}),]
    fieldsets += [(_("Organizer"), {'fields': ('organizing_museum', 'organizer_title', 'organizer_url_link')}),]
    fieldsets += [(_("Prices"), {'fields': ('admission_price', 'reduced_price', get_admin_lang_section(_("Price info"), ['admission_price_info', 'booking_info']))}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories", "languages")
    
    inlines = [WorkshopTimeInline]
    
    def is_geoposition_set(self, obj):
        if obj.latitude:
            return '<img alt="True" src="%sgrappelli/img/admin/icon-yes.gif" />' % settings.STATIC_URL
        return '<img alt="False" src="%sgrappelli/img/admin/icon-no.gif">' % settings.STATIC_URL
    is_geoposition_set.allow_tags = True
    is_geoposition_set.short_description = _("Geoposition?")
        
admin.site.register(Workshop, WorkshopAdmin)
