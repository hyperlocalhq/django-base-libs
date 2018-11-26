# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from base_libs.forms import dynamicforms
from base_libs.middleware import get_current_user
from base_libs.forms.fields import SecurityField

from mailsnake import MailSnake

from ruhrbuehnen.apps.mailchimp.models import Subscription
from ruhrbuehnen.apps.mailchimp.models import MList
from ruhrbuehnen.apps.mailchimp.models import Settings

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap


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
                layout.Div(
                    layout.Div(
                        layout.Field(
                            "first_name", css_class="input-block-level"
                        ),
                        css_class="span6",
                    ),
                    layout.Div(
                        layout.Field(
                            "last_name", css_class="input-block-level"
                        ),
                        css_class="span6",
                    ),
                    css_class="row-fluid",
                    css_id="mailing-list-names",
                ),
                layout.Field("email", css_class="input-block-level"),
                "prevent_spam",
            ),
            bootstrap.FormActions(layout.Submit('submit', _('Send')), ),
        )

    def save(self, request):
        cleaned = self.cleaned_data
        email = cleaned['email']
        first_name = cleaned['first_name']
        last_name = cleaned['last_name']
        ip = request.META['REMOTE_ADDR']
        user = get_current_user()
        ml = cleaned['mlist']
        s = Settings.objects.get()
        ms = MailSnake(s.api_key)
        if s.double_optin:
            status = "pending"
        else:
            status = "subscribed"
        sub, created = Subscription.objects.get_or_create(
            ip=ip,
            email=email,
            subscriber=user,
            first_name=first_name,
            last_name=last_name,
            mailinglist=ml,
            status=status,
        )
        if ml.mailchimp_id:
            ms.listSubscribe(
                id=ml.mailchimp_id,
                email_address=sub.email,
                merge_vars={
                    'FNAME': first_name,
                    'LNAME': last_name,
                },
                double_optin=s.double_optin,
                update_existing=s.update_existing,
                send_welcome=s.send_welcome,
            )
        return sub
