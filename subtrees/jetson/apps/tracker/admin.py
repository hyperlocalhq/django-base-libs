# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section

from jetson.apps.tracker.models import Ticket, TicketModifications, Concern


class ConcernOptions(admin.ModelAdmin):
    save_on_top = True
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', )
        }),
    ]
    list_display = [
        '__unicode__',
    ]
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE, )}


class TicketModifications_Inline(admin.StackedInline):
    model = TicketModifications
    extra = 0


class TicketOptions(admin.ModelAdmin):
    save_on_top = True
    inlines = [TicketModifications_Inline]
    list_display = (
        'concern', 'priority', 'submitted_date', 'submitter_name',
        'submitter_email', 'status', 'modifier'
    )
    list_filter = ('status', 'concern')
    search_fieldsets = (
        'description',
        'concern',
        'status',
    )
    fieldsets = (
        (
            None, {
                'fields':
                    (
                        'concern', 'description', 'status', 'priority', 'url',
                        'submitter_name', 'submitter_email', 'modifier'
                    )
            }
        ),
    )


admin.site.register(Concern, ConcernOptions)
admin.site.register(Ticket, TicketOptions)
