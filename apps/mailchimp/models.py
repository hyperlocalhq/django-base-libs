# -*- coding: UTF-8 -*-
import re
from mailsnake import MailSnake, CampaignInvalidStatusException

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_str, force_unicode
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from filebrowser.fields import FileBrowseField

from base_libs.models import SingleSiteMixin, CreationModificationDateMixin, CreationModificationMixin
from base_libs.models import PlainTextModelField
from base_libs.models import ExtendedTextField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import TemplatePathField
from base_libs.utils.user import get_user_title
from base_libs.models.fields import PositionField

verbose_name = _("MailChimp")

INFOSUBSCRIPTION_STATUS_CHOICES = (
    ("pending", _("Pending")),
    ("subscribed", _("Subscribed")),
    ("unsubscribed", _("Unsubscribed")),
    )

class Settings(models.Model):
    api_key = models.CharField(_("API key"), max_length=200, blank=True)
    double_optin = models.BooleanField(_("Double Optin"), default=True, help_text=_("Flag to control whether a double opt-in confirmation message is sent. ABUSING THIS MAY CAUSE YOUR ACCOUNT TO BE SUSPENDED."))
    update_existing = models.BooleanField(_("Update existing"), default=False, help_text=_("Flag to congtrol whether the existing subscribers should be updated instead of throwing an error."))
    send_welcome = models.BooleanField(_("Send welcome"), default=False, help_text=_("If double optin is false and this is true, MailChimp will send a welcome message to new subscribers."))
    delete_member = models.BooleanField(_("Delete member"), default=False, help_text=_("Flag to completely delete the member from the list instead of just unsubscribing"))
    send_goodbye = models.BooleanField(_("Send goodbye"), default=True, help_text=_("Flag to send the goodbye message to the email address."))

    class Meta:
        verbose_name = _("MailChimp Settings")
        verbose_name_plural = _("MailChimp Settings")
        ordering = ['api_key']

    def __unicode__(self):
        return force_unicode(self.api_key)

class Subscription(CreationModificationDateMixin):
    subscriber = models.ForeignKey(User, verbose_name=_("Subscriber"), null=True, blank=True)
    first_name = models.CharField(_("First name"), max_length=200, blank=True)
    last_name = models.CharField(_("Last name"), max_length=200, blank=True)
    email = models.EmailField(_("Email address"), blank=True)
    ip = models.IPAddressField(_("IP Address"), blank=True)
    mailinglist = models.ForeignKey('MList', verbose_name=_("Mailing list"))
    status = models.CharField(_("Status"), max_length=200, blank=True, choices=INFOSUBSCRIPTION_STATUS_CHOICES)
    
    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")
        ordering = ['email']
    
    def get_mailinglist_with_link(self):
        return '<a href="%(link)s" class="cross_link">%(mailinglist)s</a>' % {
            'link': reverse(
                'admin:%s_%s_change' % (
                    MList._meta.app_label,
                    MList._meta.module_name,
                    ),
                args=[self.mailinglist.pk],
                ),
            'mailinglist': self.mailinglist,
            }
    get_mailinglist_with_link.short_description = _("Mailing list")
    get_mailinglist_with_link.allow_tags = True
        
    def save(self, *args, **kwargs):
        if self.subscriber:
            self.first_name = self.subscriber.first_name
            self.last_name = self.subscriber.last_name
            self.email = self.email or self.subscriber.email
        super(Subscription, self).save(*args, **kwargs)
    save.alters_data = True
        
    def __unicode__(self):
        return force_unicode(self.email)


