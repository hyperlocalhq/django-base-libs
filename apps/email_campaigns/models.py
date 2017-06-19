# -*- coding: UTF-8 -*-
import re

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.utils.encoding import smart_str, force_unicode
from django.conf import settings
from django.core.urlresolvers import reverse

from filebrowser.fields import FileBrowseField

from base_libs.models import SingleSiteMixin, CreationModificationDateMixin, CreationModificationMixin
from base_libs.models import PlainTextModelField
from base_libs.models import ExtendedTextField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import TemplatePathField
from base_libs.utils.user import get_user_title

verbose_name = _("Email Campaigns")

class InfoSubscription(CreationModificationDateMixin):
    subscriber = models.ForeignKey(User, verbose_name=_("Subscriber"), null=True, blank=True)
    subscriber_name = models.CharField(_("Subscriber's name"), max_length=200, blank=True)
    email = models.EmailField(_("Email address"), blank=True)
    ip = models.IPAddressField(_("IP Address"), blank=True)
    mailinglist = models.ForeignKey('MailingList', verbose_name=_("Mailing list"))
    
    class Meta:
        verbose_name = _("info subscription")
        verbose_name_plural = _("info subscriptions")
        ordering = ['email']
    
    def get_mailinglist_with_link(self):
        return '<a href="%(link)s" class="cross_link">%(mailinglist)s</a>' % {
            'link': reverse(
                'admin:%s_%s_change' % (
                    MailingList._meta.app_label,
                    MailingList._meta.module_name,
                    ),
                args=[self.mailinglist.pk],
                ),
            'mailinglist': self.mailinglist,
            }
    get_mailinglist_with_link.short_description = _("Mailing list")
    get_mailinglist_with_link.allow_tags = True
        
    def save(self, *args, **kwargs):
        if self.subscriber:
            self.subscriber_name = self.subscriber_name or get_user_title(self.subscriber)
            self.email = self.email or self.subscriber.email
        super(InfoSubscription, self).save(*args, **kwargs)
    save.alters_data = True
        
    def __unicode__(self):
        return force_unicode(self.email)


class Campaign(models.Model):
    title = MultilingualCharField(_("Title"), max_length=255)
    
    def __unicode__(self):
        return self.title
    
    def get_mailinglists_with_link(self):
        count = self.mailinglist_set.count()
        if not count:
            return _("None")
        return '%(count)s &nbsp; <a href="%(link)s?campaign__id__exact=%(campaign_id)s" class="cross_link">%(linktext)s</a>' % {
            'count': count,
            'link': reverse(
                'admin:%s_%s_changelist' % (
                    MailingList._meta.app_label,
                    MailingList._meta.module_name,
                    )
                ),
            'campaign_id': self.pk,
            'linktext': _("Show mailing lists"),
            }
    get_mailinglists_with_link.short_description = _("Mailing Lists")
    get_mailinglists_with_link.allow_tags = True
    
    class Meta:
        ordering = ('title',)


class MailingList(SingleSiteMixin):
    campaign = models.ForeignKey('Campaign', verbose_name=_("Campaign"), blank=True, null=True)
    title = MultilingualCharField(_("Title"), max_length=255)
    is_public = models.BooleanField(_('Will this mailing list be displayed in the public settings of subscriptions?'), default=True)
    
    def get_count(self):
        return self.infosubscription_set.count()
    get_count.short_description = _("Number of recipients")
    
    def get_count_with_link(self):
        count = self.get_count()
        if not count:
            return count
        return '%(count)s &nbsp; <a href="%(link)s?mailinglist__id__exact=%(mailinglist_id)s" class="cross_link">%(linktext)s</a>' % {
            'count': count,
            'link': reverse(
                'admin:%s_%s_changelist' % (
                    InfoSubscription._meta.app_label,
                    InfoSubscription._meta.module_name,
                    )
                ),
            'mailinglist_id': self.pk,
            'linktext': _("Show recipients"),
            }
    get_count_with_link.short_description = _("Number of recipients")
    get_count_with_link.allow_tags = True
    
    def get_campaign_with_link(self):
        return '<a href="%(link)s" class="cross_link">%(campaign)s</a>' % {
            'link': reverse(
                'admin:%s_%s_change' % (
                    Campaign._meta.app_label,
                    Campaign._meta.module_name
                    ),
                args=[self.campaign.pk],
                ),
            'campaign': self.campaign,
            }
    get_campaign_with_link.short_description = _("Campaign")
    get_campaign_with_link.allow_tags = True
    
    def get_admin_change_url(self):
        return reverse(
            'admin:%s_%s_change' % (
                self._meta.app_label,
                self._meta.module_name,
                ),
            args=[self.pk],
            )
    
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.campaign)
    
    class Meta:
        ordering = ('title', 'campaign',)


