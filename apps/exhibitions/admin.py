# -*- coding: UTF-8 -*-

from django import forms
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor
from base_libs.forms.fields import AutocompleteModelChoiceField

ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")
Exhibition = models.get_model("exhibitions", "Exhibition")
Season = models.get_model("exhibitions", "Season")
SpecialOpeningTime = models.get_model("exhibitions", "SpecialOpeningTime")
MediaFile = models.get_model("exhibitions", "MediaFile")
Organizer = models.get_model("exhibitions", "Organizer")

class ExhibitionCategoryAdmin(TreeEditor, ExtendedModelAdmin):
        
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', ]
    
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'parent')}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}


admin.site.register(ExhibitionCategory, ExhibitionCategoryAdmin)

class SeasonInline(ExtendedStackedInline):
    model = Season
    extra = 0
    template = "admin/exhibitions/exhibition/season_inline.html"

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

class OrganizerInline(ExtendedStackedInline):
    model = Organizer
    extra = 0

class ExhibitionAdminForm(forms.ModelForm):
    museum = AutocompleteModelChoiceField(
        required=False,
        label=u"Name",
        help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
        app="museums",
        qs_function="get_published_museums",
        display_attr="title",
        add_display_attr="get_address",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight" : False,
            "multipleSeparator": ",,, ",
            },
        )
    organizing_museum = AutocompleteModelChoiceField(
        required=False,
        label=u"Name",
        help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
        app="museums",
        qs_function="get_published_museums",
        display_attr="title",
        add_display_attr="get_address",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight" : False,
            "multipleSeparator": ",,, ",
            },
        )
    class Meta:
        model = Exhibition

class ExhibitionAdmin(ExtendedModelAdmin):
    form = ExhibitionAdminForm
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
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'teaser', 'description', 'press_text', 'website', 'catalog'])
    fieldsets += [(None, {'fields': ('slug', 'link',)}),]
    fieldsets += [(_("Location"), {'fields': ('museum', 'location_name', 'street_address','street_address2','postal_code','city', 'district', 'country','latitude','longitude')}),]
    fieldsets += get_admin_lang_section(_("Other locations"), ['other_locations', ])
    fieldsets += [(_("Time"), {'fields': ('start','end', 'vernissage', 'finissage', 'exhibition_extended', 'permanent')}),]
    fieldsets += [(_("Prices"), {'fields': ('museum_prices', 'free_entrance', 'member_of_museumspass', 
        'admission_price', get_admin_lang_section(_("Price info"), ['admission_price_info']),
        'reduced_price', get_admin_lang_section(_("Price info"), ['reduced_price_info']),
        'show_group_ticket', get_admin_lang_section(_("Price info"), ['group_ticket']),
        'show_family_ticket',
        'show_yearly_ticket',
    )}),]
    fieldsets += [(_("Categories"), {'fields': ('categories', 'tags', 'newly_opened', 'featured', 'closing_soon', 'is_for_children',)}),]
    fieldsets += [(_("Suitability"), {'fields': ('suitable_for_disabled', get_admin_lang_section(_("Description"), ['suitable_for_disabled_info', ]))}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories",)
    
    inlines = [OrganizerInline, SeasonInline, SpecialOpeningTimeInline, MediaFileInline]

    def get_museum_display(self, obj):
        return '<a href="/admin/museums/museum/%d/">%s</a>' % (obj.museum.id, obj.museum.title)
    get_museum_display.allow_tags = True
    get_museum_display.short_description = _("Museum")

admin.site.register(Exhibition, ExhibitionAdmin)

