# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section

from berlinbuehnen.apps.advertising.models import *


class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'website']
    list_display = ['company_name', 'website', 'user']


class AdCategoryAdmin(ExtendedModelAdmin):
    list_display = ['title', 'sysname']
    fieldsets = [(None, {'fields': ('sysname',)}),]
    fieldsets += get_admin_lang_section(_("Contents"), ['title', 'description'])


class AdZoneAdmin(ExtendedModelAdmin):
    list_display = ['title', 'sysname', 'description']
    fieldsets = [(None, {'fields': ('sysname',)}),]
    fieldsets += get_admin_lang_section(_("Contents"), ['title', 'description'])


class AdBaseAdmin(ExtendedModelAdmin):
    list_display = ['title', 'url', 'advertiser', 'zone', 'category', 'show_ad_label', 'start_showing', 'stop_showing', 'get_impressions', 'get_clicks']
    list_filter = ['start_showing', 'advertiser', 'category', 'zone', 'language']
    search_fields = ['title', 'url']

    def get_impressions(self, obj):
        return obj.impressions_stats
    get_impressions.short_description = _("Impressions")
    get_impressions.allow_tags = True

    def get_clicks(self, obj):
        return obj.clicks_stats
    get_clicks.short_description = _("Clicks")
    get_clicks.allow_tags = True

#class AdZoneListFilter(SimpleListFilter):
#    title = _('zone')
#    parameter_name = 'zone'
#
#    def lookups(self, request, model_admin):
#        return AdZone.objects.value_list("pk", "title_%s" % request.LANGUAGE_CODE, flat=True)
#
#    def queryset(self, request, queryset):
#        return queryset.filter(zone__pk=self.value)


class AdClickAdmin(ExtendedModelAdmin):
    search_fields = ['ad', 'source_ip']
    list_display = ['ad', 'click_date', 'source_ip']
    list_filter = ['click_date']
    date_hierarchy = 'click_date'


class AdImpressionAdmin(ExtendedModelAdmin):
    search_fields = ['ad', 'source_ip']
    list_display = ['ad', 'impression_date', 'source_ip']
    list_filter = ['impression_date']
    date_hierarchy = 'impression_date'


class TextAdAdmin(AdBaseAdmin):
    search_fields = ['title', 'url', 'content']
    fieldsets = [
        (_(u'Main data'), {'fields': ('title', 'url', 'content', 'show_ad_label')}),
        (_(u'Categories'), {'fields': ('language', 'advertiser', 'zone', 'category')}),
        (_(u'Publishing'), {'fields': ('start_showing', 'stop_showing')}),
    ]


class BannerAdAdmin(AdBaseAdmin):
    fieldsets = [
        (_(u'Main data'), {'fields': ('title', 'url', 'content', 'show_ad_label')}),
        (_(u'Categories'), {'fields': ('language', 'advertiser', 'zone', 'category')}),
        (_(u'Publishing'), {'fields': ('start_showing', 'stop_showing')}),
    ]


admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(AdCategory, AdCategoryAdmin)
admin.site.register(AdZone, AdZoneAdmin)
admin.site.register(TextAd, TextAdAdmin)
admin.site.register(BannerAd, BannerAdAdmin)
admin.site.register(AdClick, AdClickAdmin)
admin.site.register(AdImpression, AdImpressionAdmin)
