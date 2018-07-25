# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.forms.fields import SingleEmailTextField
from base_libs.forms.fields import SecurityField

from jetson.apps.mailing.models import EmailMessage
from jetson.apps.messaging.models import InternalMessage

class MessageFormBase(dynamicforms.Form):
    
    subject = forms.CharField(
        label=_("Subject"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    
    body = forms.CharField(
        label= _("Message"),
        required=True,
        widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
        )
    
    # prevent spam
    prevent_spam = SecurityField()


class ContactForm(MessageFormBase):
    
    def __init__(self, sender, recipient, *args, **kwargs):
        # sender is a User
        # recipient is either a Person or an Institution
        super(ContactForm, self).__init__(*args, **kwargs)
        self.sender = sender.is_authenticated() and sender or None
        self.recipient = recipient
        # add sender_name and sender_email only if unregistered

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.form_id = "contact_form"

        if not self.sender:
            self.fields['sender_name'] = forms.CharField(
                label=_("Your name"),
                required=True, 
                max_length=255,
                widget=forms.TextInput(attrs={'class':'vTextField'}),
                )
            self.fields['sender_email'] = SingleEmailTextField(
                label=_("Your e-mail address"),
                required=True,
                max_length=255,
                widget=forms.TextInput(attrs={'class':'vTextField'}),
                )
            self.helper.layout = layout.Layout(
                layout.Fieldset(
                    _("Write a message to %s") % self.recipient.get_title(),
                    layout.Field("sender_name"),
                    layout.Field("sender_email"),
                    layout.Field("subject"),
                    layout.Field("body"),
                    "prevent_spam",
                    layout.HTML("{{ form.prevent_spam.error_tag }}"),
                ),
                bootstrap.FormActions(
                    layout.Submit('submit', _('Send message')),
                )
            )
        else:
            self.helper.layout = layout.Layout(
                layout.Fieldset(
                    _("Write a message to %s") % self.recipient.get_title(),
                    layout.Field("subject"),
                    layout.Field("body"),
                    "prevent_spam",
                    layout.HTML("{{ form.prevent_spam.error_tag }}"),
                ),
                bootstrap.FormActions(
                    layout.Submit('submit', _('Send message')),
                )
            )

    def save(self):
        cleaned = self.cleaned_data
        
        subject = cleaned["subject"]
        body = cleaned["body"]
        sender_name = cleaned.get("sender_name", "")
        sender_email = cleaned.get("sender_email", "")
        if self.sender:
            sender_name = self.sender.profile.get_title()
            sender_email = self.sender.email

        if hasattr(self.recipient, "user"):
            message = InternalMessage.objects.create(
                sender = self.sender,
                recipient = self.recipient.user,
                subject = subject,
                body = body,
                )
            # send notification
            message_received(InternalMessage, message)
        else:
            to_email = self.recipient.get_primary_contact().get('email0_address', '')
            message = EmailMessage.objects.create(
                sender = self.sender,
                recipient = None,
                sender_name = sender_name,
                sender_email = sender_email,
                recipient_emails = to_email,
                subject = subject,
                body_html = body,
                )
            message.send()


class InternalMessageForm(MessageFormBase):

    def __init__(self, sender, instance=None, *args, **kwargs):
        # sender is a User
        # recipient is either a Person or an Institution
        super(InternalMessageForm, self).__init__(*args, **kwargs)
        self.sender = sender
        self.instance = instance
        if instance:
            self.initial = instance.__dict__
        
        if not self.instance:
            recipients = [
                (r.to_user.pk, r.to_user.profile.get_title())
                for r in sender.profile.get_individual_relations()
                ]
            self.fields['recipients_email_list'] = forms.MultipleChoiceField(
                label=_("Recipients"),
                widget=forms.SelectMultiple(),
                help_text=_("Please select one or more recipients from the list."),
                required=True,
                choices = recipients,
                )
        

    def send(self):
        cleaned = self.cleaned_data
        
        subject = cleaned["subject"]
        body = cleaned["body"]
        
        if self.instance:
            message = self.instance
            message.sender = self.sender
            message.subject = subject
            message.body = body
            message.is_draft = False
            message.save()
            # send notification
            message_received(InternalMessage, message)
        else:
            for recipient_pk in cleaned['recipients_email_list']:
                message = InternalMessage()
                message.sender = self.sender
                message.recipient_id = recipient_pk
                message.subject = subject
                message.body = body
                message.is_draft = False
                message.save()
                # send notification
                message_received(InternalMessage, message)

    def save_as_draft(self):
        cleaned = self.cleaned_data
        
        subject = cleaned["subject"]
        body = cleaned["body"]
        
        if self.instance:
            message = self.instance
            message.sender = self.sender
            message.subject = subject
            message.body = body
            message.is_draft = True
            message.save()
        else:
            for recipient_pk in cleaned['recipients_email_list']:
                message = InternalMessage()
                message.sender = self.sender
                message.recipient_id = recipient_pk
                message.subject = subject
                message.body = body
                message.is_draft = True
                message.save()

def message_received(sender, instance, **kwargs):
    from jetson.apps.notification import models as notification
    
    submitter_email = instance.sender.email
    submitter_name = instance.sender.profile.get_title()
    notification.send(
        instance.recipient,
        "message_received",
        {
            "object_creator_title": submitter_name,
            "object_title": instance.subject,
            },
        instance=instance,
        )
    # action.send(instance.recipient, verb="received internal message", action_object=instance)
