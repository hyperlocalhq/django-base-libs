# -*- coding: UTF-8 -*-

from django.db import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate

from base_libs.middleware.threadlocals import get_current_language

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from jetson.apps.mailchimp.models import MList

User = models.get_model("auth", "User")

class EmailOrUsernameAuthentication(AuthenticationForm):
    login_as = forms.CharField(
        label=_("Email or Username"),
        max_length=75,
        widget=forms.HiddenInput(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(EmailOrUsernameAuthentication, self).__init__(*args, **kwargs)
        self.fields['email_or_username'] = forms.CharField(
            label=_("Email or Username"),
            max_length=75,
        )
        del self.fields['username']
        self.fields['password'].help_text = """<a href="/password-reset/">%s</a>""" % _("Forgot password?")

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "", # no legend
                layout.Field("email_or_username", autocomplete="off"),
                "password",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Login')),
            )
        )

    def clean(self):
        email_or_username = self.cleaned_data.get('email_or_username')
        password = self.cleaned_data.get('password')

        if email_or_username and password:
            if "@" in email_or_username:
                self.user_cache = authenticate(email=email_or_username, password=password)
            else:
                self.user_cache = authenticate(username=email_or_username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct email or username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        return self.cleaned_data


class RegistrationForm(forms.Form):

    # Simplified signup ->

    # username = forms.RegexField(
    #     label=_("Username for login"),
    #     max_length=30,
    #     regex=r'^[\w.@+-]+$',
    #     help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
    #     error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")}
    #     )
    # first_name = forms.CharField(
    #     label=_("First name"),
    #     )
    # last_name = forms.CharField(
    #     label=_("Last name"),
    #     )

    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
    confirm_password = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['privacy_policy'] = forms.BooleanField(
            required=True,
            label=_("I accept <a href=\"/%(lang_code)s/privacy/\" target=\"_blank\">the privacy policy</a>.") % {'lang_code': get_current_language()},
        )
        self.fields['terms_of_use'] = forms.BooleanField(
            required=True,
            label=_("I accept <a href=\"/%(lang_code)s/terms-of-use/\" target=\"_blank\">the terms of use</a>.") % {'lang_code': get_current_language()},
        )

        self.newsletter_fields = []
        self.newsletter_field_names = []
        for ml in MList.site_objects.filter(is_public=True):
            f = self.fields['newsletter_%s' % ml.pk] = forms.BooleanField(
                label=_("I want to subscribe to %s.") % ml.title,
                initial=True,
                required=False,
            )
            self.newsletter_fields.append(("newsletter_%s" % ml.pk, f))
            self.newsletter_field_names.append("newsletter_%s" % ml.pk)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "", # no legend

                # "username",
                # "first_name",
                # "last_name",

                layout.Field("email", autocomplete="off"),

                "password",
                "confirm_password",
                "privacy_policy",
                "terms_of_use",
                *self.newsletter_field_names
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Signup')),
            )
        )

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("A user with that email already exists."))

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password", "")
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return confirm_password

password_change_form_helper = FormHelper()
password_change_form_helper.form_action = ""
password_change_form_helper.form_method = "POST"
password_change_form_helper.layout = layout.Layout(
    layout.Fieldset(
        "", # no legend
        "old_password",
        "new_password1",
        "new_password2",
    ),
    bootstrap.FormActions(
        layout.Submit('submit', _('Confirm')),
    )
)

password_reset_form_helper = FormHelper()
password_reset_form_helper.form_action = ""
password_reset_form_helper.form_method = "POST"
password_reset_form_helper.layout = layout.Layout(
    layout.Fieldset(
        "", # no legend
        "email",
    ),
    bootstrap.FormActions(
        layout.Submit('submit', _('Reset password')),
    )
)

password_reset_change_form_helper = FormHelper()
password_reset_change_form_helper.form_action = ""
password_reset_change_form_helper.form_method = "POST"
password_reset_change_form_helper.layout = layout.Layout(
    layout.Fieldset(
        "", # no legend
        layout.HTML("""{% load i18n %}
            <p>{% trans "Please enter your new password twice so we can verify you typed it in correctly." %}</p>
        """),
        "new_password1",
        "new_password2",
    ),
    bootstrap.FormActions(
        layout.Submit('submit', _('Change my password')),
    )
)
