# -*- coding: UTF-8 -*-
import re

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.utils.misc import get_related_queryset, XChoiceList

from jetson.apps.individual_relations.models import IndividualRelation

from mptt.forms import TreeNodeChoiceField

Person = models.get_model("people", "Person")

RELATION_TYPE_CHOICES =  XChoiceList(
    get_related_queryset(IndividualRelation, 'relation_types').filter(
        parent__isnull=True,
        ),
    null_choice_text=None,
    )

NULL_PREFIX_CHOICES = XChoiceList(get_related_queryset(Person, 'prefix'))

username_re = re.compile(r"^[a-zA-Z][0-9a-zA-Z\-_]{2,}$")

BIRTHDAY_DD_CHOICES = Person._meta.get_field('birthday_dd').get_choices()
BIRTHDAY_DD_CHOICES[0] = ("", _("Day"))
BIRTHDAY_MM_CHOICES = Person._meta.get_field('birthday_mm').get_choices()
BIRTHDAY_MM_CHOICES[0] = ("", _("Month"))
BIRTHDAY_YYYY_CHOICES = Person._meta.get_field('birthday_yyyy').get_choices()
BIRTHDAY_YYYY_CHOICES[0] = ("", _("Year"))

class IndividualRelationForm(dynamicforms.Form):
    message = forms.CharField(
        required=False,
        label=_("Message"),
        widget=forms.Textarea,
        )
    relation_types = forms.MultipleChoiceField(
        label=_("Relation"),
        required=False,
        choices=RELATION_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
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
    def __init__(self, relation_action, user_1, user_2, **kwargs):
        super(IndividualRelationForm, self).__init__(**kwargs)
        fields = self.fields
        self.relation_action = relation_action
        self.user_1 = user_1
        self.user_2 = user_2
        try:
            rel = IndividualRelation.objects.get(
                user=user_1,
                to_user=user_2,
                )
        except:
            pass
        else:
            for fname in (
                'display_birthday',
                'display_address',
                'display_phone',
                'display_fax',
                'display_mobile',
                'display_im',
                ):
                self.fields[fname].initial = getattr(rel, fname, False)
            self.fields['relation_types'].initial = [
                el.id
                for el in rel.relation_types.all()
                ]
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _('Relation'),
                'message',
                'relation_types',
            ),
            layout.Fieldset(
                _('Permissions'),
                'display_phone',
                'display_fax',
                'display_mobile',
                'display_birthday',
                'display_address',
                'display_im',
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _(self.relation_action.title()).upper()),
                layout.Button('button', _('Cancel').upper()),
            )
        )

    
    def save(self):
        cleaned = self.cleaned_data
        action = self.relation_action
        user_1 = self.user_1
        user_2 = self.user_2
        if action=="edit":
            IndividualRelation.objects.edit(
                user_1 = user_1,
                user_2 = user_2,
                **cleaned
                )
        elif action=="invite":
            IndividualRelation.objects.invite(
                user_1 = user_1,
                user_2 = user_2,
                **cleaned
                )
        elif action=="accept":
            IndividualRelation.objects.accept(
                user_1 = user_1,
                user_2 = user_2,
                **cleaned
                )
        elif action=="deny":
            IndividualRelation.objects.deny(
                user_1 = user_1,
                user_2 = user_2,
                **cleaned
                )
        elif action=="block":
            IndividualRelation.objects.block(
                user_1 = user_1,
                user_2 = user_2,
                **cleaned
                )
        elif action=="unblock":
            IndividualRelation.objects.unblock(
                user_1 = user_1,
                user_2 = user_2,
                **cleaned
                )
        elif action=="cancel":
            IndividualRelation.objects.cancel_invitation(
                user_1 = user_1,
                user_2 = user_2,
                **cleaned
                )
        elif action=="remove":
            IndividualRelation.objects.remove_relation(
                user_1 = user_1,
                user_2 = user_2,
                **cleaned
                )

