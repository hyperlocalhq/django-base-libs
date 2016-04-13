# -*- coding: utf-8 -*-
import re

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from actstream import action

from base_libs.forms import dynamicforms
from base_libs.forms.fields import SecurityField, SingleEmailTextField, MultiEmailTextField
from base_libs.utils.user import get_user_title

from jetson.apps.mailing.models import EmailMessage

class GenericMailForm(dynamicforms.Form):
    sender_name = forms.CharField(
        label=_("Sender Name"),
        required=False, 
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    sender_email = SingleEmailTextField(
        label=_("Sender Email"),
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    tester_email = SingleEmailTextField(
        label=_("Tester Email"),
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    recipients_email_list = forms.MultipleChoiceField(
        label=_("Recipients"),
        widget=forms.SelectMultiple(),
        help_text=_("Please select one or more recipients from the list and/or enter recipients in the text field below."),
        )
    recipients_email_input = MultiEmailTextField(
        label=_("Recipients (Emails)"),
        required=False,
        widget=forms.Textarea(attrs={'class':'vPlainTextField'}),
        help_text=_("Email addresses must have the form 'John Doe (john.doe@domain.com)' or just 'john.doe@domain.com'."),
        )
    subject = forms.CharField(
        label=_("Subject (English)"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    body = forms.CharField(
        label= _("Message (English)"),
        required=True,
        widget=forms.Textarea(attrs={'class':'vTextField'}),
        )
    subject_de = forms.CharField(
        label=_("Subject (German)"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    body_de = forms.CharField(
        label=_("Message (German)"),
        required=True,
        widget=forms.Textarea(attrs={'class':'vTextField'}),
        )

def message_received(sender, instance, **kwargs):
    from jetson.apps.notification import models as notification
    
    if notification.NoticeSetting.objects.filter(
        user=instance.recipient,
        notice_type__sysname="message_received",
        send=True,
        medium="1",
        ):
        if instance.sender_email:
            submitter_email = instance.sender_email
        else:
            submitter_email = instance.sender.email
        if instance.sender_name:
            submitter_name = instance.sender_name
        else:
            submitter_name = get_user_title(instance.sender)
        notification.send(
            instance.recipient,
            "message_received",
            {
                "object_creator_title": submitter_name,
                "object_title": instance.subject,
                },
            instance=instance,
            )
        action.send(instance.recipient, verb="received message", action_object=instance)
