# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from datetime import date, timedelta

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import date as date_filter
#from django.contrib.admin import SimpleListFilter

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section

from jetson.apps.advertising.models import *


class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'website']
    list_display = ['company_name', 'website', 'user']


class AdCategoryAdmin(ExtendedModelAdmin):
    list_display = ['title', 'sysname']
    fieldsets = [
        (None, {
            'fields': ('sysname', )
        }),
    ]
    fieldsets += get_admin_lang_section(_("Contents"), ['title', 'description'])


class AdZoneAdmin(ExtendedModelAdmin):
    list_display = ['title', 'sysname', 'description']
    fieldsets = [
        (None, {
            'fields': ('sysname', )
        }),
    ]
    fieldsets += get_admin_lang_section(_("Contents"), ['title', 'description'])


class AdBaseAdmin(ExtendedModelAdmin):
    list_display = [
        'title', 'url', 'advertiser', 'zone', 'category', 'start_showing',
        'stop_showing', 'get_impressions', 'get_clicks'
    ]
    list_filter = [
        'start_showing', 'advertiser', 'category', 'zone', 'language'
    ]
    search_fields = ['title', 'url']

    def get_impressions(self, obj):
        current_month = date.today().replace(day=1)
        current_month_minus_1 = current_month - timedelta(days=1)
        current_month_minus_2 = current_month_minus_1.replace(
            day=1
        ) - timedelta(days=1)
        impressions_by_month = [
            date_filter(current_month_minus_2, "F") + (
                ": <strong>%d</strong>" % obj.adimpression_set.filter(
                    impression_date__year=current_month_minus_2.year,
                    impression_date__month=current_month_minus_2.month,
                ).count()
            ),
            date_filter(current_month_minus_1, "F") + (
                ": <strong>%d</strong>" % obj.adimpression_set.filter(
                    impression_date__year=current_month_minus_1.year,
                    impression_date__month=current_month_minus_1.month,
                ).count()
            ),
            date_filter(current_month, "F") + (
                ": <strong>%d</strong>" % obj.adimpression_set.filter(
                    impression_date__year=current_month.year,
                    impression_date__month=current_month.month,
                ).count()
            )
        ]
        return "<br />".join(impressions_by_month)

    get_impressions.short_description = _('Impressions')
    get_impressions.allow_tags = True

    def get_clicks(self, obj):
        current_month = date.today().replace(day=1)
        current_month_minus_1 = current_month - timedelta(days=1)
        current_month_minus_2 = current_month_minus_1.replace(
            day=1
        ) - timedelta(days=1)
        clicks_by_month = [
            date_filter(current_month_minus_2, "F") + (
                ": <strong>%d</strong>" % obj.adclick_set.filter(
                    click_date__year=current_month_minus_2.year,
                    click_date__month=current_month_minus_2.month,
                ).count()
            ),
            date_filter(current_month_minus_1, "F") + (
                ": <strong>%d</strong>" % obj.adclick_set.filter(
                    click_date__year=current_month_minus_1.year,
                    click_date__month=current_month_minus_1.month,
                ).count()
            ),
            date_filter(current_month, "F") + (
                ": <strong>%d</strong>" % obj.adclick_set.filter(
                    click_date__year=current_month.year,
                    click_date__month=current_month.month,
                ).count()
            )
        ]
        return "<br />".join(clicks_by_month)

    get_clicks.short_description = _('Clicks')
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
        (_(u'Main data'), {
            'fields': ('title', 'url', 'content')
        }),
        (
            _(u'Categories'), {
                'fields': ('language', 'advertiser', 'zone', 'category')
            }
        ),
        (_(u'Publishing'), {
            'fields': ('start_showing', 'stop_showing')
        }),
    ]


class BannerAdAdmin(AdBaseAdmin):
    fieldsets = [
        (_(u'Main data'), {
            'fields': ('title', 'url', 'content')
        }),
        (
            _(u'Categories'), {
                'fields': ('language', 'advertiser', 'zone', 'category')
            }
        ),
        (_(u'Publishing'), {
            'fields': ('start_showing', 'stop_showing')
        }),
    ]


admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(AdCategory, AdCategoryAdmin)
admin.site.register(AdZone, AdZoneAdmin)
admin.site.register(TextAd, TextAdAdmin)
admin.site.register(BannerAd, BannerAdAdmin)
admin.site.register(AdClick, AdClickAdmin)
admin.site.register(AdImpression, AdImpressionAdmin)
