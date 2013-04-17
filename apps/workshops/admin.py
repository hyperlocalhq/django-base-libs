# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

Workshop = models.get_model("workshops", "Workshop")
WorkshopTime = models.get_model("workshops", "WorkshopTime")
MediaFile = models.get_model("workshops", "MediaFile")
Organizer = models.get_model("workshops", "Organizer")

class WorkshopTimeInline(admin.StackedInline):
    model = WorkshopTime
    extra = 0

class MediaFileInline(ExtendedStackedInline):
    model = MediaFile
    extra = 0
    sortable = True
    sortable_field_name = "sort_order"

class OrganizerInline(ExtendedStackedInline):
    model = Organizer
    extra = 0

class WorkshopAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'creation_date', 'status', 'is_geoposition_set')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', )
    search_fields = ('title', 'subtitle', 'workshop_type', 'slug')
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'workshop_type', 'description', 'press_text', 'website', ])
    fieldsets += [(None, {'fields': ('slug',)}),]
    fieldsets += [(_("Categories"), {'fields': ('tags', 'languages', 'other_languages', 
        'has_group_offer', 'is_for_preschool', 'is_for_primary_school', 'is_for_youth', 'is_for_families', 'is_for_wheelchaired',
        'is_for_deaf', 'is_for_blind', 'is_for_learning_difficulties',
    )}),]
    fieldsets += [(_("Location"), {'fields': ('museum', 'location_name','street_address','street_address2','postal_code','city', 'district', 'country','latitude','longitude', 'exhibition')}),]
    fieldsets += [(_("Prices"), {'fields': ('free_admission', 'admission_price', 'reduced_price', get_admin_lang_section(_("Details"), ['admission_price_info', 'booking_info', 'meeting_place']))}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("languages",)
    
    inlines = [WorkshopTimeInline, MediaFileInline, OrganizerInline]
    
    def is_geoposition_set(self, obj):
        if obj.latitude:
            return '<img alt="True" src="%sgrappelli/img/admin/icon-yes.gif" />' % settings.STATIC_URL
        return '<img alt="False" src="%sgrappelli/img/admin/icon-no.gif">' % settings.STATIC_URL
    is_geoposition_set.allow_tags = True
    is_geoposition_set.short_description = _("Geoposition?")

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()
        if instances:
            instance = instances[0]
            if isinstance(instance, WorkshopTime):
                instance.workshop.update_closest_workshop_time()
        

admin.site.register(Workshop, WorkshopAdmin)