class MList(SingleSiteMixin):
    title = MultilingualCharField(_("Title"), max_length=255)
    is_public = models.BooleanField(_("Public"), help_text=_('Will this mailing list be displayed in the public settings of subscriptions?'), default=True)
    last_sync = models.DateTimeField(_("Last sync"), blank=True, null=True)
    
    class Meta:
        verbose_name = _("Mailing List")
        verbose_name_plural = _("Mailing Lists")
        ordering = ["title"]
        
    def get_count(self):
        return self.subscription_set.count()
    get_count.short_description = _("Number of recipients")
    
    def get_count_with_link(self):
        count = self.get_count()
        if not count:
            return count
        return '%(count)s &nbsp; <a href="%(link)s?mailinglist__id__exact=%(mailinglist_id)s" class="cross_link">%(linktext)s</a>' % {
            'count': count,
            'link': reverse(
                'admin:%s_%s_changelist' % (
                    Subscription._meta.app_label,
                    Subscription._meta.module_name,
                    )
                ),
            'mailinglist_id': self.pk,
            'linktext': _("Show recipients"),
            }
    get_count_with_link.short_description = _("Number of recipients")
    get_count_with_link.allow_tags = True
    
    def get_admin_change_url(self):
        return reverse(
            'admin:%s_%s_change' % (
                self._meta.app_label,
                self._meta.module_name,
                ),
            args=[self.pk],
            )
    
    def __unicode__(self):
        return self.title
    
    def _get_mailchimp_id(self):
        if not hasattr(self, "_mailchimp_id"):
            Service = models.get_model("external_services", "Service")
            s, created = Service.objects.get_or_create(
                sysname="mailchimp",
                defaults={
                    'url': "http://api.mailchimp.com/",
                    'title': "MailChimp",
                    },
                )
            try:
                mapper = s.objectmapper_set.get(
                    content_type__app_label="mailchimp",
                    content_type__model="mlist",
                    object_id=self.pk,
                    )
            except:
                self._mailchimp_id = None
            else:
                self._mailchimp_id = mapper.external_id
        return self._mailchimp_id
        
    def _set_mailchimp_id(self, value):
        Service = models.get_model("external_services", "Service")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        s, created = Service.objects.get_or_create(
            sysname="mailchimp",
            defaults={
                'url': "http://api.mailchimp.com/",
                'title': "MailChimp",
                },
            )

        s.objectmapper_set.filter(
            content_type__app_label="mailchimp",
            content_type__model="mlist",
            object_id=self.pk,
            ).delete()
        if value:
            mapper = ObjectMapper(
                service=s,
                external_id=value,
                )
            mapper.content_object = self
            mapper.save()
        self._mailchimp_id = value
        
    mailchimp_id = property(_get_mailchimp_id, _set_mailchimp_id)


class Campaign(CreationModificationMixin):
    sender_name = models.CharField(_("Sender name"), max_length=255, default=getattr(settings, 'MAILING_DEFAULT_FROM_NAME', ''))
    sender_email = models.EmailField(_("Sender email"), default=getattr(settings, 'MAILING_DEFAULT_FROM_EMAIL', ''))
    subject = models.CharField(_("Subject"), max_length=255)
    body_html = ExtendedTextField(_("Message"), blank=True)
    mailinglist = models.ForeignKey('MList', verbose_name=_("Mailing list"))
    template = TemplatePathField(_("Template"), path="mailchimp/campaign/", match="\.html$")
    sent = models.BooleanField(_("Sent"), default=False, editable=False)

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")
        ordering = ('-creation_date',)

    def __unicode__(self):
        return self.subject
    
    def is_sent(self):
        if self.sent:
            return True
        if not self.mailchimp_id:
            return False

        try:
            st = Settings.objects.get()
        except:
            return False
        ms = MailSnake(st.api_key)
        response_dict = ms.campaigns(filters={'campaign_id': self.mailchimp_id})
        sent = response_dict['data'][0]['status'] == "sent"
        if sent:
            Campaign.objects.filter(pk=self.pk).update(sent=True)
        return sent
    
    def get_mailinglist(self):
        return self.mailinglist.title
    get_mailinglist.short_description = _("Mailing List")
    
    def get_mailinglist_with_link(self):
        r = '<div><a href="%(link)s" class="cross_link">%(name)s</a> (%(count)s recipients)</div>' % {
            'link': reverse(
                'admin:%s_%s_change' % (
                    MList._meta.app_label,
                    MList._meta.module_name,
                    ),
                args=[self.mailinglist.pk],
                ),
            'name': self.mailinglist.title,
            'count': self.mailinglist.get_count(),
            }
        return r
    get_mailinglist_with_link.allow_tags = True
    get_mailinglist_with_link.short_description = _("Mailing list")
    
    def get_admin_preview_url(self):
        return reverse(
            'admin:%s_%s_preview' % (
                self._meta.app_label,
                self._meta.module_name,
                ),
            args=[self.pk],
            )

    def _get_mailchimp_id(self):
        if not hasattr(self, "_mailchimp_id"):
            Service = models.get_model("external_services", "Service")
            s, created = Service.objects.get_or_create(
                sysname="mailchimp",
                defaults={
                    'url': "http://api.mailchimp.com/",
                    'title': "MailChimp",
                    },
                )
            try:
                mapper = s.objectmapper_set.get(
                    content_type__app_label="mailchimp",
                    content_type__model="campaign",
                    object_id=self.pk,
                    )
            except:
                self._mailchimp_id = None
            else:
                self._mailchimp_id = mapper.external_id
        return self._mailchimp_id
        
    def _set_mailchimp_id(self, value):
        Service = models.get_model("external_services", "Service")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        s, created = Service.objects.get_or_create(
            sysname="mailchimp",
            defaults={
                'url': "http://api.mailchimp.com/",
                'title': "MailChimp",
                },
            )

        s.objectmapper_set.filter(
            content_type__app_label="mailchimp",
            content_type__model="campaign",
            object_id=self.pk,
            ).delete()
        if value:
            mapper = ObjectMapper(
                service=s,
                external_id=value,
                )
            mapper.content_object = self
            mapper.save()
        self._mailchimp_id = value
        
    mailchimp_id = property(_get_mailchimp_id, _set_mailchimp_id)

    def get_rendered_html(self):
        from django.template.loader import get_template, Context
        from filebrowser.settings import MEDIA_URL as UPLOADS_URL
        from base_libs.utils.misc import get_website_url
        
        template = get_template(self.template)
        return template.render(Context({
            'campaign': self,
            'media_url': settings.MEDIA_URL,
            'jetson_media_url': settings.JETSON_MEDIA_URL,
            'website_url': get_website_url(),
            'UPLOADS_URL': UPLOADS_URL,
            }))


