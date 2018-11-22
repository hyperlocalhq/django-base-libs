# -*- coding: UTF-8 -*-
import re
from datetime import time
from datetime import datetime

from django.db import models
from django import forms
from django.forms.models import modelform_factory
from django.forms.models import inlineformset_factory
from django.template import loader, RequestContext, Template
from django.contrib.auth.models import User
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin import widgets
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.utils.misc import is_installed
from base_libs.utils.misc import get_related_queryset
from base_libs.widgets import TreeSelectWidget, TreeSelectMultipleWidget
from base_libs.forms.fields import AutocompleteModelChoiceField

from jetson.apps.location.models import Address, Locality, Geoposition

CONTACT_DATA_FIELDS = []
for i in range(3):
    CONTACT_DATA_FIELDS.extend(
        [
            'phone%d_country' % i,
            'phone%d_area' % i,
            'phone%d_number' % i,
            'url%d_link' % i,
            'email%d_address' % i,
            'im%d_address' % i,
        ]
    )
    for c in ('phone', 'email', 'im', 'url'):
        CONTACT_DATA_FIELDS.extend(
            ['is_%s%d_default' % (c, i),
             'is_%s%d_on_hold' % (c, i)]
        )

FIELDS_FROM_INDIVIDUAL_CONTACT_MODEL = [
    'location_title', 'is_primary', 'institutional_title', 'is_billing_address',
    'is_shipping_address', 'is_seasonal', 'validity_start_yyyy',
    'validity_start_mm', 'validity_start_dd', 'validity_end_yyyy',
    'validity_end_mm', 'validity_end_dd'
]
FIELDS_FROM_INDIVIDUAL_CONTACT_MODEL.extend(CONTACT_DATA_FIELDS)

FIELDS_FROM_INSTITUTIONAL_CONTACT_MODEL = [
    'location_title', 'is_primary', 'is_billing_address', 'is_shipping_address',
    'is_temporary', 'validity_start_yyyy', 'validity_start_mm',
    'validity_start_dd', 'validity_end_yyyy', 'validity_end_mm',
    'validity_end_dd'
]
FIELDS_FROM_INSTITUTIONAL_CONTACT_MODEL.extend(CONTACT_DATA_FIELDS)

FIELDS_FROM_USER_MODEL = ('first_name', 'last_name', 'email', 'username')
FIELDS_FROM_ADDRESS_MODEL = (
    'country', 'state', 'city', 'street_address', 'street_address2',
    'street_address3', 'postal_code'
)
FIELDS_FROM_LOCALITY_MODEL = ('district', 'neighborhood')
FIELDS_FROM_GEOPOSITION_MODEL = ('latitude', 'longitude', 'altitude')


def add_form_fields(form, modelform):
    for field_name, field in modelform.base_fields.items():
        setattr(form, field_name, field)
        form.fields[field_name] = field


