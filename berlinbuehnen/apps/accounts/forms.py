# -*- coding: UTF-8 -*-
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from base_libs.middleware.threadlocals import get_current_language

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

User = models.get_model("auth", "User")

class EmailOrUsernameAuthentication(AuthenticationForm):
    email_or_username = forms.CharField(
        label=_("Email or Username"),
        max_length=75,
    )
    login_as = forms.CharField(
        label=_("Email or Username"),
        max_length=75,
        widget=forms.HiddenInput(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(EmailOrUsernameAuthentication, self).__init__(*args, **kwargs)
        del self.fields['username']
        # self.fields['password'].help_text = """<a href="/password_reset/">%s</a>""" % _("Forgot password?")

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "", # no legend
                layout.Field("email_or_username", autocomplete="off"),
                layout.Field("password", autocomplete="off"),
                "login_as",
                layout.HTML("""
                    {% load i18n %}
                    <input type="hidden" name="this_is_the_login_form" value="1" />
                    <input type="hidden" name="post_data" value="{{ post_data }}" />
                """),
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Login')),
            )
        )

    def clean(self):
        email_or_username = self.cleaned_data.get('email_or_username')
        password = self.cleaned_data.get('password')

        if email_or_username and password:
            self.user_cache = None
            if "@" in email_or_username:
                # TODO: integrate this somehow better into the Python Social Auth backends
                try:
                    user = User.objects.get(email=email_or_username)
                except (User.DoesNotExist, MultipleObjectsReturned) as e:
                    pass
                else:
                    self.user_cache = authenticate(username=user.username, password=password)
            else:
                self.user_cache = authenticate(username=email_or_username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_(
                    "Please enter a correct email or username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(
                    _("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data


class RegistrationForm(forms.Form):

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

        lang_code = get_current_language()
        if lang_code == 'de':
            privacy_policy_link = '/de/meta/datenschutzerklarung/'
            terms_and_conditions_link = '/de/meta/nutzungsbedingungen/'
        else:
            privacy_policy_link = '/en/meta/data-protection-guidelines/'
            terms_and_conditions_link = '/en/meta/terms-conditions/'

        self.fields['privacy_policy'] = forms.BooleanField(
            required=True,
            label=_(
                "I accept the <a href=\"%(privacy_policy_link)s\" target=\"_blank\">data protection guidelines</a>."
            ) % {
                "privacy_policy_link": privacy_policy_link,
            },
        )
        self.fields['terms_of_use'] = forms.BooleanField(
            required=True,
            label=_(
                "I accept the <a href=\"%(terms_and_conditions_link)s\" target=\"_blank\">terms and conditions</a>."
            ) % {
                "terms_and_conditions_link": terms_and_conditions_link,
            },
        )

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "",  # no legend
                layout.Row(
                    layout.Div(
                        layout.Field("email", autocomplete="off"),
                        css_class="col-xs-12",
                    ),
                    layout.Div(
                        "password",
                        "confirm_password",
                        css_class="col-xs-12",
                    )
                ),
                layout.Row(
                    layout.Div(
                        "privacy_policy",
                        "terms_of_use",
                        css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12",
                    )
                )
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
        layout.Row("new_password1", "new_password2"),
    ),
    bootstrap.FormActions(
        layout.Submit('submit', _('Change my password')),
    )
)
