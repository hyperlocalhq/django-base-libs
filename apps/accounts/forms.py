# -*- coding: UTF-8 -*-

import re
from mailsnake import MailSnake

from django import forms
from django.db import models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.forms.fields import SecurityField
from base_libs.utils.misc import get_related_queryset
from base_libs.utils.misc import get_unique_value
from base_libs.utils.misc import XChoiceList
from base_libs.utils.crypt import cryptString
from base_libs.utils.betterslugify import better_slugify

from jetson.apps.mailchimp.models import MList
from jetson.apps.mailchimp.models import Subscription
from jetson.apps.mailchimp.models import Settings
from jetson.apps.configuration.models import SiteSettings
from jetson.apps.mailing.views import Recipient, send_email_using_template
from jetson.apps.utils.forms import ModelMultipleChoiceTreeField

image_mods = models.get_app("image_mods")

from ccb.apps.people.app_settings import PREFIX_CI

app = models.get_app("people")
Person, IndividualContact, URL_ID_PERSON, URL_ID_PEOPLE = (
    app.Person, app.IndividualContact, app.URL_ID_PERSON, app.URL_ID_PEOPLE
)

NULL_PREFIX_CHOICES = XChoiceList(get_related_queryset(Person, 'prefix'))
username_re = re.compile(r"^[a-zA-Z][0-9a-zA-Z\-_]{2,}$")

# FORMS

site_settings = SiteSettings.objects.get_current()


class SimpleRegistrationFormBase(dynamicforms.Form):
    """ One-step registration form """
    # TODO: merge this class with SimpleRegistrationForm as it doesn't add any value when used separately
    email = forms.EmailField(
        label=_("Email"),
        required=True,
    )
    username = forms.RegexField(
        label=_("Username"),
        regex=username_re,
        required=True,
        max_length=30,
        error_messages={
            'invalid': _(
                "Username can only consist of letters, digits, dashes, and underscores. It should start with a letter and be not shorter than 3 symbols."),
        },
    )
    prefix = forms.ChoiceField(
        label=_("Prefix"),
        choices=NULL_PREFIX_CHOICES,
    )
    first_name = forms.CharField(
        label=_("First name"),
        required=True,
        max_length=30,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=True,
        max_length=30,
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        required=True,
        max_length=30,
    )
    password_confirm = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
        required=True,
        max_length=30,
    )
    privacy_policy = forms.BooleanField(
        required=True,
        label=_("I accept <a href=\"/privacy/\">the privacy policy</a>."),
    )
    terms_of_use = forms.BooleanField(
        required=True,
        label=_("I accept <a href=\"/terms-of-use/\">the terms of use</a>."),
    )
    prevent_spam = SecurityField()

    def __init__(self, request, *args, **kwargs):
        super(SimpleRegistrationFormBase, self).__init__(*args, **kwargs)
        self.request = request

        self.helper = FormHelper()
        self.helper.form_action = "register"
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Profile"),
                "prefix",
                "first_name",
                "last_name",
                "email",
            ),
            layout.Fieldset(
                _("Login"),
                "username",
                "password",
                "password_confirm",
            ),
            layout.Fieldset(
                _("Confirmation"),
                "privacy_policy",
                "terms_of_use",
                "prevent_spam",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Create account')),
            )
        )

    def clean(self):
        from ccb.apps.site_specific.models import ContextItem
        cleaned = self.cleaned_data
        errors = False
        first_name = cleaned.get('first_name', '')
        last_name = cleaned.get('last_name', '')
        # check the uniqueness; returns the same username if it's unique or a suggestion if it isn't.
        username = cleaned.get('username', '')
        if username:
            suggested = get_unique_value(
                ContextItem,
                username.lower() or better_slugify("_".join((first_name, last_name))).replace("-", "_"),
                field_name="slug",
                separator="_",
                ignore_case=True,
            )
            if username.lower() != suggested.lower():
                self._errors['username'] = self._errors.get('username', [])
                self._errors['username'].append(_(
                    "This username is already used for another account. But you can use \"%s\" as your username.") % suggested)
                errors = True
        # check password confirmation
        password = cleaned.get("password", "")
        password_confirm = cleaned.get("password_confirm", "")
        if password != password_confirm:
            self._errors['password_confirm'] = self._errors.get('password_confirm', [])
            self._errors['password_confirm'].append(_("The confirmed password doesn't match the password."))
            errors = True

        non_field_errors = []

        if errors:
            # raise an error so that the form doesn't validate
            raise forms.ValidationError(non_field_errors)

        return cleaned

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count():
            raise forms.ValidationError(_("This email address is already used for another account."))
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 3:
            raise forms.ValidationError(_("Passwords must be at least 3 characters long"))
        return password

    def save(self, activate_immediately=False):
        cleaned = self.cleaned_data
        email = cleaned['email']

        username = get_unique_value(
            User,
            cleaned.get('username', "") or better_slugify(cleaned["name"]).replace("-", "_"),
            field_name="username",
            separator="_",
        )

        password = cleaned['password']
        user = User.objects.create_user(username, email, password)
        user.is_active = activate_immediately
        user.first_name = cleaned['first_name']
        user.last_name = cleaned['last_name']
        user.save()

        person, created = Person.objects.get_or_create(user=user)
        person.prefix_id = cleaned['prefix']
        if activate_immediately:
            person.status = "published"
        person.save()

        if not activate_immediately:
            # setting the raw password for email to the user
            encrypted_password = user.password
            user.password = cleaned['password']

            current_site = Site.objects.get_current()
            encrypted_email = cryptString(user.email)

            sender_name, sender_email = settings.MANAGERS[0]
            send_email_using_template(
                [Recipient(user=user)],
                "account_verification",
                obj_placeholders={
                    'encrypted_email': encrypted_email,
                    'site_name': current_site.name,
                },
                delete_after_sending=False,
                sender_name=sender_name,
                sender_email=sender_email,
                send_immediately=True,
            )

            user.password = encrypted_password
        return user


