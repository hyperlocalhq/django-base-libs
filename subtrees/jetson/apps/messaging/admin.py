# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings

from base_libs.admin import ExtendedModelAdmin

InternalMessage = models.get_model("messaging", "InternalMessage")

class InternalMessageOptions(ExtendedModelAdmin):
    list_display = ('creation_date', 'subject', 'sender_display', 'recipient_display', 'is_read', 'is_deleted', 'is_spam', 'is_draft', 'is_replied')
    list_filter = ('creation_date', 'is_read', 'is_deleted', 'is_spam')
    search_fields = ("subject", "body", "sender__username", "sender__first_name", "sender__last_name", "recipient__username", "recipient__first_name", "recipient__last_name")
    search_fieldsets = ('subject', 'body',)
    save_on_top = True
    fieldsets = (
        (_("Sender"), {'classes': ('grp-collapse grp-open',), 'fields': ('sender', )}),
        (_("Recipient"), {'classes': ('grp-collapse grp-open',), 'fields': ('recipient',)}),
        (_("Message"), {'classes': ('grp-collapse grp-open',), 'fields': ('subject', 'body',)}),
        (_("Flags"), {'classes': ('grp-collapse grp-closed','float-checkbox'), 'fields': ('is_read', 'is_deleted', 'is_spam', 'is_draft', 'is_replied',)}),
        )
    raw_id_fields = ("sender", "recipient")
    autocomplete_lookup_fields = {
        'fk': ["sender", "recipient"],
    }
    
    def sender_display(self, obj):
        return """<a href="/admin/auth/user/%s/">%s</a>""" % (
            obj.sender.id,
            obj.sender.profile.get_title(),
            )
    sender_display.allow_tags = True
    sender_display.short_description = ugettext("Sender")
    
    def recipient_display(self, obj):
        return """<a href="/admin/auth/user/%s/">%s</a>""" % (
            obj.recipient.pk,
            obj.recipient.profile.get_title(),
            )
    recipient_display.allow_tags = True
    recipient_display.short_description = ugettext("Recipient")

admin.site.register(InternalMessage, InternalMessageOptions)

