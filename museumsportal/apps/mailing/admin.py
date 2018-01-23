# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib import messages
from django.conf import settings

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin

from museumsportal.apps.mailing.models import EmailTemplatePlaceholder
from museumsportal.apps.mailing.models import EmailTemplate
from museumsportal.apps.mailing.models import EmailMessage


class EmailTemplatePlaceholderOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', 'help_text', 'relates_to']
    list_filter = ['relates_to']
    search_fields = ['name', 'sysname']
    
    fieldsets = get_admin_lang_section(_('Name'), ['name'])
    fieldsets += [(None, {'fields': ("sysname", "relates_to", "help_text")}),]
    
    prepopulated_fields = {"sysname": ("name_%s" % settings.LANGUAGE_CODE,),}


class EmailTemplateOptions(admin.ModelAdmin):
    list_display = ['name', 'owner', 'subject', 'get_site']
    search_fields = ('name', 'subject', 'subject_de', 'subject_fr', 'subject_pl', 'subject_pl', 'subject_tr', 'subject_es', 'subject_it', 'body', 'body_de', 'body_fr', 'body_pl', 'body_tr', 'body_es', 'body_it', 'body_html', 'body_html_de', 'body_html_fr', 'body_html_pl', 'body_html_tr', 'body_html_es', 'body_html_it',)
    save_on_top = True
    filter_horizontal = ('allowed_placeholders',)


def send_messages(modeladmin, request, queryset):
    for m in queryset:
        if not m.is_sent:
            if m.send():
                messages.success(request, ugettext("""Message "%s" has been sent""") % m)
            else:
                messages.error(request, ugettext("""Message "%s" has not been sent""") % m)
send_messages.short_description = _("Send unsent selected messages")


class EmailMessageOptions(ExtendedModelAdmin):
    list_display = ('creation_date', 'subject', 'recipients_display', 'is_sent', 'delete_after_sending')
    list_filter = ('creation_date', 'is_sent',)
    search_fields = ('subject', 'body', 'body_html', 'sender_email', 'recipient_emails')
    save_on_top = True
    fieldsets = (
        (_("Sender"), {'classes': ('grp-collapse grp-open',), 'fields': ('sender', 'sender_name', 'sender_email')}),
        (_("Recipients"), {'classes': ('grp-collapse grp-open',), 'fields': ('recipient', 'recipient_emails')}),
        (_("Message"), {'classes': ('grp-collapse grp-open',), 'fields': ('subject', 'body', 'body_html')}),
        (_("Flags"), {'classes': ('grp-collapse grp-closed','float-checkbox'), 'fields': ('is_sent', 'delete_after_sending')}),
    )
    actions = [send_messages]

    def sender_display(self, obj):
        result = ""
        if obj.sender:
            result = """<a href="/admin/auth/user/%s/">%s</a>""" % (
                obj.sender.id,
                obj.sender_email,
                )
        else:
            result = obj.sender_email
        return result
    sender_display.allow_tags = True
    sender_display.short_description = ugettext("Sender")
    
    def recipients_display(self, obj):
        from django.template.defaultfilters import force_escape
        result = ""
        if obj.recipient:
            result = """<a href="/admin/auth/user/%s/">%s</a>""" % (
                obj.recipient.id,
                force_escape(obj.recipient.email),
                )
        else:
            result = force_escape(obj.recipient_emails).replace("\n", "<br />")
        return result
    recipients_display.allow_tags = True
    recipients_display.short_description = ugettext("Recipients")


admin.site.register(EmailTemplatePlaceholder, EmailTemplatePlaceholderOptions)
admin.site.register(EmailTemplate, EmailTemplateOptions)
admin.site.register(EmailMessage, EmailMessageOptions)