def formfield_for_dbfield(db_field, **kwargs):
    """
    If kwargs are given, they're passed to the form Field's constructor.
    """

    # If the field specifies choices, we don't need to look for special
    # admin widgets - we just need to use a select widget of some kind.

    #if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
    #    try:
    #        # if a foreign key points to a model which has a field "parent"..
    #        db_field.rel.to._meta.get_field("parent")
    #    except models.FieldDoesNotExist:
    #        pass
    #    else:
    #        # .. then display the select options in a hierarchical view
    #        if isinstance(db_field, models.ForeignKey):
    #            kwargs['widget'] = TreeSelectWidget(
    #                model=db_field.rel.to,
    #                choices=db_field.choices,
    #                )
    #        else:
    #            kwargs['widget'] = TreeSelectMultipleWidget(
    #                model=db_field.rel.to,
    #                choices=db_field.choices,
    #                )

    # For fields that have choices do not overwrite the widget
    #el
    if db_field.choices:
        pass

    # For DateTimeFields, use a special field and widget.
    elif isinstance(db_field, models.DateTimeField):
        kwargs['form_class'] = forms.SplitDateTimeField
        kwargs['widget'] = widgets.AdminSplitDateTime()

    # For DateFields, add a custom CSS class.
    elif isinstance(db_field, models.DateField):
        kwargs['widget'] = widgets.AdminDateWidget

    # For TimeFields, add a custom CSS class.
    elif isinstance(db_field, models.TimeField):
        kwargs['widget'] = widgets.AdminTimeWidget

    # For TextFields, add a custom CSS class.
    elif isinstance(db_field, models.TextField):
        kwargs['widget'] = widgets.AdminTextareaWidget

    # For URLFields, add a custom CSS class.
    elif isinstance(db_field, models.URLField):
        kwargs['widget'] = widgets.AdminURLFieldWidget

    # For IntegerFields, add a custom CSS class.
    elif isinstance(db_field, models.IntegerField):
        kwargs['widget'] = widgets.AdminIntegerFieldWidget

    # For TextInputs, add a custom CSS class.
    elif isinstance(db_field, models.CharField):
        kwargs['widget'] = widgets.AdminTextInputWidget

    # For FileFields and ImageFields add a link to the current file.
    elif isinstance(db_field, (models.ImageField, models.FileField)):
        kwargs['widget'] = widgets.AdminFileWidget

    if re.search('markup_type$', db_field.name):
        kwargs['widget'] = forms.Select(attrs={'class': "markupType"})

    return db_field.formfield(**kwargs)


AddressForm = modelform_factory(
    Address,
    exclude=["id"],
    formfield_callback=formfield_for_dbfield,
)
LocalityForm = modelform_factory(
    Locality,
    exclude=["id", "address"],
    formfield_callback=formfield_for_dbfield,
)
GeopositionForm = modelform_factory(
    Geoposition,
    exclude=["id", "address"],
    formfield_callback=formfield_for_dbfield,
)

