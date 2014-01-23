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
            "highlight": False,
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
            "highlight": False,
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
    list_display = ('id', 'title', 'slug', 'get_museum_display', 'start', 'end', 'is_geoposition_set', 'status', 'newly_opened', 'special', 'featured', 'featured_in_magazine', 'closing_soon')
    list_editable = ('status', 'newly_opened', 'special', 'featured', 'featured_in_magazine', 'closing_soon')
    list_display_links = ('title', )
    list_filter = ('creation_date', 'status', 'newly_opened', 'featured', 'featured_in_magazine', 'closing_soon')
    search_fields = ('title_de','title_en', 'subtitle_de','subtitle_en', 'slug', 'museum__title_de', 'museum__title_en',)
    
    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'teaser', 'description', 'press_text', 'website', 'catalog', 'catalog_ordering'])
    fieldsets += [(None, {'fields': ('slug', 'description_locked',)}),]
    fieldsets += [(_("Location"), {'fields': ('museum', 'location_name', 'street_address','street_address2','postal_code','city', 'country','latitude','longitude')}),]
    fieldsets += get_admin_lang_section(_("Other locations"), ['other_locations', ])
    fieldsets += [(_("Time"), {'fields': ('start','end', 'vernissage', 'finissage', 'exhibition_extended', 'permanent', 'museum_opening_hours')}),]
    fieldsets += [(_("Prices"), {'fields': ('museum_prices', 'free_entrance',  
        'admission_price', get_admin_lang_section(_("Price info"), ['admission_price_info']),
        'reduced_price', get_admin_lang_section(_("Price info"), ['reduced_price_info']),
    )}),]
    fieldsets += [(_("PDF Documents"), {'fields': ('pdf_document_de', 'pdf_document_en',)}),]
    fieldsets += [(_("Categories"), {'fields': ('categories', 'tags', 'newly_opened', 'featured', 'featured_in_magazine', 'closing_soon', 'is_for_children', 'special')}),]
    fieldsets += [(_("Suitability"), {'fields': ('suitable_for_disabled', get_admin_lang_section(_("Description"), ['suitable_for_disabled_info', ]))}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}
    filter_horizontal = ("categories",)
    
    inlines = [OrganizerInline, SeasonInline, MediaFileInline]

    def is_geoposition_set(self, obj):
        return bool(obj.latitude)
    is_geoposition_set.boolean = True
    is_geoposition_set.short_description = _("Geoposition?")

    def get_museum_display(self, obj):
        if obj.museum:
            return u'<a href="/admin/museums/museum/%d/">%s</a>' % (obj.museum.id, obj.museum.title)
        return u''
    get_museum_display.allow_tags = True
    get_museum_display.short_description = _("Museum")

admin.site.register(Exhibition, ExhibitionAdmin)
