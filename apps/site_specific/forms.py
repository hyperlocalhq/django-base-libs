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
        self.fields['password'].help_text = """<a href="/password_reset/">%s</a>""" % _("Forgot password?")
        
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

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

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
            _("Claiming Invitation"),
            "museum",
            "email",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Send invitation')),
                )
            )

class ClaimingConfirmationForm(forms.Form):
    username = forms.RegexField(
        label=_("Username for login"),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")}
        )
    first_name = forms.CharField(
        label=_("First name"),
        )
    last_name = forms.CharField(
        label=_("Last name"),
        )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        )
    confirm_password = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password for verification.")
        )
    
    def __init__(self, user, *args, **kwargs):
        super(ClaimingConfirmationForm, self).__init__(*args, **kwargs)
        
        self.user = user
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
            _("Claiming Confirmation"),
            layout.HTML("""{% load i18n %}
                <p>{% blocktrans with museum_link=museum.get_url_path museum_title=museum.title %}Please fill in this form to create and account at Museumsportal Berlin and to confirm that you are the owner of <a href="{{ museum_link }}">{{ museum_title }}</a>.{% endblocktrans %}</p>
            """),
            "username",
            layout.Row("first_name", "last_name"),
            layout.Row("password", "confirm_password"),
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Confirm')),
                )
            )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if self.user and self.user.username == username:
            return username
        else:
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

class RegistrationForm(forms.Form):
    username = forms.RegexField(
        label=_("Username for login"),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")}
        )
    email = forms.EmailField(label=_("Email"))
    first_name = forms.CharField(
        label=_("First name"),
        )
    last_name = forms.CharField(
        label=_("Last name"),
        )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        )
    confirm_password = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password for verification.")
        )
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
            _("Registration"),
            layout.HTML("""{% load i18n %}
                <p>{% blocktrans %}Please fill in this form to create and account at Museumsportal Berlin.{% endblocktrans %}</p>
            """),
            layout.Row("username", "email"),
            layout.Row("first_name", "last_name"),
            layout.Row("password", "confirm_password"),
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Confirm')),
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
    "",
    layout.HTML("""{% load i18n %}
        <p>{% trans "Please enter your old password, for security's sake, and then enter your new password twice so we can verify you typed it in correctly." %}</p>
    """),
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
    "",
    layout.HTML(u"""{% load i18n %}
        <p>{% trans "Forgot your password? Enter your email address below, and we’ll send you an email with a link which allows you to set up a new password.." %}</p>
    """),
    "email",
    ),
    bootstrap.FormActions(
        layout.Submit('submit', _('Reset my password')),
        )
    )

password_reset_change_form_helper = FormHelper()
password_reset_change_form_helper.form_action = ""
password_reset_change_form_helper.form_method = "POST"
password_reset_change_form_helper.layout = layout.Layout(
    layout.Fieldset(
    "",
    layout.HTML("""{% load i18n %}
        <p>{% trans "Please enter your new password twice so we can verify you typed it in correctly." %}</p>
    """),
    layout.Row("new_password1", "new_password2"),
    ),
    bootstrap.FormActions(
        layout.Submit('submit', _('Change my password')),
        )
    )