MAILING_STATUS_DRAFT = 1
MAILING_STATUS_SENT = 2

MAILING_STATUS_CHOICES = (
    (MAILING_STATUS_DRAFT, _("Draft")),
    (MAILING_STATUS_SENT, _("Sent")),
)

class Mailing(CreationModificationMixin):
    sender_name = models.CharField(_("Sender name"),  null=True, blank=True, max_length=255, default=getattr(settings, 'MAILING_DEFAULT_FROM_NAME', ''))
    sender_email = models.EmailField(_("Sender email"), null=True, blank=True, default=getattr(settings, 'MAILING_DEFAULT_FROM_EMAIL', ''))
    subject = MultilingualCharField(_("Subject"), max_length=255, blank=True)
    body_html = MultilingualTextField(_("Message"), blank=True)
    mailinglists = models.ManyToManyField('MailingList', verbose_name=_("Mailing lists"))
    template = TemplatePathField(_("Template"), path="email_campaigns/mailing/", match="\.html$")
    status = models.PositiveIntegerField(_("Status"), choices=MAILING_STATUS_CHOICES, default=MAILING_STATUS_DRAFT)
    
    def __unicode__(self):
        return self.subject
    
    def is_sent(self):
        return self.status == MAILING_STATUS_SENT
    
    def get_mailinglists(self):
        return ', '.join(self.mailinglists.values_list('title', flat=True))
    get_mailinglists.short_description = _("Mailing List(s)")
    
    def get_mailinglists_with_links(self):
        mailinglists = self.mailinglists.all()
        r = ''
        for mailinglist in mailinglists:
            r += '<div><a href="%(link)s" class="cross_link">%(name)s</a> (%(count)s recipients)</div>' % {
                'link': reverse(
                    'admin:%s_%s_change' % (
                        MailingList._meta.app_label,
                        MailingList._meta.module_name,
                        ),
                    args=[mailinglist.pk],
                    ),
                'name': mailinglist.title,
                'count': mailinglist.get_count(),
                }
        return r
    get_mailinglists_with_links.allow_tags = True
    get_mailinglists_with_links.short_description = _("Mailing lists")
    
    def get_admin_preview_url(self):
        return reverse(
            'admin:%s_%s_preview' % (
                self._meta.app_label,
                self._meta.module_name,
                ),
            args=[self.pk],
            )

    # class Meta:
    #     ordering = ('-timestamp',)


class MailingContentBlock(models.Model):
    topic = MultilingualCharField(_("Topic"), max_length=255, blank=True)
    title = MultilingualCharField(_("Title"), max_length=255, blank=True)
    text = MultilingualTextField(_("Text"), blank=True)
    image = FileBrowseField(_("Image"), max_length=255, directory="newsletter/", extensions=['.jpg', '.jpeg', '.gif','.png'], blank=True)
    link = models.URLField(_("Link"), blank=True)
    mailing = models.ForeignKey('Mailing')
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Content Block")
        verbose_name_plural = _("Content Blocks")
