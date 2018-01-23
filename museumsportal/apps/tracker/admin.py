# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section

from museumsportal.apps.tracker.models import Ticket, TicketModifications, Concern

class ConcernOptions(admin.ModelAdmin):
    save_on_top = True
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}),]
    list_display = ['__unicode__',]
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,)}

class TicketModifications_Inline(admin.StackedInline):
    model = TicketModifications
    extra = 0

class TicketOptions(admin.ModelAdmin):
    save_on_top = True
    inlines = [TicketModifications_Inline]
    list_display = ('submitted_date', 'concern', 'get_url', 'priority', 'submitter_name', 'submitter_email', 'status', 'modifier')
    list_filter = ('status', 'concern')
    search_fieldsets = ('description', 'concern', 'status',)
    fieldsets = (
        (None, 
        {'fields': ('concern', 'description', 'status', 'priority', 'url', 'submitter_name', 'submitter_email', 'modifier')}
        ),
    )

    def get_url(self, obj):
        if obj.url:
            return '<a href="%s" target="_blank">%s</a>' % (obj.url, _("Edit"))
        return ''
    get_url.short_description = _("Related Object")
    get_url.allow_tags = True

admin.site.register(Concern, ConcernOptions)
admin.site.register(Ticket, TicketOptions)

