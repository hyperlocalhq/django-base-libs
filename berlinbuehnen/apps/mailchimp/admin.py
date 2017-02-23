# -*- coding: UTF-8 -*-
from django import forms
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext
from django.http import HttpResponse
from django.template import RequestContext
from django.forms.util import ErrorList
from django.conf.urls import *
from django.contrib.admin.util import unquote
from django.contrib import messages

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline

from berlinbuehnen.apps.mailchimp.models import Settings, Subscription, MList, Campaign, MailingContentBlock
from berlinbuehnen.apps.mailchimp.utils import sync_mc_list

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'double_optin', 'update_existing', 'send_welcome', 'delete_member', 'send_goodbye')
    save_on_top = True

admin.site.register(Settings, SettingsAdmin)


class SubscriptionAdminForm(forms.ModelForm):
    class Meta:
        model = Subscription
        
    def clean(self, *args, **kwargs):
        cleaned = super(SubscriptionAdminForm, self).clean(*args, **kwargs)
        if not cleaned.get("subscriber", None) and not cleaned.get("email", ""):
            self._errors['email'] = ErrorList([_("Either subscriber or subscriber email should be filled in.")])
        return cleaned

class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionAdminForm
    list_display = ('email', 'first_name', 'last_name', 'get_mailinglist_with_link', 'creation_date', 'status')
    list_filter = ('mailinglist',)
    search_fields = ('first_name', 'last_name', 'email',)
    fieldsets = (
        (None, {'fields': ("mailinglist", "subscriber", "first_name", "last_name", "email", "ip", "status")}),
        )
    save_on_top = True

admin.site.register(Subscription, SubscriptionAdmin)


class MListAdminForm(forms.ModelForm):
    mailchimp_list = forms.ChoiceField(
        choices=(),
        required=False,
        )

    class Meta:
        model = MList
        
    def __init__(self, *args, **kwargs):
        super(MListAdminForm, self).__init__(*args, **kwargs)
        mailchimp_list_choices = [("", "---------")]
        from mailsnake import MailSnake
        Settings = models.get_model("mailchimp", "Settings")
        try:
            st = Settings.objects.get()
        except:
            pass
        else:
            ms = MailSnake(st.api_key)
            for l in ms.lists()['data']:
                mailchimp_list_choices.append((l['id'], l['name']))
            self.fields['mailchimp_list'].choices = mailchimp_list_choices
            self.fields['mailchimp_list'].initial = self.instance.mailchimp_id
        
class MListAdmin(admin.ModelAdmin):
    form = MListAdminForm
    list_display = ('title', 'get_mailchimp_list', 'get_count_with_link', 'last_sync', 'is_public')
    list_filter = ('is_public',)
    fieldsets = [(None, {'fields': ('site', 'mailchimp_list')}),]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('is_public', )}),]
    save_on_top = True
    
    def save_model(self, request, obj, form, change):
        super(MListAdmin, self).save_model(request, obj, form, change)
        
        obj.mailchimp_id = form.cleaned_data['mailchimp_list']
            
    def get_mailchimp_list(self, obj):
        if not hasattr(self, "_mailchimp_lists"):
            from mailsnake import MailSnake
            Settings = models.get_model("mailchimp", "Settings")
            try:
                st = Settings.objects.get()
            except:
                pass
            else:
                ms = MailSnake(st.api_key)
                self._mailchimp_lists = {}
                for l in ms.lists()['data']:
                    self._mailchimp_lists[l['id']] = l['name']
        
        if obj.mailchimp_id:
            return self._mailchimp_lists[obj.mailchimp_id]
        
    get_mailchimp_list.short_description = _("MailChimp List")
        
    def sync_list(self, request, queryset):
        for ml in queryset:
            for message in sync_mc_list(ml):
                self.message_user(request, message)
            
    sync_list.short_description = _("Synchronize list")

    actions = [sync_list]

admin.site.register(MList, MListAdmin)


class MailingContentBlockInline(ExtendedStackedInline):
    model = MailingContentBlock
    extra = 0
    fieldsets = [(_("Content"), {'fields': ['content_type', 'content', 'sort_order'], 'classes': ('grp-collapse grp-open',)})]
    ordering = ("sort_order",)
    sortable = True
    sortable_field_name = "sort_order"
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

class CampaignAdmin(ExtendedModelAdmin):
    list_display = ('subject', 'get_mailinglist_with_link', 'get_preview_link', 'get_status')
    list_filter = ('mailinglist',)
    fieldsets = [(None, {'fields': ('sender_name', 'sender_email', 'mailinglist', 'template', )}),]
    fieldsets += [(_("Content"), {'fields': ['subject', 'image', 'body_html']})]
    inlines = (MailingContentBlockInline,)

    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )
    save_on_top = True

    def get_urls(self):
        urls = super(CampaignAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^template-content/(?P<template_name>[^/]+)/$', self.admin_site.admin_view(self.template_content)),
            (r'^(.+)/preview/$', self.admin_site.admin_view(self.preview)),
        )
        return my_urls + urls

    def template_content(self, request, template_name):
        from django.shortcuts import render_to_response
        return render_to_response(
            "mailchimp/campaign/includes/%s.html" % template_name,
            {},
            context_instance=RequestContext(request),
            )
        
    def preview(self, request, object_id):
        obj = self.get_object(request, unquote(object_id))
        html = obj.get_rendered_html()
        return HttpResponse(html)

    def get_preview_link(self, obj):
        return '<a href="%d/preview/" target="_blank">%s</a>' % (obj.pk, ugettext("Preview"))
    get_preview_link.short_description = _("Preview")
    get_preview_link.allow_tags = True

    def get_status(self, obj):
        return _("Sent") if obj.is_sent() else _("Draft")
    get_status.short_description = _("Status")

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.is_sent():
            messages.warning(request, _("""Campaign "%s" was not updated at MailChimp, because it has been sent.""") % unicode(obj))


admin.site.register(Campaign, CampaignAdmin)