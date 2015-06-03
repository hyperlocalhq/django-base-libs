# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin

from jetson.apps.mailing.models import EmailTemplatePlaceholder
from jetson.apps.mailing.models import EmailTemplate
from jetson.apps.mailing.models import EmailMessage
from jetson.apps.utils.models import XFieldList

class EmailTemplatePlaceholderOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', 'help_text', 'relates_to']
    list_filter = XFieldList(['relates_to'])
    search_fields = ['name', 'sysname']
    
    fieldsets = get_admin_lang_section(_('Name'), ['name'])
    fieldsets += [(None, {'fields': ("sysname", "relates_to", "help_text")}),]
    
    prepopulated_fields = {"sysname": ("name_%s" % settings.LANGUAGE_CODE,),}

class EmailTemplateOptions(admin.ModelAdmin):
    list_display = XFieldList(['name', 'owner', 'subject_', 'get_site'])
    search_fields = ('name', 'subject', 'subject_de', 'body', 'body_de', 'body_html', 'body_html_de',)
    save_on_top = True
    filter_horizontal = ('allowed_placeholders',)

class EmailMessageOptions(ExtendedModelAdmin):
    list_display = ('creation_date', 'subject', 'sender_display', 'recipients_display', 'is_sent', 'delete_after_sending', 'send_button')
    list_filter = ('creation_date', 'is_sent',)
    search_fields = ('subject', 'body', 'body_html', 'sender_email', 'recipient_emails')
    save_on_top = True
    fieldsets = (
        (_("Sender"), {'classes': ('collapse open',), 'fields': ('sender', 'sender_name', 'sender_email')}),
        (_("Recipients"), {'classes': ('collapse open',), 'fields': ('recipient', 'recipient_emails')}),
        (_("Message"), {'classes': ('collapse open',), 'fields': ('subject', 'body', 'body_html')}),
        (_("Flags"), {'classes': ('collapse closed','float-checkbox'), 'fields': ('is_sent', 'delete_after_sending')}),
        )
    
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
        result = ""
        if obj.recipient:
            result = """<a href="/admin/auth/user/%s/">%s</a>""" % (
                obj.recipient.id,
                obj.recipient_emails,
                )
        else:
            result = obj.recipient_emails.replace("\n", "<br />")
        return result
    recipients_display.allow_tags = True
    recipients_display.short_description = ugettext("Recipients")
    
    def send_button(self, obj):
        result = ""
        if not obj.is_sent:
            result = """<form action="" method="post">
            <p>
                <input type="hidden" name="send" value="%s" />
                <input type="submit" value="%s" />
            </p></form>""" % (obj.id, ugettext("Send"))
        return result
    send_button.allow_tags = True
    send_button.short_description = ""
    
    def changelist_view(self, request, extra_context=None):
        if request.POST:
            try:
                m = EmailMessage.objects.get(pk=request.POST['send'])
            except:
                pass
            else:
                m.send()
                request.user.message_set.create(message=ugettext("""Message "%s" has been sent""") % m)
        return super(EmailMessageOptions, self).changelist_view(request, extra_context)


admin.site.register(EmailTemplatePlaceholder, EmailTemplatePlaceholderOptions)
admin.site.register(EmailTemplate, EmailTemplateOptions)
admin.site.register(EmailMessage, EmailMessageOptions)