class InvitationConfirmation(dynamicforms.Form):
    prefix = forms.ChoiceField(
        required=True,
        choices=NULL_PREFIX_CHOICES,
        label=_("Prefix"),
        error_messages={
            'required': _("Prefix is required"),
            },
        )
    first_name = forms.CharField(
        required=True,
        label=_("First Name"),
        error_messages={
            'required': _("First name is required"),
            },
        )
    last_name = forms.CharField(
        required=True,
        label=_("Last Name"),
        )
    individual_type = TreeNodeChoiceField(
        required=True,
        queryset=get_related_queryset(Person, "individual_type"),
        label=_("Individual type"),
        )
    
    login_email = forms.EmailField(
        required=True,
        label=_("E-mail"),
        )
    login_email_confirm = forms.EmailField(
        required=True,
        label=_("Confirm E-mail"),
        help_text=_("IMPORTANT: The provided email address must be valid! You will receive your account data via this address.")
        #help_text=_("WICHTIG: Diese angegebene Email-Adresse muss gültig sein, damit wir Ihnen die Zugangsdaten zu Ihrem Profil zusenden können.")
        )
    username = forms.RegexField(
        required=True,
        regex=username_re,
        error_messages = {
            'invalid': _("Username can only consist of letters, digits, dashes, and underscores. It should start with a letter and be not shorter than 3 symbols."),
            },
        label=_("Username"),
        )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label=_("Password"),
        )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label=_("Confirm Password"),
        )
    birthday_dd = forms.ChoiceField(
        required=True,
        choices=BIRTHDAY_DD_CHOICES,
        label=_("Birthday"),
        error_messages={
            'required': _("Day of birth is required"),
            },
        )
    birthday_mm = forms.ChoiceField(
        required=True,
        choices=BIRTHDAY_MM_CHOICES,
        label=_("Birthday"),
        error_messages={
            'required': _("Month of birth is required"),
            },
        )
    birthday_yyyy = forms.ChoiceField(
        required=True,
        choices=BIRTHDAY_YYYY_CHOICES,
        label=_("Birthday"),
        error_messages={
            'required': _("Year of birth is required"),
            },
        )
    privacy_policy = forms.BooleanField(
        required=True,
        label=_("I accept the privacy policy."),
        )
    terms_of_use = forms.BooleanField(
        required=True,
        label=_("I accept the terms of use."),
        )
    occupation = forms.CharField(
        required=False,
        label=_("Occupation"),
        )
    phone_country = forms.CharField(
        required=False,
        max_length=4,
        initial="49",
        )
    phone_area = forms.CharField(
        required=False,
        max_length=5,
        )
    phone_number = forms.CharField(
        required=False,
        max_length=15,
        label=_("Phone"),
        )
    fax_country = forms.CharField(
        required=False,
        max_length=4,
        initial="49",
        )
    fax_area = forms.CharField(
        required=False,
        max_length=5,
        )
    fax_number = forms.CharField(
        required=False,
        max_length=15,
        label=_("Fax"),
        )
    mobile_country = forms.CharField(
        required=False,
        max_length=4,
        initial="49",
        )
    mobile_area = forms.CharField(
        required=False,
        max_length=5,
        )
    mobile_number = forms.CharField(
        required=False,
        max_length=15,
        label=_("Mobile"),
        )
    accept_inviter = forms.BooleanField(
        required=False,
        label=_("Add the inviter to your contacts."),
        )
    accept_membership = forms.BooleanField(
        required=False,
        label=_("Accept membership at the group."),
        )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        initial = self.initial['username']
        if username != initial:
            suggested = get_unique_value(
                User,
                username or slugify("_".join(
                    cleaned_data['first_name'],
                    cleaned_data['last_name'],
                    )).replace("-", "_"),
                field_name="username",
                separator="_",
                )
            if username.lower() != suggested.lower():
                raise forms.ValidationError(_("This username is already used for another account. But you can use \"%s\" as your username.") % suggested)
        return username
    def clean_login_email(self):
        login_email = self.cleaned_data['login_email']
        initial = self.initial['login_email']
        if login_email != initial:
            if User.objects.filter(email=login_email).count():
                raise forms.ValidationError(_("This email address is already used for another account."))
        return login_email
    def clean_login_email_confirm(self):
        if not 'login_email' in self.cleaned_data:
            raise forms.ValidationError(_("Please, correct the error for the login email at first."))
        login_email = self.cleaned_data['login_email']
        login_email_confirm = self.cleaned_data['login_email_confirm']
        if login_email != login_email_confirm:
            raise forms.ValidationError(_("The confirmed e-mail doesn't match the e-mail."))
        return login_email
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) <3 :
            raise forms.ValidationError(_("Passwords must be at least 3 characters long"))
        return password
    def clean_password_confirm(self):
        if not 'password' in self.cleaned_data:
            raise forms.ValidationError(_("Please, correct the error for the password at first."))
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError(_("The confirmed password doesn't match the password."))
        return password
    def clean_privacy_policy(self):
        privacy_policy = self.cleaned_data['privacy_policy']
        if not privacy_policy:
            raise forms.ValidationError(_("You must accept the privacy policy to register."))
        return privacy_policy
    def clean_terms_of_use(self):
        terms_of_use = self.cleaned_data['terms_of_use']
        if not terms_of_use:
            raise forms.ValidationError(_("You must accept the terms of use to register."))
        return terms_of_use

