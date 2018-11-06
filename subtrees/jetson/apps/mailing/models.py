# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import linebreaks, urlize
from django.contrib.auth.models import User
from django.utils.encoding import smart_str, force_unicode
from django.conf import settings

from base_libs.utils.misc import html_to_plain_text
from base_libs.utils.misc import get_translation
from base_libs.models import SingleSiteMixin
from base_libs.models import SlugMixin
from base_libs.models import SysnameMixin
from base_libs.models import MultilingualCharField
from base_libs.models import PlainTextModelField
from base_libs.models import ExtendedTextField
from base_libs.models import CreationModificationMixin

from jetson.apps.mailing.mail import send_mail
from jetson.apps.history.models import custom_action_signal_1
from jetson.apps.history.models import custom_action_signal_2

verbose_name = _("Mailing")

PLACEHOLDER_RELATES_TO = (
    (1, _("Recipient")),
    (2, _("Sender")),
    (3, _("Object")),
    (4, _("Global")),
)


class EmailMessageManager(models.Manager):
    def send_mails(self):
        for item in self.filter(is_sent=False):
            item.send()


class EmailMessage(CreationModificationMixin):
    sender = models.ForeignKey(User, verbose_name=_("Sender"), null=True, blank=True, related_name="sent_by_message_set")
    recipient = models.ForeignKey(User, verbose_name=_("Recipient"), null=True, blank=True, related_name="received_by_message_set")
    sender_name = models.CharField(_("Sender name"),  null=True, blank=True, max_length=255)
    sender_email = models.EmailField(_("Sender email"), null=True, blank=True)
    recipient_emails = PlainTextModelField(_("Recipient email(s)"), null=True, blank=True)
    subject = models.CharField(_("Subject"), max_length=255, blank=True)
    body = PlainTextModelField(_("Message (Plain text)"), blank=True)
    body_html = ExtendedTextField(_("Message (HTML)"), blank=True)
    is_sent = models.BooleanField(_("Sent"), default=False)
    delete_after_sending = models.BooleanField(_("Delete after sending"), default=False)

    objects = EmailMessageManager()

    class Meta:
        verbose_name = _("email message")
        verbose_name_plural = _("email messages")
        ordering = ('-creation_date', 'subject',)
        
    def __unicode__(self):
        return "%s %s" % (self.creation_date, force_unicode(self.subject))
        
    def save(self, *args, **kwargs):
        if not self.body:
            self.body = html_to_plain_text(self.body_html)
        if not self.body_html:
            self.body_html = linebreaks(urlize(self.body))
        self.body_html = smart_str(self.body_html)
        self.body = smart_str(self.body)
        super(EmailMessage, self).save(*args, **kwargs)
    save.alters_data = True

    def send(self):
        try:
            send_mail(
                self.subject,
                self.body_html,
                u"%s <%s>" % (self.sender_name, self.sender_email),
                self.recipient_emails.split(","),
                plain_message=self.body,
            )
        except Exception as e:
            return False
        else:
            if self.sender:
                custom_action_signal_1.send(
                    sender=type(self),
                    instance=self,
                    user=self.sender,
                )
            if self.recipient:
                custom_action_signal_2.send(
                    sender=type(self),
                    instance=self,
                    user=self.recipient,
                )
            if self.delete_after_sending:
                self.delete()
            else:
                self.is_sent = True
                self.save()
        return True
    send.alters_data = True
    
    def get_log_message(self, language=None, action=None):
        """
        Gets a message for a specific action which will be logged for history """
        history_models = models.get_app("history")
        message = ""
        if action == history_models.A_CUSTOM1:
            message = get_translation("%(sender)s sent a message to %(recipient)s", language=language) % {
                'sender': (self.sender and [force_unicode(self.sender)] or [self.sender_name])[0],
                'recipient': (self.recipient and [force_unicode(self.recipient)] or [self.recipient_emails])[0],
            }
        elif action == history_models.A_CUSTOM2:
            message = get_translation("%(recipient)s received a message from %(sender)s", language=language) % {
                'sender': (self.sender and [force_unicode(self.sender)] or [self.sender_name])[0],
                'recipient': (self.recipient and [force_unicode(self.recipient)] or [self.recipient_emails])[0],
            }
        return message


class EmailTemplatePlaceholder(SysnameMixin(verbose_name=_("Placeholder Internal Name"), prepopulate_from=("name",))):
    
    name = MultilingualCharField(_('Placeholder Name'), max_length=64, unique=True)
    relates_to = models.IntegerField(_("relates to"), default=1, choices=PLACEHOLDER_RELATES_TO)
    help_text = models.CharField(_("Placeholder Help text"), max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(_("Written"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("email template placeholder")
        verbose_name_plural = _("email template placeholders")
        ordering = ['relates_to', 'name']
    
    def __unicode__(self):
        return " | ".join([getattr(self, "name_%s" % lang_code) for lang_code, lang_verbose in settings.LANGUAGES])


class EmailTemplate(SingleSiteMixin, SlugMixin(prepopulate_from=("name",))):
    owner = models.ForeignKey(User, verbose_name=_("Owner"))
    name = models.CharField(_("Template Name"), max_length=255)
    subject = models.CharField(_("Subject (English)"), max_length=255)
    subject_de = models.CharField(_("Subject (German)"), max_length=255)
    body = PlainTextModelField(_("Template Text (English)"), blank=True)
    body_de = PlainTextModelField(_("Template Text (German)"), blank=True)
    body_html = models.TextField(_("Template HTML (English)"), null=True, blank=True)
    body_html_de = models.TextField(_("Template HTML (German)"), null=True, blank=True)
    timestamp = models.DateTimeField(_("Written"), auto_now_add=True)
    allowed_placeholders = models.ManyToManyField(EmailTemplatePlaceholder, verbose_name=_("Allowed Placeholders"), blank=True)
    
    class Meta:
        verbose_name = _("email template")
        verbose_name_plural = _("email templates")
        ordering = ['-timestamp', 'name']
        
    def __unicode__(self):
        return "%s %s" % (self.timestamp, force_unicode(self.name))
    
    def get_allowed_placeholders(self):
        return EmailTemplatePlaceholder.objects.distinct().extra(
            tables=['mailing_emailtemplate_allowed_placeholders'],
            where=['mailing_emailtemplateplaceholder.id=mailing_emailtemplate_allowed_placeholders.emailtemplateplaceholder_id', 'mailing_emailtemplate_allowed_placeholders.emailtemplate_id=%d' % (self.id or 0)],
        )
        
    def render_template(self, placeholders, template, is_html=True):
        """
        renders a template body (or whatever) by substituting placeholders
        
        placeholders:    A dictionary of the placeholders with it's values
        template:        The template text to be substituted.
        
        """
        prepare_value = lambda s: s
        if not is_html:
            # remove html from all descriptions and similar fields
            prepare_value = html_to_plain_text
        # first, get the "allowed" placeholders for the email template
        for item in self.get_allowed_placeholders():
            if item.sysname in placeholders:
                subst = placeholders[item.sysname]
                for lang_code, lang_title in settings.LANGUAGES:
                    template = template.replace(
                        "[%s]" % getattr(item, "name_%s" % lang_code),
                        force_unicode(prepare_value(subst)),
                    )
                        
        return template
        
    def save(self, *args, **kwargs):
        if not self.body:
            self.body = html_to_plain_text(self.body_html)
        if not self.body_de:
            self.body_de = html_to_plain_text(self.body_html_de)
        super(EmailTemplate, self).save(*args, **kwargs)
    save.alters_data = True

