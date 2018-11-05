# -*- coding: utf-8 -*-
import re

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.forms.fields import SecurityField, SingleEmailTextField, MultiEmailTextField
from base_libs.utils.misc import XChoiceList
from base_libs.utils.user import get_user_title

from jetson.apps.mailing.models import EmailMessage
from jetson.apps.mailing.recipient import Recipient
from jetson.apps.contact_form.models import ContactFormCategory

CONTACT_FORM_CATEGORIES = ContactFormCategory.site_objects.all()


class ContactForm(dynamicforms.Form):
    
    subject = forms.CharField(
        label=_("Subject"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
    )
    
    body = forms.CharField(
        label=_("Message"),
        required=True,
        widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
    )
    
    sender_name = forms.CharField(
        label=_("Your name"),
        required=True, 
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
    )
    sender_email = SingleEmailTextField(
        label=_("Your e-mail address"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
    )
    
    # prevent spam
    prevent_spam = SecurityField()
    
    if CONTACT_FORM_CATEGORIES.count() > 1:
        contact_form_category = forms.ChoiceField(
            label=_("Category"),
            required=False,
            choices=XChoiceList(CONTACT_FORM_CATEGORIES),
        )
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "."
        self.helper.form_method = "POST"
        self.helper.form_id = "contact_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Contact Form"),

                layout.Div(
                    layout.Div(
                        layout.Field("sender_name", css_class="input-block-level", data_progression="", data_helper=""),
                        css_class="span6",
                    ),
                    layout.Div(
                        layout.Field("sender_email", css_class="input-block-level", data_progression="", data_helper=""),
                        css_class="span6",
                    ),
                    css_class="row-fluid",
                    css_id="contact-form-names",
                ),

                layout.Field("contact_form_category", css_class="input-block-level", data_progression="", data_helper=""),
                layout.Field("subject", css_class="input-block-level", data_progression="", data_helper=""),
                layout.Field("body", css_class="input-block-level", data_progression="", data_helper=""),
                "prevent_spam",
                layout.HTML("{{ form.prevent_spam.error_tag }}"),
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Submit')),
            )
        )
        
    def save(self, sender=None):
        
        # do character encoding
        cleaned = self.cleaned_data
        #for key, value in cleaned.items():
        #    if type(value).__name__ == "unicode":
        #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)
        
        if not sender.is_authenticated():
            sender=None
        
        try:
            contact_form_category = ContactFormCategory.site_objects.get(
                pk=cleaned["contact_form_category"],
                )
        except:
            contact_form_category = CONTACT_FORM_CATEGORIES[0]
            
        subject = cleaned["subject"]
        body = cleaned["body"]
        sender_name = cleaned["sender_name"]
        sender_email = cleaned["sender_email"]
        
        recipient_emails = []
        for recipient in contact_form_category.recipients.all():
            recipient_emails.append("%s <%s>" % (
                get_user_title(recipient),
                recipient.email,
            ))
        separator_re = re.compile(r"\s*[\n\r,;]\s*")
        for recipient in separator_re.split(contact_form_category.recipient_emails):
            if recipient:
                recipient_emails.append(recipient)
        if not recipient_emails:
            recipient_emails = ["%s <%s>" % (
                '',
                settings.DEFAULT_FROM_EMAIL,
            )]
        message = EmailMessage.objects.create(
            sender=sender,
            sender_name=sender_name,
            sender_email=sender_email,
            recipient_emails=",".join(recipient_emails),
            subject=subject,
            body_html=body,
        )
        message.send()
        if contact_form_category.auto_answer_template:
            from jetson.apps.mailing.views import send_email_using_template
            send_email_using_template(
                recipients_list=[Recipient(
                    user=sender,
                    name=sender_name,
                    email=sender_email,
                    )],
                email_template_slug=contact_form_category.auto_answer_template.slug,
                obj=message,
                sender_name='',
                sender_email=settings.DEFAULT_FROM_EMAIL,
                send_immediately=True,
            )
