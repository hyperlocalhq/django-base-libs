# -*- coding: UTF-8 -*-
import os
from mailchimp3 import MailChimp
from requests import HTTPError

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from base_libs.models import SingleSiteMixin, CreationModificationDateMixin, CreationModificationMixin
from base_libs.models import ExtendedTextField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import TemplatePathField
from base_libs.models.fields import PositionField

verbose_name = _("MailChimp")


class Settings(models.Model):
    username = models.CharField(_("Username"), max_length=200, blank=True)
    api_key = models.CharField(_("API key"), max_length=200, blank=True)
    double_optin = models.BooleanField(_("Double Optin"), default=True, help_text=_("Flag to control whether a double opt-in confirmation message is sent. ABUSING THIS MAY CAUSE YOUR ACCOUNT TO BE SUSPENDED."))

    class Meta:
        verbose_name = _("MailChimp Settings")
        verbose_name_plural = _("MailChimp Settings")
        ordering = ['api_key']

    def __unicode__(self):
        return force_unicode(self.api_key)


class MList(SingleSiteMixin):
    title = MultilingualCharField(_("Title"), max_length=255)
    is_public = models.BooleanField(_("Public"), help_text=_('Will this mailing list be displayed in the public settings of subscriptions?'), default=True)
    last_sync = models.DateTimeField(_("Last sync"), blank=True, null=True)
    language = models.CharField(_("Language of the newsletter"), max_length=5, choices=settings.LANGUAGES, blank=True)

    class Meta:
        verbose_name = _("Mailing List")
        verbose_name_plural = _("Mailing Lists")
        ordering = ["title"]
        
    def get_admin_change_url(self):
        return reverse(
            'admin:%s_%s_change' % (
                self._meta.app_label,
                self._meta.model_name,
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
    template = TemplatePathField(_("Template"), path='mailchimp/campaign/', match=r'.+\.html$')
    sent = models.BooleanField(_("Sent"), default=False, editable=False)

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")
        ordering = ('-creation_date',)

    def __unicode__(self):
        return self.subject
    
    def is_sent(self):
        """
        Checks if the campaign was sent and if so, saves the status to the database.

        :return: True if the campaign has been sent; False if the campaign has not been sent; or None if status is unknown.
        """
        if self.sent:
            return True
        if not self.mailchimp_id:
            return None

        try:
            st = Settings.objects.get()
        except:
            return None
        mailchimp_client = MailChimp(st.username, st.api_key)
        try:
            data = mailchimp_client.campaigns.get(campaign_id=self.mailchimp_id)
        except HTTPError:
            return None
        sent = data['status'] == "sent"
        if sent:
            Campaign.objects.filter(pk=self.pk).update(sent=True)
        return sent
    
    def get_mailinglist(self):
        return self.mailinglist.title
    get_mailinglist.short_description = _("Mailing List")
    
    def get_mailinglist_with_link(self):
        r = '<div><a href="%(link)s" class="cross_link">%(name)s</a></div>' % {
            'link': reverse(
                'admin:%s_%s_change' % (
                    MList._meta.app_label,
                    MList._meta.model_name,
                ),
                args=[self.mailinglist.pk],
            ),
            'name': self.mailinglist.title,
        }
        return r
    get_mailinglist_with_link.allow_tags = True
    get_mailinglist_with_link.short_description = _("Mailing list")
    
    def get_admin_preview_url(self):
        return reverse(
            'admin:%s_%s_preview' % (
                self._meta.app_label,
                self._meta.model_name,
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
        from django.template.loader import get_template
        from filebrowser.settings import MEDIA_URL as UPLOADS_URL
        from base_libs.utils.misc import get_website_url
        
        template = get_template(self.template)
        return template.render({
            'campaign': self,
            'media_url': settings.MEDIA_URL,
            'jetson_media_url': settings.JETSON_MEDIA_URL,
            'website_url': get_website_url(),
            'UPLOADS_URL': UPLOADS_URL,
        })


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

            mailchimp_client = MailChimp(st.username, st.api_key)
                
            html = campaign.get_rendered_html()

            if campaign.mailchimp_id:
                try:
                    mailchimp_client.campaigns.update(
                        campaign_id=campaign.mailchimp_id,
                        data={
                            'recipients': {
                                'list_id': campaign.mailinglist.mailchimp_id,
                            },
                            'settings': {
                                'subject_line': campaign.subject,
                                'from_name': campaign.sender_name,
                                'from_email': campaign.sender_email,
                                'reply_to': campaign.sender_email,
                                'to_name': u"*|FNAME|* *|LNAME|*",
                            },
                        }
                    )
                except HTTPError:
                    return
                try:
                    mailchimp_client.campaigns.content.update(
                        campaign_id=campaign.mailchimp_id,
                        data={
                            'html': html,
                        }
                    )
                except HTTPError:
                    return
            else:
                response = mailchimp_client.campaigns.create(data={
                    'type': "regular",
                    'recipients': {
                        'list_id': campaign.mailinglist.mailchimp_id,
                    },
                    'settings': {
                        'subject_line': campaign.subject,
                        'from_name': campaign.sender_name,
                        'from_email': campaign.sender_email,
                        'reply_to': campaign.sender_email,
                        'to_name': u"*|FNAME|* *|LNAME|*",
                    },
                })
                campaign.mailchimp_id = response['id']
                mailchimp_client.campaigns.content.update(
                    campaign_id=campaign.mailchimp_id,
                    data={
                        'html': html,
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
