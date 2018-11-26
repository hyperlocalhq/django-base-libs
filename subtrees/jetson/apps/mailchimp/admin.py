# -*- coding: UTF-8 -*-
from django import forms
from django.db import models
from django.apps import apps
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext
from django.http import HttpResponse
from django.shortcuts import render
from django.forms.util import ErrorList
from django.conf.urls import *
from django.contrib.admin.util import unquote
from django.contrib import messages

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(
    filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/'
)
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline

from .models import Settings, MList, Campaign, MailingContentBlock, CONTENT_TYPE_CHOICES


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('username', 'api_key', 'double_optin')
    list_display_links = ('username', 'api_key')
    save_on_top = True


admin.site.register(Settings, SettingsAdmin)


class MListAdminForm(forms.ModelForm):
    mailchimp_list = forms.ChoiceField(
        choices=(),
        required=False,
    )

    class Meta:
        model = MList
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(MListAdminForm, self).__init__(*args, **kwargs)
        mailchimp_list_choices = [("", "---------")]
        from mailchimp3 import MailChimp
        Settings = apps.get_model("mailchimp", "Settings")
        try:
            st = Settings.objects.get()
        except:
            pass
        else:
            mailchimp_client = MailChimp(st.username, st.api_key)
            data = mailchimp_client.lists.all(
                get_all=True, fields="lists.id,lists.name"
            )
            for l in data['lists']:
                mailchimp_list_choices.append((l['id'], l['name']))
            self.fields['mailchimp_list'].choices = mailchimp_list_choices
            self.fields['mailchimp_list'].initial = self.instance.mailchimp_id


class MListAdmin(admin.ModelAdmin):
    form = MListAdminForm
    list_display = (
        'id', 'title', 'get_mailchimp_list', 'last_sync', 'language',
        'is_public'
    )
    list_display_links = ('id', 'title')
    list_filter = (
        'language',
        'is_public',
    )
    fieldsets = [
        (None, {
            'fields': ('site', 'mailchimp_list')
        }),
    ]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': (
                'language',
                'is_public',
            )
        }),
    ]
    save_on_top = True

    def save_model(self, request, obj, form, change):
        super(MListAdmin, self).save_model(request, obj, form, change)

        obj.mailchimp_id = form.cleaned_data['mailchimp_list']

    def get_mailchimp_list(self, obj):
        if not hasattr(self, "_mailchimp_lists"):
            from mailchimp3 import MailChimp
            Settings = apps.get_model("mailchimp", "Settings")
            try:
                st = Settings.objects.get()
            except:
                pass
            else:
                mailchimp_client = MailChimp(st.username, st.api_key)
                data = mailchimp_client.lists.all(
                    get_all=True, fields="lists.id,lists.name"
                )
                self._mailchimp_lists = {}
                for l in data['lists']:
                    self._mailchimp_lists[l['id']] = l['name']

        if obj.mailchimp_id:
            return self._mailchimp_lists[obj.mailchimp_id]

    get_mailchimp_list.short_description = _("MailChimp List")


admin.site.register(MList, MListAdmin)


class MailingContentBlockForm(forms.ModelForm):
    content_type = forms.ChoiceField(
        label=_("Content Type"),
        choices=[('', '---------')] + list(CONTENT_TYPE_CHOICES),
        required=True,
    )

    class Meta:
        model = MailingContentBlock
        fields = '__all__'


class MailingContentBlockInline(ExtendedStackedInline):
    model = MailingContentBlock
    form = MailingContentBlockForm
    extra = 0
    fieldsets = [
        (
            _("Content"), {
                'fields': ['content_type', 'content', 'sort_order'],
                'classes': ('grp-collapse grp-open', )
            }
        )
    ]
    ordering = ("sort_order", )
    sortable = True
    sortable_field_name = "sort_order"
    classes = ('grp-collapse grp-open', )
    inline_classes = ('grp-collapse grp-open', )


class CampaignAdmin(ExtendedModelAdmin):
    list_display = (
        'subject', 'get_mailinglist_with_link', 'get_preview_link', 'get_status'
    )
    list_filter = ('mailinglist', )
    fieldsets = [
        (
            None, {
                'fields':
                    ('sender_name', 'sender_email', 'mailinglist', 'template')
            }
        ),
    ]
    fieldsets += [(_("Content"), {'fields': ['subject', 'body_html']})]
    inlines = (MailingContentBlockInline, )

    save_on_top = True

    def get_urls(self):
        urls = super(CampaignAdmin, self).get_urls()
        my_urls = patterns(
            '',
            (
                r'^template-content/(?P<template_name>[^/]+)/$',
                self.admin_site.admin_view(self.template_content)
            ),
            (r'^(.+)/preview/$', self.admin_site.admin_view(self.preview)),
        )
        return my_urls + urls

    def template_content(self, request, template_name):
        from django.shortcuts import render_to_response
        return render(
            request, "mailchimp/campaign/includes/%s.html" % template_name, {}
        )

    def preview(self, request, object_id):
        obj = self.get_object(request, unquote(object_id))
        html = obj.get_rendered_html()
        return HttpResponse(html)

    def get_preview_link(self, obj):
        return '<a href="%d/preview/" target="_blank">%s</a>' % (
            obj.pk, ugettext("Preview")
        )

    get_preview_link.short_description = _("Preview")
    get_preview_link.allow_tags = True

    def get_status(self, obj):
        is_sent = obj.is_sent()
        if is_sent is None:
            return _("Unknown (probably deleted)")
        return _("Sent") if is_sent else _("Draft")

    get_status.short_description = _("Status")

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.is_sent():
            messages.warning(
                request,
                _(
                    """Campaign "%s" was not updated at MailChimp, because it has been sent."""
                ) % unicode(obj)
            )


admin.site.register(Campaign, CampaignAdmin)
