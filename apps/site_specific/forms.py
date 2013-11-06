# -*- coding: UTF-8 -*-

from django.db import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

User = models.get_model("auth", "User")
Museum = models.get_model("museums", "Museum")


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
        # self.fields['password'].help_text = """<a href="/password_reset/">%s</a>""" % _("Forgot password?")
        
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


class ClaimingInvitationForm(forms.Form):
    museum = forms.ModelChoiceField(
        label=_("Museum"),
        queryset=Museum.objects.all(),
    )
    email = forms.EmailField(label=_("Owner's email"))
    
    def __init__(self, *args, **kwargs):
        super(ClaimingInvitationForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "", # no legend
                "museum",
                "email",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Send invitation')),
            )
        )


class ClaimingRegisterForm(forms.Form):
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
    confirm_password = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
    )
    
    def __init__(self, user, *args, **kwargs):
        super(ClaimingRegisterForm, self).__init__(*args, **kwargs)
        
        self.user = user
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "", # no legend
                layout.Field("email", autocomplete="off"),
                "password",
                "confirm_password",
            ),
            bootstrap.FormActions(
                layout.Submit('register', _('Signup')),
            )
        )

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password", "")
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return confirm_password


class ClaimingLoginForm(forms.Form):
    email_or_username = forms.CharField(
        label=_("Email or Username"),
        max_length=75,
        required=True,
    )
    password = forms.CharField(
        label=_("Password"),
        max_length=75,
        required=True,
        widget=forms.PasswordInput(),
    )

    def __init__(self, user, *args, **kwargs):
        super(ClaimingLoginForm, self).__init__(*args, **kwargs)
        self.user = user
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                "", # no legend
                "email_or_username",
                "password",
            ),
            bootstrap.FormActions(
                layout.Submit('login', _('Login')),
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
        
    def get_user(self):
        return getattr(self, "user_cache", None)


class ClaimingConfirmForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ClaimingConfirmForm, self).__init__(*args, **kwargs)
        
        self.user = user
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            bootstrap.FormActions(
                layout.Submit('confirm', _('Confirm')),
            )
        )


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
        layout.Row("new_password1", "new_password2"),
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


class ExhibitionFilterForm(forms.Form):
    status = forms.ChoiceField(
        label=_("Status"),
        choices=(
            ('published', _("Published")),
            ('draft', _("Draft")),
            ('expired', _("Expired")),
        ),
        required=False,
        initial="published",
    )

    def __init__(self, *args, **kwargs):
        super(ExhibitionFilterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.layout = layout.Layout(
            "status",
            layout.Submit('submit', _('Filter')),
        )


class EventFilterForm(forms.Form):
    status = forms.ChoiceField(
        label=_("Status"),
        choices=(
            ('published', _("Published")),
            ('draft', _("Draft")),
            ('expired', _("Expired")),
        ),
        required=False,
        initial="published",
    )

    def __init__(self, *args, **kwargs):
        super(EventFilterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.layout = layout.Layout(
            "status",
            layout.Submit('submit', _('Filter')),
        )


class WorkshopFilterForm(forms.Form):
    status = forms.ChoiceField(
        label=_("Status"),
        choices=(
            ('published', _("Published")),
            ('draft', _("Draft")),
            ('expired', _("Expired")),
        ),
        required=False,
        initial="published",
    )

    def __init__(self, *args, **kwargs):
        super(WorkshopFilterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.layout = layout.Layout(
            "status",
            layout.Submit('submit', _('Filter')),
        )

