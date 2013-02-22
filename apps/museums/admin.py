# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

MuseumCategory = models.get_model("museums", "MuseumCategory")
AccessibilityOption = models.get_model("museums", "AccessibilityOption")
Museum = models.get_model("museums", "Museum")
Season = models.get_model("museums", "Season")
SpecialOpeningTime = models.get_model("museums", "SpecialOpeningTime")
MediaFile = models.get_model("museums", "MediaFile")

class MuseumCategoryAdmin(TreeEditor, ExtendedModelAdmin):
        
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}


admin.site.register(MuseumCategory, MuseumCategoryAdmin)


class AccessibilityOptionAdmin(ExtendedModelAdmin):
        
    save_on_top = True
    list_display = ['title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'image', 'sort_order', )}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}


admin.site.register(AccessibilityOption, AccessibilityOptionAdmin)


class SeasonInline(ExtendedStackedInline):
    model = Season
    extra = 0
    template = "admin/museums/museum/season_inline.html"

class SpecialOpeningTimeInline(ExtendedStackedInline):
    model = SpecialOpeningTime
    extra = 0
    fieldsets = get_admin_lang_section(_("Title"), ['day_label'])
    fieldsets += [(_("Date"), {'fields': ('yyyy', 'mm', 'dd'), })]
    fieldsets += [(_("Opening hours"), {'fields': ('is_closed', 'is_regular', 'opening', 'break_close', 'break_open', 'closing', get_admin_lang_section(_("Exceptions"), ['exceptions']))})]

class MediaFileInline(ExtendedStackedInline):
    model = MediaFile
    extra = 0
    sortable = True
    sortable_field_name = "sort_order"

class MuseumAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('id', 'title', 'get_owners_list', 'creation_date', 'status', 'is_geoposition_set')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', 'categories', 'open_on_mondays', 'free_entrance')
    search_fields = ('title', 'subtitle', 'slug')
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description', 'press_text'])
    fieldsets += [(None, {'fields': ('slug', 'image', get_admin_lang_section(_("Image Caption"), ['image_caption', ]))}),]
    fieldsets += [(_("Categories"), {'fields': ('categories', 'tags', 'open_on_mondays')}),]
    fieldsets += [(_("Prices"), {'fields': ('free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
        'show_admission_price_info', get_admin_lang_section(_("Price info"), ['admission_price_info']),
        'show_reduced_price_info', get_admin_lang_section(_("Price info"), ['reduced_price_info']),
        'show_arrangements_for_children', get_admin_lang_section(_("Price info"), ['arrangements_for_children']),
        'show_free_entrance_for', get_admin_lang_section(_("Price info"), ['free_entrance_for']),
        'show_family_ticket', get_admin_lang_section(_("Price info"), ['family_ticket']),
        'show_group_ticket', get_admin_lang_section(_("Price info"), ['group_ticket']),
        'show_free_entrance_times', get_admin_lang_section(_("Price info"), ['free_entrance_times']),
        'show_yearly_ticket', get_admin_lang_section(_("Price info"), ['yearly_ticket']),
        'show_other_tickets', get_admin_lang_section(_("Price info"), ['other_tickets']),
        )}),]
    fieldsets += [(_("Location"), {'fields': ('street_address','street_address2','postal_code','city', 'district', 'country','latitude','longitude')}),]
    fieldsets += [(_("Contacts"), {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),'email','website', (_("Group bookings phone"), {'fields': ('group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number')}), (_("Service phone"), {'fields': ('service_phone_country', 'service_phone_area', 'service_phone_number')}), 'twitter', 'facebook')}),]
    fieldsets += get_admin_lang_section(_("Mediation offer"), ['mediation_offer',])
    fieldsets += [(_("Accessibility"), {'fields': ['accessibility_options', get_admin_lang_section(_("Explanation"), ['accessibility',])]})]
    fieldsets += [(_("Services"), {'fields': [
        'service_shop', 
        'service_books',
        'service_restaurant',
        'service_cafe',
        'service_library',
        'service_archive',
        'service_studio',
        'service_online',
        'service_diaper_changing_table',
        'service_birthdays',
        'service_rent',
        'service_other', get_admin_lang_section(_("Details"), ['service_other_info',]),
    ]})]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories", "accessibility_options")
    
    inlines = [SeasonInline, SpecialOpeningTimeInline, MediaFileInline]
    
    def is_geoposition_set(self, obj):
        if obj.latitude:
            return '<img alt="True" src="%sgrappelli/img/admin/icon-yes.gif" />' % settings.STATIC_URL
        return '<img alt="False" src="%sgrappelli/img/admin/icon-no.gif">' % settings.STATIC_URL
    is_geoposition_set.allow_tags = True
    is_geoposition_set.short_description = _("Geoposition?")
        
        
    def get_owners_list(self, obj):
        owners_list = []
        for o in obj.get_owners():
            owners_list.append('<a href="/admin/auth/user/%s/">%s</a>' % (o.pk, o.username))
        if owners_list:
            return '<br />'.join(owners_list)
        return '<a href="/claiming-invitation/?museum_id=%s">%s</a>' % (obj.pk, ugettext("Invite owners"))
    get_owners_list.allow_tags = True
    get_owners_list.short_description = _("Owners")
        
        
admin.site.register(Museum, MuseumAdmin)