if is_installed("people.models"):
    Person = models.get_model("people", "Person")
    IndividualContact = models.get_model("people", "IndividualContact")

    Institution = models.get_model("institutions", "Institution")

    UserForm = modelform_factory(
        User,
        fields=("first_name", "last_name", "email", "username"),
        formfield_callback=formfield_for_dbfield,
    )

    class PersonForm(forms.ModelForm):
        """
        Person form for administration
        Combines
        * all fields from Person model
        * several fields from User model
        * fields for setting/changing password
        """
        GENDER_CHOICES = Person._meta.get_field('gender').get_choices()
        GENDER_CHOICES[0] = ("", _("Unknown"))
        gender = forms.ChoiceField(
            widget=forms.RadioSelect(),
            choices=GENDER_CHOICES,
            required=not Person._meta.get_field('gender').blank,
        )

        formfield_callback = formfield_for_dbfield

        def __init__(self, *args, **kwargs):
            super(PersonForm, self).__init__(*args, **kwargs)

            add_form_fields(self, UserForm)

            # initial values from the User model should also be added
            # (only those which are necessary)
            if self.instance.id:
                user_form = UserForm(instance=self.instance.user)
            else:
                user_form = UserForm()
                # if it's a new person, the password is required
                self.fields['new_password'].required = True
                self.fields['new_password_confirm'].required = True

            self.initial.update(user_form.initial)

        def save(self, *args, **kwargs):
            user = None
            if self.instance.id:
                user = self.instance.user
            user_form = UserForm(
                self.cleaned_data,
                instance=user,
            )
            if user_form.is_valid():
                user = user_form.save(commit=False)
                if self.cleaned_data['new_password']:
                    user.set_password(self.cleaned_data['new_password'])
                user.save()  # creates a person by a signal
                user_form.save_m2m()
                person = Person.objects.get(user=user)
                if self.instance:
                    self.instance.pk = person.pk
                    self.instance.user = user
            return super(PersonForm, self).save(*args, **kwargs)

        class Meta:
            model = Person
            exclude = ("user", "description_markup_type")

        old_password = forms.CharField(
            widget=forms.PasswordInput,
            required=False,
            max_length=128,
        )
        new_password = forms.CharField(
            widget=forms.PasswordInput,
            required=False,
            max_length=128,
        )
        new_password_confirm = forms.CharField(
            widget=forms.PasswordInput,
            required=False,
            max_length=128,
        )

        def clean_old_password(self):
            """Validates that the old_password field is correct."""
            old_password = self.cleaned_data['old_password']
            if old_password and self.instance.id:
                if not self.instance.user.check_password(old_password):
                    raise forms.ValidationError, _(
                        "Your old password was entered incorrectly. Please enter it again."
                    )
            return old_password

        def clean(self):
            """Checks if the old password was entered if the user tries to change """
            cleaned_data = super(PersonForm, self).clean()

            user = None
            if self.instance.id:
                user = self.instance.user
            user_form = UserForm(
                cleaned_data,
                instance=user,
            )
            if not user_form.is_valid():
                self._errors.update(user_form._errors)

            old_password = cleaned_data.get('old_password', "")
            new_password = cleaned_data.get('new_password', "")
            new_password_confirm = cleaned_data.get('new_password_confirm', "")
            if new_password:
                if not old_password and self.instance.id:
                    raise forms.ValidationError, _(
                        "For security reasons your must enter the old password in order to change it to the new one."
                    )
                if new_password != new_password_confirm:
                    raise forms.ValidationError, _(
                        "Your confirmed password doesn't match the new password."
                    )
            return cleaned_data

    class IndividualContactForm(forms.ModelForm):
        """
        Individual-contact form for administration
        Combines
        * all fields from IndividualContact model
        * all fields from Address model
        * most fields from Locality model
        * most fields from Geoposition model
        """
        if Institution:
            institution = AutocompleteModelChoiceField(
                required=False,
                label=_("Company/Institution"),
                help_text=_(
                    "Please enter a letter to display a list of available institutions"
                ),
                app="institutions",
                qs_function="get_all_institutions",
                display_attr="title",
                add_display_attr="get_address_string",
                options={
                    "minChars": 1,
                    "max": 20,
                    "mustMatch": 1,
                    "highlight": False,
                }
            )

        def __init__(self, *args, **kwargs):
            super(IndividualContactForm, self).__init__(*args, **kwargs)
            add_form_fields(self, AddressForm)
            add_form_fields(self, LocalityForm)
            add_form_fields(self, GeopositionForm)

            self.country = self.fields['country'] = AutocompleteModelChoiceField(
                required=False,
                label=_("Country"),
                help_text=_(
                    "Please enter a letter to display a list of available countries"
                ),
                app="i18n",
                qs_function="get_countries",
                display_attr="get_name",
                options={
                    "minChars": 1,
                    "max": 20,
                    "mustMatch": 1,
                    "highlight": False,
                }
            )

            contact_id = self.initial.get("id", None)
            if contact_id:
                self.instance = IndividualContact.objects.get(pk=contact_id)

            # initial fields from the Address, Locality, and Geoposition models
            # should also be added (only those which are necessary)
            if self.instance.id and self.instance.postal_address:
                address_form = AddressForm(
                    instance=self.instance.postal_address,
                )
                locality_form = LocalityForm(
                    instance=self.instance.postal_address.get_locality(),
                )
                geoposition_form = GeopositionForm(
                    instance=self.instance.postal_address.get_geoposition(),
                )
            else:
                address_form = AddressForm()
                locality_form = LocalityForm()
                geoposition_form = GeopositionForm()

            self.initial.update(address_form.initial)
            self.initial.update(locality_form.initial)
            self.initial.update(geoposition_form.initial)

        # unfortunately save() method of this class is not used for saving formsets

        class Meta:
            model = IndividualContact
            exclude = ("postal_address", )

    IndividualContactFormSet = inlineformset_factory(
        parent_model=Person,
        model=IndividualContact,
        form=IndividualContactForm,
        extra=0,
        #max_num=0,
        can_delete=True,
        formfield_callback=formfield_for_dbfield,
    )

