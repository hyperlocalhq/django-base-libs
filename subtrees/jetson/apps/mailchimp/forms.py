# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from requests import HTTPError

from base_libs.forms import dynamicforms
from base_libs.middleware import get_current_user
from base_libs.forms.fields import SecurityField

from mailchimp3 import MailChimp

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from .models import MList
from .models import Settings


class SubscriptionForm(dynamicforms.Form):
    mlist = forms.ModelChoiceField(
        label=_("Mailing list"),
        queryset=MList.objects.filter(is_public=True),
        required=True,
    )
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        max_length=200,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        max_length=200,
    )
    email = forms.EmailField(
        label=_("Your email"),
        required=True,
    )
    prevent_spam = SecurityField()
    
    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)

        mailing_lists = MList.objects.filter(is_public=True)
        if mailing_lists.count() == 1:
            self.fields['mlist'].initial = mailing_lists[0]
            self.fields['mlist'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "",
                layout.Field("mlist", css_class="input-block-level"),
                layout.Field("first_name", css_class="input-block-level"),
                layout.Field("last_name", css_class="input-block-level"),
                layout.Field("email", css_class="input-block-level"),
                "prevent_spam",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Send')),
            ),
        )
    
    def save(self, request):
        import hashlib
        cleaned = self.cleaned_data
        email = cleaned['email']
        first_name = cleaned['first_name']
        last_name = cleaned['last_name']
        ip = request.META['REMOTE_ADDR']
        user = get_current_user()
        ml = cleaned['mlist']
        s = Settings.objects.get()
        mailchimp_client = MailChimp(s.username, s.api_key)
        if s.double_optin:
            status = "pending"
        else:
            status = "subscribed"
        m = hashlib.md5()
        m.update(user.email.lower())
        if ml.mailchimp_id:
            result = mailchimp_client.lists.members.create_or_update(
                ml.mailchimp_id,
                m.hexdigest(),
                {
                    'email_address': email,
                    'status_if_new': status,
                    'merge_fields': {
                        'FNAME': first_name,
                        'LNAME': last_name,
                    }
                }
            )
            return result


class SimpleSubscriptionForm(dynamicforms.Form):
    mlist = forms.ModelChoiceField(
        label=_("Mailing list"),
        queryset=MList.objects.filter(is_public=True),
        required=True,
    )
    email = forms.EmailField(
        label=_("Your email"),
        required=True,
    )
    prevent_spam = SecurityField()

    def __init__(self, lang_code, *args, **kwargs):
        super(SimpleSubscriptionForm, self).__init__(*args, **kwargs)

        self.lang_code = lang_code

        mailing_lists = MList.objects.filter(
            models.Q(language=lang_code) | models.Q(language=""),
            is_public=True,
        )
        if mailing_lists.count() == 1:
            self.fields['mlist'].initial = mailing_lists[0]
            self.fields['mlist'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "",
                layout.Field("mlist", css_class="input-block-level"),
                layout.Field("email", css_class="input-block-level"),
                "prevent_spam",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Subscribe')),
            ),
        )

    def save(self, request):
        cleaned = self.cleaned_data
        email = cleaned['email']
        user = get_current_user()
        ml = cleaned['mlist']
        s = Settings.objects.get()
        mailchimp_client = MailChimp(s.username, s.api_key)
        if s.double_optin:
            status = "pending"
        else:
            status = "subscribed"
        if ml.mailchimp_id:
            try:
                result = mailchimp_client.lists.members.create(
                    list_id=ml.mailchimp_id,
                    data={
                        'email_address': email,
                        'status': status,
                        'merge_fields': {
                            'FNAME': user.first_name if user else "",
                            'LNAME': user.last_name if user else "",
                        }
                    }
                )
            except HTTPError as err:
                result = err.response.json()
            return result
