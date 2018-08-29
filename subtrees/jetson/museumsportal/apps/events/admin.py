# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

EventCategory = models.get_model("events", "EventCategory")
Event = models.get_model("events", "Event")
EventTime = models.get_model("events", "EventTime")
MediaFile = models.get_model("events", "MediaFile")
Organizer = models.get_model("events", "Organizer")


class EventCategoryAdmin(TreeEditor, ExtendedModelAdmin):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'parent')}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(EventCategory, EventCategoryAdmin)


class EventTimeInline(admin.StackedInline):
    model = EventTime
    extra = 0


class MediaFileInline(ExtendedStackedInline):
    model = MediaFile
    extra = 0
    sortable = True
    sortable_field_name = "sort_order"


class OrganizerInline(ExtendedStackedInline):
    model = Organizer
    extra = 0


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.LANGUAGES:
            self.fields['website_%s' % lang_code] = forms.URLField(
                label=self.fields['website_%s' % lang_code].label,
                help_text=self.fields['website_%s' % lang_code].help_text,
                required=self.fields['website_%s' % lang_code].required,
                widget=forms.TextInput(attrs={'class': 'vURLField'})
            )
            self.fields['shop_link_%s' % lang_code] = forms.URLField(
                label=self.fields['shop_link_%s' % lang_code].label,
                help_text=self.fields['shop_link_%s' % lang_code].help_text,
                required=self.fields['shop_link_%s' % lang_code].required,
                widget=forms.TextInput(attrs={'class': 'vURLField'})
            )


class EventAdmin(ExtendedModelAdmin):
    form = EventForm
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'creation_date', 'status', 'featured', 'is_geoposition_set', 'favorites_count')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', 'categories', 'featured', 'linkgroup')
    search_fields = ('title', 'subtitle', 'event_type', 'slug')
    list_editable = ('status', 'featured')
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'event_type', 'description', 'press_text', 'website'])
    fieldsets += [(None, {'fields': ('slug', 'description_locked', )}),]
    fieldsets += [(_("PDF Documents"), {'fields': ('pdf_document_de', 'pdf_document_en',)}),]
    fieldsets += [(_("Categories"), {'fields': ('categories', 'tags', 'languages', 'other_languages', 'suitable_for_children', 'featured')}),]
    fieldsets += [(_("Location"), {'fields': ('museum', 'location_name','street_address','street_address2','postal_code','city', 'country','latitude','longitude', 'exhibition')}),]
    fieldsets += [(_("Prices"), {'fields': ('free_admission', 'admission_price', 'reduced_price', get_admin_lang_section(_("Details"), ['admission_price_info', 'booking_info', 'meeting_place', 'shop_link']))}),]
    fieldsets += get_admin_lang_section(_("Search"), ['search_keywords',])
    fieldsets += [(_("Status"), {'fields': ('status', )}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories", "languages")

    ordering = ("-creation_date",)
    inlines = [EventTimeInline, MediaFileInline, OrganizerInline]
    
    def is_geoposition_set(self, obj):
        return bool(obj.latitude)
    is_geoposition_set.boolean = True
    is_geoposition_set.short_description = _("Geoposition?")
        
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()
        if instances:
            instance = instances[0]
            if isinstance(instance, EventTime):
                instance.event.update_closest_event_time()
        
admin.site.register(Event, EventAdmin)
