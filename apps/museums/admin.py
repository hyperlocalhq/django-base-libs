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

MuseumCategory = models.get_model("museums", "MuseumCategory")
AccessibilityOption = models.get_model("museums", "AccessibilityOption")
Museum = models.get_model("museums", "Museum")
Season = models.get_model("museums", "Season")
SpecialOpeningTime = models.get_model("museums", "SpecialOpeningTime")

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
    fieldsets += [(_("Opening times"), {'fields': ('is_closed', 'is_regular', 'opening', 'break_close', 'break_open', 'closing', get_admin_lang_section(_("Exceptions"), ['exceptions']))})]


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
    fieldsets += [(_("Categories"), {'fields': ('categories', 'tags', 'open_on_mondays')}),]
    fieldsets += [(_("Prices"), {'fields': ('free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass', get_admin_lang_section(_("Price info"), ['admission_price_info', 'reduced_price_info', 'arrangements_for_children', 'free_entrance_for', 'family_ticket', 'group_ticket', 'free_entrance_times', 'yearly_ticket', 'other_tickets' ]))}),]
    fieldsets += [(_("Location"), {'fields': ('street_address','street_address2','postal_code','city', 'district', 'country','latitude','longitude')}),]
    fieldsets += [(_("Postal address"), {'fields': ('post_street_address','post_street_address2','post_postal_code','post_city', 'post_country')}),]
    fieldsets += [(_("Contacts"), {'fields': ((_("Phone"), {'fields': ('phone_country', 'phone_area', 'phone_number')}), (_("Fax"), {'fields': ('fax_country', 'fax_area', 'fax_number')}),'email','website', (_("Group bookings phone"), {'fields': ('group_bookings_phone_country', 'group_bookings_phone_area', 'group_bookings_phone_number')}), (_("Service phone"), {'fields': ('service_phone_country', 'service_phone_area', 'service_phone_number')}), 'twitter', 'facebook')}),]
    fieldsets += [(_("Contact person"), {'fields': ('contact_name', ('contact_phone_country','contact_phone_area','contact_phone_number'),'contact_email',)}),]
    fieldsets += get_admin_lang_section(_("Mediation offer"), ['mediation_offer',])
    fieldsets += [(_("Accessibility"), {'fields': ['accessibility_options', get_admin_lang_section(_("Explanation"), ['accessibility',])]})]
    fieldsets += [(_("Services"), {'fields': [
        'service_shop', get_admin_lang_section(_("Details"), ['service_shop_info',]),
        'service_books', get_admin_lang_section(_("Details"), ['service_books_info',]),
        'service_restaurant', get_admin_lang_section(_("Details"), ['service_restaurant_info',]),
        'service_cafe', get_admin_lang_section(_("Details"), ['service_cafe_info',]),
        'service_library', get_admin_lang_section(_("Details"), ['service_library_info',]),
        'service_archive', get_admin_lang_section(_("Details"), ['service_archive_info',]),
        'service_studio', get_admin_lang_section(_("Details"), ['service_studio_info',]),
        'service_online', get_admin_lang_section(_("Details"), ['service_online_info',]),
        'service_diaper_changing_table',
        'service_birthdays', get_admin_lang_section(_("Details"), ['service_birthdays_info',]),
        'service_rent', get_admin_lang_section(_("Details"), ['service_rent_info',]),
        'service_other', get_admin_lang_section(_("Details"), ['service_other_info',]),
    ]})]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories", "accessibility_options")
    
    inlines = [SeasonInline, SpecialOpeningTimeInline]
    
    def is_geoposition_set(self, obj):
        if obj.latitude:
            return '<img alt="True" src="%sgrappelli/img/admin/icon-yes.gif" />' % settings.STATIC_URL
        return '<img alt="False" src="%sgrappelli/img/admin/icon-no.gif">' % settings.STATIC_URL
    is_geoposition_set.allow_tags = True
    is_geoposition_set.short_description = _("Geoposition?")
        
admin.site.register(Museum, MuseumAdmin)