class SimpleRegistrationForm(SimpleRegistrationFormBase):
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        queryset=get_related_queryset(Person, "categories"),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(SimpleRegistrationForm, self).__init__(*args, **kwargs)

        self.newsletter_fields = []
        self.newsletter_field_names = []
        for ml in MList.site_objects.filter(is_public=True):
            f = self.fields['newsletter_%s' % ml.pk] = forms.BooleanField(
                label=_("I want to subscribe to %s.") % ml.title,
                initial=False,
                required=False,
            )
            self.newsletter_fields.append(("newsletter_%s" % ml.pk, f))
            self.newsletter_field_names.append("newsletter_%s" % ml.pk)

        self.helper = FormHelper()
        self.helper.form_action = "register"
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Profile"),
                "prefix",
                "first_name",
                "last_name",
                "email",
            ),
            layout.Fieldset(
                _("Login"),
                "username",
                "password",
                "password_confirm",
            ),
            layout.Fieldset(
                _("Categories"),
                layout.Field("categories", template="ccb_form/custom_widgets/checkboxselectmultipletree.html"),
                css_class="no-label",
            ),
            layout.Fieldset(
                _("Confirmation"),
                "privacy_policy",
                "terms_of_use",
                "prevent_spam",
                *self.newsletter_field_names,
                css_class="no-label"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Create account')),
                css_class='button-group form-buttons',
            )
        )

    def save(self, activate_immediately=False):
        user = super(SimpleRegistrationForm, self).save(activate_immediately=activate_immediately)
        cleaned = self.cleaned_data

        # TODO: Update the save method to use creatives sectors from crispy form

        person = user.profile

        person.categories.clear()
        person.categories.add(*cleaned['categories'])

        try:
            s = Settings.objects.get()
        except Exception:
            pass
        else:
            ms = MailSnake(s.api_key)
            for ml in MList.site_objects.filter(is_public=True):
                if cleaned['newsletter_%s' % ml.pk]:
                    if s.double_optin:
                        status = "pending"
                    else:
                        status = "subscribed"
                    sub = Subscription.objects.create(
                        subscriber=user,
                        ip=self.request.META['REMOTE_ADDR'],
                        mailinglist=ml,
                        status=status,
                    )
                    if ml.mailchimp_id:
                        ms.listSubscribe(
                            id=ml.mailchimp_id,
                            email_address=sub.email,
                            merge_vars={
                                'FNAME': sub.first_name,
                                'LNAME': sub.last_name,
                            },
                            double_optin=s.double_optin,
                            update_existing=s.update_existing,
                            send_welcome=s.send_welcome,
                        )
        return user