def save_mailchimp_campaign(sender, **kwargs):
    instance = kwargs['instance']
    ct = ContentType.objects.get_for_model(Campaign)
    if ct.id == instance.content_type.id:
        if instance.is_addition() or instance.is_change():
            campaign = instance.get_edited_object()
            
            Settings = models.get_model("mailchimp", "Settings")
            
            try:
                st = Settings.objects.get()
            except:
                return

            ms = MailSnake(st.api_key)
                
            html = campaign.get_rendered_html()

            if campaign.mailchimp_id:
                try:
                    ms.campaignUpdate(
                        cid=campaign.mailchimp_id,
                        name="list_id",
                        value=campaign.mailinglist.mailchimp_id,
                        )
                    ms.campaignUpdate(
                        cid=campaign.mailchimp_id,
                        name="subject",
                        value=campaign.subject,
                        )
                    ms.campaignUpdate(
                        cid=campaign.mailchimp_id,
                        name="title",
                        value=campaign.subject,
                        )
                    ms.campaignUpdate(
                        cid=campaign.mailchimp_id,
                        name="from_email",
                        value=campaign.sender_email,
                        )
                    ms.campaignUpdate(
                        cid=campaign.mailchimp_id,
                        name="from_name",
                        value=campaign.sender_name,
                        )
                    ms.campaignUpdate(
                        cid=campaign.mailchimp_id,
                        name="content",
                        value={
                            'html': html,
                            'text': ms.generateText(type="html", content=html),
                            },
                        )
                except CampaignInvalidStatusException:
                    pass
            else:
                campaign.mailchimp_id = ms.campaignCreate(
                    type="regular",
                    options={
                        'list_id': campaign.mailinglist.mailchimp_id,
                        'subject': campaign.subject,
                        'from_email': campaign.sender_email,
                        'from_name': campaign.sender_name,
                        'to_name': u"*|FNAME|* *|LNAME|*",
                        },
                    content={
                        'html': html,
                        'text': ms.generateText(type="html", content=html),
                        }
                    )
post_save.connect(save_mailchimp_campaign, sender=LogEntry)

CONTENT_TYPE_CHOICES = getattr(settings, "MAILING_CONTENT_TYPE_CHOICES", (
    ('image_and_text', _("Image and text")),
    ('text', _("Text only")),
    ))

class MailingContentBlock(models.Model):
    campaign = models.ForeignKey('Campaign')
    content_type = models.CharField('Content Type', max_length=20, choices=CONTENT_TYPE_CHOICES, blank=True)
    content = ExtendedTextField(_("Content"), blank=True)
    sort_order = PositionField(_("Sort order"))
    
    def __unicode__(self):
        return self.get_content_type_display()
    
    class Meta:
        ordering = ("sort_order",)
        verbose_name = _("Content Block")
        verbose_name_plural = _("Content Blocks")
    
    def save(self, *args, **kwargs):
        from base_libs.models.base_libs_settings import MARKUP_HTML_WYSIWYG
        if not self.content and self.content_type:
            self.content = self.get_content_from_template()
            self.content_markup_type = MARKUP_HTML_WYSIWYG
        super(MailingContentBlock, self).save(*args, **kwargs)

    def get_content_from_template(self):
        from django.template.loader import render_to_string
        return render_to_string(
            "mailchimp/campaign/includes/%s.html" % self.content_type,
            {
                'campaign': self.campaign,
                'block': self,
                },
            )