if is_installed("institutions.models"):
    Institution = models.get_model("institutions", "Institution")
    InstitutionalContact = models.get_model(
        "institutions", "InstitutionalContact"
    )

    class InstitutionForm(forms.ModelForm):
        """
        Institution form for administration
        """

        parent = AutocompleteModelChoiceField(
            required=False,
            label=_("Member of"),
            help_text=_(
                "Please enter a letter to display a list of available institutions"
            ),
            app="institutions",
            qs_function="get_all_institutions",
            display_attr="title",
            add_display_attr="get_address_string",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight": False,
            }
        )

        formfield_callback = formfield_for_dbfield

        class Meta:
            model = Institution
            exclude = ("description_markup_type", "exceptions_markup_type")

    class InstitutionalContactForm(forms.ModelForm):
        """
        Institutional-contact form for administration
        Combines
        * all fields from InstitutionalContact model
        * all fields from Address model
        * most fields from Locality model
        * most fields from Geoposition model
        """

        def __init__(self, *args, **kwargs):
            super(InstitutionalContactForm, self).__init__(*args, **kwargs)
            add_form_fields(self, AddressForm)
            add_form_fields(self, LocalityForm)
            add_form_fields(self, GeopositionForm)

            self.country = self.fields['country'] = AutocompleteModelChoiceField(
                required=False,
                label=_("Country"),
                help_text=_(
                    "Please enter a letter to display a list of available countries"
                ),
                app="i18n",
                qs_function="get_countries",
                display_attr="get_name",
                options={
                    "minChars": 1,
                    "max": 20,
                    "mustMatch": 1,
                    "highlight": False,
                }
            )

            contact_id = self.initial.get("id", None)
            if contact_id:
                self.instance = InstitutionalContact.objects.get(pk=contact_id)

            # initial fields from the Address, Locality, and Geoposition models
            # should also be added (only those which are necessary)
            if self.instance.id and self.instance.postal_address:
                address_form = AddressForm(
                    instance=self.instance.postal_address,
                )
                locality_form = LocalityForm(
                    instance=self.instance.postal_address.get_locality(),
                )
                geoposition_form = GeopositionForm(
                    instance=self.instance.postal_address.get_geoposition(),
                )
            else:
                address_form = AddressForm()
                locality_form = LocalityForm()
                geoposition_form = GeopositionForm()

            self.initial.update(address_form.initial)
            self.initial.update(locality_form.initial)
            self.initial.update(geoposition_form.initial)

        # unfortunately save() method of this class is not used for saving formsets

        class Meta:
            model = InstitutionalContact
            exclude = ("postal_address", )

    InstitutionalContactFormSet = inlineformset_factory(
        parent_model=Institution,
        model=InstitutionalContact,
        form=InstitutionalContactForm,
        extra=0,
        #max_num=0,
        can_delete=True,
        formfield_callback=formfield_for_dbfield,
    )

if is_installed("resources.models"):
    from django.contrib import admin
    from django.contrib.admin.widgets import ForeignKeyRawIdWidget, ManyToManyRawIdWidget
    Document = models.get_model("resources", "Document")
    Person = models.get_model("people", "Person")
    Institution = models.get_model("institutions", "Institution")

    class DocumentForm(forms.ModelForm):
        """
        Document form for administration
        """
        authors = forms.ModelMultipleChoiceField(
            label=_("Authors"),
            required=False,
            queryset=Person.objects.all().only("id", "person_repr"),
            widget=ManyToManyRawIdWidget(
                Document._meta.get_field('authors').rel, admin.site
            )
        )
        publisher = forms.ModelChoiceField(
            label=_("Publisher"),
            required=False,
            queryset=Institution.objects.all().only("id", "title", "title2"),
            widget=ForeignKeyRawIdWidget(
                Document._meta.get_field('publisher').rel, admin.site
            )
        )
        formfield_callback = formfield_for_dbfield

        class Meta:
            model = Document
            exclude = ("description_markup_type", )
