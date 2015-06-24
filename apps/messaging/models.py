# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from django.conf import settings

from base_libs.utils.misc import get_translation
from base_libs.models import CreationModificationMixin
from base_libs.models import ExtendedTextField

verbose_name = _("Messaging")

class InternalMessage(CreationModificationMixin):
    sender = models.ForeignKey(User, verbose_name=_("Sender"), null=True, blank=True, related_name="sent_message_set")
    recipient = models.ForeignKey(User, verbose_name=_("Recipient"), null=True, blank=True, related_name="received_message_set")
    subject = models.CharField(_("Subject"), max_length=255, blank=True)
    body = ExtendedTextField(_("Message"), blank=True)
    is_read = models.BooleanField(_("Read"), default=False)
    is_deleted = models.BooleanField(_("Deleted"), default=False)
    is_replied = models.BooleanField(_("Replied"), default=False)
    is_spam = models.BooleanField(_("Spam"), default=False)
    is_draft = models.BooleanField(_("Draft"), default=False)

    class Meta:
        verbose_name = _("internal message")
        verbose_name_plural = _("internal messages")
        ordering = ('-creation_date', 'subject',)
        
    def __unicode__(self):
        return "%s %s" % (self.creation_date, force_unicode(self.subject))
        
    def get_log_message(self, language=None, action=None):
        """
        Gets a message for a specific action which will be logged for history """
        history_models = models.get_app("history")
        message = ""
        if action==history_models.A_CUSTOM1:
            message = get_translation("%(sender)s sent a message to %(recipient)s", language=language) % {
                'sender': (self.sender and [force_unicode(self.sender)] or [self.sender_name])[0],
                'recipient': (self.recipient and [force_unicode(self.recipient)] or [self.recipient_emails])[0],
                }
        elif action==history_models.A_CUSTOM2:
            message = get_translation("%(recipient)s received a message from %(sender)s", language=language) % {
                'sender': (self.sender and [force_unicode(self.sender)] or [self.sender_name])[0],
                'recipient': (self.recipient and [force_unicode(self.recipient)] or [self.recipient_emails])[0],
                }
        return message
