# -*- coding: UTF-8 -*-
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, get_language, activate
from django.http import HttpResponseRedirect, HttpResponse
from functools import update_wrapper
from django.utils.encoding import force_unicode
from django.utils.text import capfirst, get_text_list
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template, Context
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.forms.util import ErrorList

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/')
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline

from jetson.apps.people.functions import get_user_language
from jetson.apps.email_campaigns.models import InfoSubscription, Campaign, MailingList, Mailing, MailingContentBlock
from jetson.apps.mailing.models import EmailMessage
from jetson.apps.history.models import ExtendedLogEntry
from jetson.apps.history.default_settings import A_CUSTOM1, AS_PUBLIC

class InfoSubscriptionAdminForm(forms.ModelForm):
    class Meta:
        model = InfoSubscription
        exclude = ()

    def clean(self, *args, **kwargs):
        cleaned = super(InfoSubscriptionAdminForm, self).clean(*args, **kwargs)
        if not cleaned.get("subscriber", None) and not cleaned.get("email", ""):
            self._errors['email'] = ErrorList([_("Either subscriber or subscriber email should be filled in.")])
        return cleaned

class InfoSubscriptionOptions(admin.ModelAdmin):
    form = InfoSubscriptionAdminForm
    list_display = ('subscriber_name', 'email', 'get_mailinglist_with_link', 'creation_date')
    list_filter = ('mailinglist',)
    search_fields = ('subscriber_name', 'email',)
    fieldsets = (
        (None, {'fields': ("mailinglist", "subscriber", "subscriber_name", "email", "ip")}),
        )
    save_on_top = True

admin.site.register(InfoSubscription, InfoSubscriptionOptions)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_mailinglists_with_link',)
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    save_on_top = True

admin.site.register(Campaign, CampaignAdmin)


class MailingListAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_campaign_with_link', 'get_count_with_link',)
    list_filter = ('campaign',)
    fieldsets = [(None, {'fields': ('site','campaign',)}),]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('is_public',)}),]
    save_on_top = True

admin.site.register(MailingList, MailingListAdmin)


class MailingContentBlockInline(ExtendedStackedInline):
    model = MailingContentBlock
    extra = 1
    fieldsets = get_admin_lang_section(_("Content"), ['topic', 'title', 'text',], default_expanded=True)
    fieldsets += [(None, {'fields': ('image', 'link',)})]

