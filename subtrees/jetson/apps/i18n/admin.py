from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from jetson.apps.i18n.models import Language, Nationality, Country, CountryLanguage, Area, TimeZone, Phone

class CountryLanguage_Inline(admin.TabularInline):
    model = CountryLanguage

class Area_Inline(admin.TabularInline):
    model = Area

class TimeZone_Inline(admin.TabularInline):
    model = TimeZone

class Phone_Inline(admin.TabularInline):
    model = Phone

class LanguageOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('__unicode__', 'iso3_code', 'iso2_code', 'synonym', 'display')
    list_filter = ('display',)
    search_fieldsets = ('name', 'synonym', 'iso3_code', 'iso2_code')

class CountryLanguageOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('country', 'language', 'lang_type')
    list_filter = ('lang_type',)
    search_fieldsets = ('country', 'language')

class CountryOptions(admin.ModelAdmin):
    save_on_top = True
    inlines = [CountryLanguage_Inline, Area_Inline, TimeZone_Inline, Phone_Inline]
    """
    fieldsets = (
        (_('Sorry! Not allowed to add or modify items in this model.'), {
            'fields': ('iso3_code',)
        }),
    )
    """
    list_display = ('__unicode__', 'iso3_code', 'iso2_code', 'territory_of', 'adm_area', 'display')
    list_filter = ('region', 'territory_of', 'display')
    search_fieldsets = ('name', 'iso3_code', 'iso2_code')

class AreaOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('country', 'name', 'alt_name', 'abbrev', 'reg_area')
    search_fieldsets = ('name',)

class PhoneOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('country', 'code', 'ln_area', 'ln_sn', 'ln_area_sn',
                    'nat_prefix', 'int_prefix')
    search_fieldsets = ('country', 'code')

class NationalityOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('__unicode__', 'display')
    list_filter = ('display',)
    search_fieldsets = ['name']

class TimeZoneOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('country', 'zone')
    search_fieldsets = ('country',)
    ordering = ['country', 'zone']

admin.site.register(Language, LanguageOptions)
admin.site.register(CountryLanguage, CountryLanguageOptions)
admin.site.register(Country, CountryOptions)
admin.site.register(Area, AreaOptions)
admin.site.register(Phone, PhoneOptions)
admin.site.register(Nationality, NationalityOptions)
admin.site.register(TimeZone, TimeZoneOptions)