class EmailAuthentication(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(EmailAuthentication, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            label=_("Email"),
            max_length=75,
        )
        del self.fields['username']

        self.helper = FormHelper()
        self.helper.form_action = "login"
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Login"),
                "email",
                "password",
                "login_as",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Login')),
            )
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Please enter a correct email and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(
                    _("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data


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

        self.helper = FormHelper()
        self.helper.form_action = "login"
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Login"),
                "email_or_username",
                "password",
                "login_as",
                layout.HTML("""
                    {% load i18n %}
                    <p><a href="{% url "password_reset" %}">{% trans "Forgotten your password?" %}</a></p>
                    <input type="hidden" name="this_is_the_login_form" value="1" />
                    <input type="hidden" name="post_data" value="{{ post_data }}" />
                    <input type="hidden" name="goto_next" value="{% if goto_next == "/" %}/dashboard/{% else %}{% if goto_next %}{{ goto_next }}{% else %}/dashboard/{% endif %}{% endif %}" />
                """),
                bootstrap.FormActions(
                    layout.Submit('submit', _('Login')),
                    css_class='button-group form-buttons',
                )
            ),
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
                except:
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


class PrivacySettingsForm(dynamicforms.Form):
    def __init__(self, *args, **kwargs):
        ## we overrride the init method here, because we
        ## need a custom mapping for special initial values
        if kwargs.has_key('initial'):
            initial = kwargs['initial']
            status = initial['status']
            if status == "published":
                initial['display_profile'] = True
            else:
                initial['display_profile'] = False

        super(PrivacySettingsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = "privacy_settings"
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Global"),
                "display_profile",
                "display_username",
            ),
            layout.Fieldset(
                _("Profile"),
                "display_birthday",
                "allow_search_engine_indexing",
            ),
            layout.Fieldset(
                _("Contact"),
                "display_address",
                "display_phone",
                "display_fax",
                "display_mobile",
                "display_im",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Confirm')),
            )
        )

    display_profile = forms.BooleanField(
        required=False,
        label=_("Display profile to public"),
        initial=True,
    )
    display_username = forms.BooleanField(
        required=False,
        label=_("Display user name instead of full name"),
        initial=False,
    )
    allow_search_engine_indexing = forms.BooleanField(
        required=False,
        label=_("Allow indexing by search engines"),
        initial=True,
    )
    display_birthday = forms.BooleanField(
        required=False,
        label=_("Display birthday to public"),
        initial=False,
    )
    display_address = forms.BooleanField(
        required=False,
        label=_("Display address data to public"),
        initial=True,
    )
    display_phone = forms.BooleanField(
        required=False,
        label=_("Display phone numbers to public"),
        initial=True,
    )
    display_fax = forms.BooleanField(
        required=False,
        label=_("Display fax numbers to public"),
        initial=True,
    )
    display_mobile = forms.BooleanField(
        required=False,
        label=_("Display mobile phones to public"),
        initial=True,
    )
    display_im = forms.BooleanField(
        required=False,
        label=_("Display instant messangers to public"),
        initial=True,
    )


# Translatable strings to collect to django.po file
_("Please enter your old password, for security's sake, and then enter your new password twice so we can verify you typed it in correctly.")
_("Forgot your password? Enter your e-mail address below, and we’ll send you an e-mail with a link which allows you to set up a new password.")
_("Please enter your new password twice so we can verify you typed it in correctly.")


password_change_form_helper = FormHelper()
password_change_form_helper.form_action = ""
password_change_form_helper.form_method = "POST"
password_change_form_helper.layout = layout.Layout(
    layout.Fieldset(
        _("Password change"),
        layout.HTML(u"""{% load i18n %}
            <p>{% trans "Please enter your old password, for security's sake, and then enter your new password twice so we can verify you typed it in correctly." %}</p>
        """),
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
        _("Password reset"),
        layout.HTML(u"""{% load i18n %}
            <p>{% trans "Forgot your password? Enter your e-mail address below, and we’ll send you an e-mail with a link which allows you to set up a new password." %}</p>
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
        _("Password change"),
        layout.HTML(u"""{% load i18n %}
            <p>{% trans "Please enter your new password twice so we can verify you typed it in correctly." %}</p>
        """),
        layout.Row("new_password1", "new_password2"),
    ),
    bootstrap.FormActions(
        layout.Submit('submit', _('Change my password')),
    )
)