class MailingAdmin(ExtendedModelAdmin):
    list_display = ('subject', 'get_mailinglists_with_links', 'status',)
    list_filter = ('mailinglists',)
    fieldsets = [(None, {'fields': ('sender_name', 'sender_email', 'mailinglists', 'template', 'status',)}),]
    fieldsets += get_admin_lang_section(_("Content"), ['subject', 'body_html'], default_expanded=True)
    inlines = (MailingContentBlockInline,)
    radio_fields = {
        'status': admin.HORIZONTAL,
    }
    
    save_on_top = True
    
    # callback for the additional buttons (overwritten method)
    def add_get_additional_buttons_callback(self):
        return self.change_get_additional_buttons_callback()
    
    # callback for the additional buttons actions (overwritten method)
    def add_handle_button_action_callback(self, action, obj):
        self.change_handle_button_action_callback(action, obj)

    # callback for the additional buttons (overwritten method)
    def change_get_additional_buttons_callback(self):
        return [('send', _('Save and send'))]
    
    # callback for the additional buttons actions (overwritten method)
    def change_handle_button_action_callback(self, action, obj):
        if obj:
            if action == 'send':
                return HttpResponseRedirect(reverse(
                    'admin:%s_%s_send' % (
                        self.model._meta.app_label, self.model._meta.module_name,
                        ),
                    args=[obj.id],
                    ))
    
    def get_urls(self):
        from django.conf.urls import patterns, url
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        
        urls = patterns('',
            url(r'^(.+)/send/$',
                wrap(self.send_view),
                name='%s_%s_send' % info),
            url(r'^(.+)/preview/$',
                wrap(self.preview_view),
                name='%s_%s_preview' % info),
        )
        urls += super(MailingAdmin, self).get_urls()
        return urls
        
    #@never_cache # doesn't work for class methods with django r11611
    def send_view(self, request, object_id, extra_context=None):
        obj = Mailing.objects.get(pk=object_id)
        if request.POST.has_key('mailing_action'):
            template = get_template(obj.template)
            
            if request.POST['mailing_action'] == 'test':
                
                from re import split
                recipients = split('\s*,\s*', request.POST['recipients'])
                
                for recipient in recipients:
                    context = {
                        'mailing': obj,
                        'recipient': recipient,
                        'language': get_user_language(request.user),
                    }
                    rendered_body = template.render(RequestContext(request, context))
                    message = EmailMessage.objects.create(
                        # sender=sender,
                        # recipient=recipient,
                        sender_name=obj.sender_name,
                        sender_email=obj.sender_email,
                        recipient_emails=recipient,
                        subject="%s [TEST]" % obj.subject,
                        body_html=rendered_body,
                        delete_after_sending=True
                    )
                    message.save()
                self.message_user(request, _("Mailing was sent out to %(count)s recipients (test transmission)") % { 'count': len(recipients) })
                ExtendedLogEntry.objects.create(
                    object_id=obj.id,
                    content_type_id=ContentType.objects.get_for_model(Mailing).pk,
                    user=request.user, 
                    object_repr=unicode(obj), 
                    action_flag=A_CUSTOM1, 
                    change_message=_("Mailing was sent out to %(count)s recipients (test transmission)") % { 'count': len(recipients) }, 
                    scope=AS_PUBLIC)
                return HttpResponseRedirect('../../')
                
            if request.POST['mailing_action'] == 'real':
                current_lang = get_language()
                recipients = []
                for mailinglist in obj.mailinglists.all():
                    recipients += mailinglist.infosubscription_set.all()
                # TODO: we still need to remove duplicates!
                
                for recipient in recipients:
                    try:
                        language = get_user_language(recipient.subscriber)
                    except:
                        language = settings.LANGUAGE_CODE
                    activate(language)

                    context = {
                        'mailing': obj,
                        'recipient': recipient,
                        'language': language,
                    }
                    rendered_body = template.render(RequestContext(request, context))
                    message = EmailMessage.objects.create(
                        # sender=sender,
                        recipient=recipient.subscriber,
                        sender_name=obj.sender_name,
                        sender_email=obj.sender_email,
                        recipient_emails=recipient.email,
                        subject=obj.subject,
                        body_html=rendered_body,
                        delete_after_sending=True
                    )
                    message.save()
                
                activate(current_lang)
                
                from jetson.apps.email_campaigns.models import MAILING_STATUS_SENT
                obj.status = MAILING_STATUS_SENT
                obj.save()
                
                self.message_user(request, _("Mailing was sent out to %(count)s recipients (real transmission)") % { 'count': len(recipients)})
                ExtendedLogEntry.objects.create(
                    object_id=obj.id,
                    content_type_id=ContentType.objects.get_for_model(Mailing).pk,
                    user=request.user, 
                    object_repr=unicode(obj), 
                    action_flag=A_CUSTOM1, 
                    change_message=_("Mailing was sent out to %(count)s recipients (real transmission)") % { 'count': len(recipients) }, 
                    scope=AS_PUBLIC)
                return HttpResponseRedirect('../../')
        
        context = {
            'title': _('Send mailing: %s') % force_unicode(obj),
            'module_name': capfirst(force_unicode(Mailing._meta.verbose_name_plural)),
            'object': obj,
            'root_path': self.admin_site.root_path,
            'app_label': Mailing._meta.app_label,
        }
        return render_to_response('admin/email_campaigns/mailing_send_prepare.html', context, context_instance=RequestContext(request))
    
    
    
    def preview_view(self, request, object_id, extra_context=None):
        obj = Mailing.objects.get(pk=object_id)
        template = get_template(obj.template)
        
        context = {
            'mailing': obj,
            'recipient': request.user,
            'language': get_language(),
        }
        html = template.render(RequestContext(request, context))
        return HttpResponse(html)

admin.site.register(Mailing, MailingAdmin)
