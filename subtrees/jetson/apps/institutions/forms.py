# -*- coding: UTF-8 -*-
import os

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.db import models
from django.utils.timezone import now as tz_now

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField

from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType
from base_libs.utils.misc import get_related_queryset, get_unique_value, XChoiceList
from base_libs.utils.betterslugify import better_slugify
from base_libs.middleware import get_current_user

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

image_mods = models.get_app("image_mods")

app = models.get_app("people")
Person, IndividualContact, URL_ID_PERSON, URL_ID_PEOPLE = (
    app.Person,
    app.IndividualContact,
    app.URL_ID_PERSON,
    app.URL_ID_PEOPLE,
)

app = models.get_app("institutions")
Institution, InstitutionalContact, URL_ID_INSTITUTION, URL_ID_INSTITUTIONS = (
    app.Institution, app.InstitutionalContact, app.URL_ID_INSTITUTION,
    app.URL_ID_INSTITUTIONS
)
LegalForm = app.LegalForm

WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

LEGAL_FORM_CHOICES = XChoiceList(
    get_related_queryset(Institution, 'legal_form')
)

ESTABLISHMENT_YYYY_CHOICES = Institution._meta.get_field('establishment_yyyy'
                                                        ).get_choices()
ESTABLISHMENT_YYYY_CHOICES[0] = ("", _("Year"))
ESTABLISHMENT_MM_CHOICES = Institution._meta.get_field('establishment_mm'
                                                      ).get_choices()
ESTABLISHMENT_MM_CHOICES[0] = ("", _("Month"))

URL_TYPE_CHOICES = XChoiceList(
    get_related_queryset(IndividualContact, 'url0_type')
)
IM_TYPE_CHOICES = XChoiceList(
    get_related_queryset(IndividualContact, 'im0_type')
)
LOCATION_TYPE_CHOICES = XChoiceList(
    get_related_queryset(IndividualContact, 'location_type')
)
INSTITUTION_LOCATION_TYPE_CHOICES = XChoiceList(
    get_related_queryset(InstitutionalContact, 'location_type')
)

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE

# Collect translatable strings
_("Apply to all days")

### ADD INSTITUTION ###


class MainDataForm(dynamicforms.Form):
    institution_name = forms.CharField(
        required=True,
        label=_("Institution Name"),
    )

    institution_name2 = forms.CharField(
        required=False,
        label=_("Institution Name 2nd line"),
    )

    legal_form = forms.ChoiceField(
        required=True,
        choices=LEGAL_FORM_CHOICES,
        label=_("Legal Form"),
    )

    location_type = forms.ChoiceField(
        required=True,
        label=_("Location type"),
        choices=INSTITUTION_LOCATION_TYPE_CHOICES,
    )
    location_title = forms.CharField(
        required=False,
        label=_("Location title"),
        max_length=255,
    )
    street_address = forms.CharField(
        required=True,
        label=_("Street Address"),
    )
    street_address2 = forms.CharField(
        required=False,
        label=_("Street Address (2nd line)"),
    )
    city = forms.CharField(
        required=True,
        label=_("City"),
        error_messages={
            'required': _("City is required"),
        },
    )
    postal_code = forms.CharField(
        required=True,
        label=_("Postal Code"),
        error_messages={
            'required': _("Postal code is required"),
        },
    )
    district = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            "class": "form_hidden",
        }),
    )
    country = forms.ChoiceField(
        required=True,
        choices=Address._meta.get_field("country").get_choices(),
        label=_("Country"),
    )
    longitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            "class": "form_hidden",
        }),
    )
    latitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            "class": "form_hidden",
        }),
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
    email0 = forms.EmailField(
        required=False,
        label=_("E-mail"),
    )
    email1 = forms.EmailField(
        required=False,
        label=_("E-mail"),
    )
    email2 = forms.EmailField(
        required=False,
        label=_("E-mail"),
    )
    url0_type = forms.ChoiceField(
        required=False,
        choices=URL_TYPE_CHOICES,
        label=_("Type"),
    )
    url0_link = forms.URLField(
        required=False,
        label=_("URL"),
    )
    url1_type = forms.ChoiceField(
        required=False,
        choices=URL_TYPE_CHOICES,
        label=_("Type"),
    )
    url1_link = forms.URLField(
        required=False,
        label=_("URL"),
    )
    url2_type = forms.ChoiceField(
        required=False,
        choices=URL_TYPE_CHOICES,
        label=_("Type"),
    )
    url2_link = forms.URLField(
        required=False,
        label=_("URL"),
    )
    im0_type = forms.ChoiceField(
        required=False,
        choices=IM_TYPE_CHOICES,
        label=_("Type"),
    )
    im0_address = forms.CharField(
        required=False,
        max_length=255,
        label=_("Address"),
    )
    im1_type = forms.ChoiceField(
        required=False,
        choices=IM_TYPE_CHOICES,
        label=_("Type"),
    )
    im1_address = forms.CharField(
        required=False,
        max_length=255,
        label=_("Address"),
    )
    im2_type = forms.ChoiceField(
        required=False,
        choices=IM_TYPE_CHOICES,
        label=_("Type"),
    )
    im2_address = forms.CharField(
        required=False,
        max_length=255,
        label=_("Address"),
    )

    def __init__(self, *args, **kwargs):
        super(MainDataForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Institution"),
                "institution_name",
                "institution_name2",
                "legal_form",
            ),
            layout.Fieldset(
                string_concat(_("Address"), "-", _("Institution")),
                "location_type",
                "location_title",
            ),
            layout.Fieldset(
                _("Address"),
                "latitude",  # hidden field
                "longitude",  # hidden field
                "district",  # hidden field
                "street_address",
                "street_address2",
                layout.Row(
                    layout.Div(
                        "postal_code",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "city",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                "country",
                layout.HTML(
                    """{% include "bootstrap3/custom_widgets/editable_map.html" %}"""
                ),
                css_id="fieldset_institution_select",
            ),
            layout.Fieldset(
                _("Phones"),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Phone")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "phone_country",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "phone_area",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "phone_number",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Fax")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fax_country",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fax_area",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fax_number",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Mobile")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mobile_country",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mobile_area",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mobile_number",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
            ),
            layout.Fieldset(
                _("Emails"),
                "email0",
                "email1",
                "email2",
            ),
            layout.Fieldset(
                _("Websites"),
                layout.Row(
                    layout.Div(
                        "url0_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "url0_link",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "url1_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "url1_link",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "url2_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "url2_link",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
            ),
            layout.Fieldset(
                _("Instant Messengers"),
                layout.Row(
                    layout.Div(
                        "im0_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "im0_address",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "im1_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "im1_address",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "im2_type",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "im2_address",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
            ),
            bootstrap.FormActions(layout.Submit('submit', _('Next')), )
        )


class ProfileForm(dynamicforms.Form):
    description_en = forms.CharField(
        required=False,
        label=_("Description (English)"),
        widget=forms.Textarea,
    )
    description_de = forms.CharField(
        required=False,
        label=_("Description (German)"),
        widget=forms.Textarea,
    )
    avatar = ImageField(
        label=_("Profile photo"),
        help_text=_(
            "You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px."
        ) % STR_LOGO_SIZE,
        required=False,
        min_dimensions=LOGO_SIZE,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Description"),
                "description_de",
                "description_en",
            ),
            layout.Fieldset(
                _("Photo"),
                layout.HTML(
                    """{% load image_modifications %}
                    {% if form_step_data.1.avatar %}
                        <img src="/helper/tmpimage/{{ form_step_data.1.avatar.tmp_filename }}/{{ LOGO_PREVIEW_SIZE }}/" alt="{{ object.get_title|escape }}"/>
                    {% else %}
                        <img src="{{ DEFAULT_FORM_LOGO_4_INSTITUTION }}" alt="{{ object.get_title|escape }}"/>
                    {% endif %}
                """
                ),
                "avatar",
            ),
            bootstrap.FormActions(
                layout.Submit('reset', _('Reset')),
                layout.HTML(
                    """{% include "bootstrap3/custom_widgets/previous_button.html" %}"""
                ),
                layout.Submit('submit', _('Next')),
            )
        )


class OpeningHoursPaymentForm(dynamicforms.Form):
    """
    Form for opening ours and payment data
    """

    show_breaks = forms.BooleanField(
        required=False,
        label=_("Morning/Afternoon"),
        initial=False,
    )

    is_appointment_based = forms.BooleanField(
        label=_("Visiting by Appointment"),
        required=False,
        initial=False,
    )

    mon_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    mon_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    mon_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    mon_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    mon_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    tue_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    tue_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    tue_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    tue_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    tue_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    wed_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    wed_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    wed_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    wed_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    wed_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    thu_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    thu_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    thu_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    thu_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    thu_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    fri_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    fri_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    fri_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    fri_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    fri_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sat_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    sat_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    sat_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    sat_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    sat_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sun_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
    )
    sun_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    sun_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
    )
    sun_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
    )
    sun_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    exceptions_en = forms.CharField(
        label=_('Exceptions for working hours (English)'),
        required=False,
        widget=forms.Textarea,
    )
    exceptions_de = forms.CharField(
        label=_('Exceptions for working hours (German)'),
        required=False,
        widget=forms.Textarea,
    )

    # Payment
    is_card_visa_ok = forms.BooleanField(
        label=_("Visa"),
        required=False,
        initial=False,
    )

    is_card_mastercard_ok = forms.BooleanField(
        label=_("MasterCard"),
        required=False,
        initial=False,
    )

    is_card_americanexpress_ok = forms.BooleanField(
        label=_("American Express"),
        required=False,
        initial=False,
    )

    is_paypal_ok = forms.BooleanField(
        label=_("PayPal"),
        required=False,
        initial=False,
    )

    is_cash_ok = forms.BooleanField(
        label=_("Cash"),
        required=False,
        initial=False,
    )

    is_transaction_ok = forms.BooleanField(
        label=_("Bank transfer"),
        required=False,
        initial=False,
    )

    is_prepayment_ok = forms.BooleanField(
        label=_("Prepayment"),
        required=False,
        initial=False,
    )

    is_on_delivery_ok = forms.BooleanField(
        label=_("Payment on delivery"),
        required=False,
        initial=False,
    )

    is_invoice_ok = forms.BooleanField(
        label=_("Invoice"),
        required=False,
        initial=False,
    )

    is_ec_maestro_ok = forms.BooleanField(
        label=_("EC Maestro"),
        required=False,
        initial=False,
    )

    is_giropay_ok = forms.BooleanField(
        label=_("Giropay"),
        required=False,
        initial=False,
    )

    def __init__(self, *args, **kwargs):
        super(OpeningHoursPaymentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                string_concat(_("Opening Time"), " - ", _("Closing Time")),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Monday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_is_closed",
                        "show_breaks",
                        layout.HTML(
                            """{% load i18n %}
                            <p>
                                <a id="id_apply_all_days" href="#">{% trans "Apply to all days" %}</a>
                            </p>
                        """
                        ),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "mon_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Tuesday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "tue_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Wednesday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "wed_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Thursday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "thu_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Friday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "fri_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Saturday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sat_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Sunday")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_open0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_close0",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_is_closed",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_open1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "sun_close1",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                "exceptions_de",
                "exceptions_en",
                "is_appointment_based",
            ),
            layout.Fieldset(
                _("Payment Options"),
                layout.Row(
                    layout.Div(
                        "is_cash_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_card_visa_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "is_invoice_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_card_mastercard_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "is_on_delivery_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_card_americanexpress_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "is_ec_maestro_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_giropay_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        "is_prepayment_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                    layout.Div(
                        "is_paypal_ok",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ),
                ),
            ),
            bootstrap.FormActions(
                layout.Submit('reset', _('Reset')),
                layout.HTML(
                    """{% load i18n %}
                    <button class="btn" onclick="window.redirect(document.location.pathname + '?step=' + ({{ form_step_data.step_counter|default:"0" }} - 1))">
                        {% trans "Previous" %}
                    </button>
                """
                ),
                layout.Submit('submit', _('Next')),
            )
        )

    def clean(self):

        show_breaks = self.cleaned_data.get('show_breaks', False)
        for week_day in WEEK_DAYS:

            is_closed = self.cleaned_data.get(week_day + '_is_closed', False)
            open0 = self.cleaned_data.get(week_day + '_open0', None)
            close0 = self.cleaned_data.get(week_day + '_close0', None)
            open1 = self.cleaned_data.get(week_day + '_open1', None)
            close1 = self.cleaned_data.get(week_day + '_close1', None)

            # here, we apply opening hours and do some checks
            if not is_closed:
                if open0:
                    if not close0:
                        self._errors[week_day + '_open0'] = [
                            _("Please enter a closing time.")
                        ]
                    elif close0 < open0:
                        self._errors[week_day + '_open0'] = [
                            _(
                                "A closing time must not be before an opening time."
                            )
                        ]
                if close0:
                    if not open0:
                        self._errors[week_day + '_open0'] = [
                            _("Please enter an opening time.")
                        ]

                if show_breaks:
                    if open1:
                        if not close1:
                            self._errors[week_day + '_open1'] = [
                                _("Please enter a closing time.")
                            ]
                        elif close1 < open1:
                            self._errors[week_day + '_open1'] = [
                                _(
                                    "A closing time must not be before an opening time."
                                )
                            ]
                    if close1:
                        if not open1:
                            self._errors[week_day + '_open1'] = [
                                _("Please enter an opening time.")
                            ]

                    if open1 or close1:
                        if not open0 or not close0:
                            self._errors[week_day + '_open1'] = [
                                _(
                                    "When specifying breaks, you must enter all data."
                                )
                            ]
                        else:
                            if open1 < close0:
                                self._errors[week_day + '_open1'] = [
                                    _(
                                        "An opening time after break must not be before the closing time to break."
                                    )
                                ]

                    if open0 and open1 and close0 and close1:
                        self.cleaned_data[week_day + '_open'] = open0
                        self.cleaned_data[week_day + '_break_close'] = close0
                        self.cleaned_data[week_day + '_break_open'] = open1
                        self.cleaned_data[week_day + '_close'] = close1
                    elif open0 and close0:
                        self.cleaned_data[week_day + '_open'] = open0
                        self.cleaned_data[week_day + '_close'] = close0
                else:
                    if open0 and close0:
                        self.cleaned_data[week_day + '_open'] = open0
                        self.cleaned_data[week_day + '_close'] = close0
        return self.cleaned_data


class CategoriesForm(dynamicforms.Form):
    # TODO: rework categories form
    choose_creative_sectors = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput(attrs={
            "class": "form_hidden",
        }),
        required=False,
    )

    def clean_choose_creative_sectors(self):
        data = self.data
        el_count = 0
        for el in self.creative_sectors.values():
            if el['field_name'] in data:
                el_count += 1
        if not el_count:
            raise forms.ValidationError(
                _("Please choose at least one creative sector.")
            )
        return True

    choose_context_categories = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput(attrs={
            "class": "form_hidden",
        }),
        required=False,
    )

    def clean_choose_context_categories(self):
        data = self.data
        el_count = 0
        for el in self.context_categories.values():
            if el['field_name'] in data:
                el_count += 1
        if not el_count:
            raise forms.ValidationError(
                _("Please choose at least one context category.")
            )
        return True

    choose_object_types = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput(attrs={
            "class": "form_hidden",
        }),
        required=False,
    )

    def clean_choose_object_types(self):
        data = self.data
        el_count = 0
        for el in self.object_types.values():
            if el['field_name'] in data:
                el_count += 1
        if not el_count:
            raise forms.ValidationError(
                _("Please choose at least one object type.")
            )
        return True

    def __init__(self, *args, **kwargs):
        super(CategoriesForm, self).__init__(*args, **kwargs)

        self.creative_sectors = {}
        for item in get_related_queryset(Institution, "creative_sectors"):
            self.creative_sectors[item.sysname] = {
                'id': item.id,
                'field_name': PREFIX_CI + str(item.id),
            }

        self.context_categories = {}
        for item in get_related_queryset(Institution, "context_categories"):
            self.context_categories[item.sysname] = {
                'id': item.id,
                'field_name': PREFIX_BC + str(item.id),
            }

        self.object_types = {}
        for item in get_related_queryset(Institution, "institution_types"):
            self.object_types[item.slug] = {
                'id': item.id,
                'field_name': PREFIX_OT + str(item.id),
            }

        for s in self.creative_sectors.values():
            self.fields[s['field_name']] = forms.BooleanField(required=False)

        for c in self.context_categories.values():
            self.fields[c['field_name']] = forms.BooleanField(required=False)

        for t in self.object_types.values():
            self.fields[t['field_name']] = forms.BooleanField(required=False)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Categories"),
                "choose_creative_sectors",
                "choose_context_categories",
                "choose_object_types",
            ),
            bootstrap.FormActions(
                layout.Submit('reset', _('Reset')),
                layout.HTML(
                    """{% load i18n %}
                    <button class="btn" onclick="window.redirect(document.location.pathname + '?step=' + ({{ form_step_data.step_counter|default:"0" }} - 1))">
                        {% trans "Previous" %}
                    </button>
                """
                ),
                layout.Submit('submit', _('Next')),
            )
        )


def submit_step(current_step, form_steps, form_step_data):
    return form_step_data


def save_data(form_steps, form_step_data):
    user = get_current_user()

    ### DEBUG ###
    import pprint
    fpath = os.path.join(settings.PATH_TMP, "institution_creation.log")
    f = open(fpath, "a")
    f.write(str(tz_now()) + "\n")
    f.write(user.username + "\n")
    pprint.pprint(form_step_data, f)
    f.write("-----\n")
    f.close()
    ### /DEBUG ###

    institution = Institution(
        title=form_step_data[0].get('institution_name', ''),
        title2=form_step_data[0].get('institution_name2', ''),
        slug=get_unique_value(
            Institution,
            better_slugify(form_step_data[0].get('institution_name',
                                                 '')).replace("-", "_"),
            separator="_"
        ),
        status="published",
    )
    institution.legal_form = LegalForm.objects.get(
        id=form_step_data[0]['legal_form'],
    )

    institution.description_en = form_step_data[1].get('description_en', None)
    institution.description_de = form_step_data[1].get('description_de', None)

    # opening hours
    for f in ("open", "break_close", "break_open", "close"):
        for d in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
            setattr(
                institution, "%s_%s" % (d, f),
                form_step_data[2].get('%s_%s' % (d, f), None)
            )

    institution.exceptions_en = form_step_data[2].get('exceptions_en', '')
    institution.exceptions_de = form_step_data[2].get('exceptions_de', '')
    institution.is_appointment_based = form_step_data[2].get(
        'is_appointment_based', False
    )

    # payment
    institution.is_card_visa_ok = form_step_data[2].get('is_card_visa_ok', None)
    institution.is_card_mastercard_ok = form_step_data[2].get(
        'is_card_mastercard_ok', None
    )
    institution.is_card_americanexpress_ok = form_step_data[2].get(
        'is_card_americanexpress_ok', None
    )
    institution.is_paypal_ok = form_step_data[2].get('is_paypal_ok', None)
    institution.is_cash_ok = form_step_data[2].get('is_cash_ok', None)
    institution.is_transaction_ok = form_step_data[2].get(
        'is_transaction_ok', None
    )
    institution.is_prepayment_ok = form_step_data[2].get(
        'is_prepayment_ok', None
    )
    institution.is_on_delivery_ok = form_step_data[2].get(
        'is_on_delivery_ok', None
    )
    institution.is_invoice_ok = form_step_data[2].get('is_invoice_ok', None)
    institution.is_ec_maestro_ok = form_step_data[2].get(
        'is_ec_maestro_ok', None
    )
    institution.is_giropay_ok = form_step_data[2].get('is_giropay_ok', None)

    # save the institution to get its id for database relations used further
    institution.save()

    institutional_contact = institution.institutionalcontact_set.create(
        location_type_id=form_step_data[0].get('location_type', ''),
        location_title=form_step_data[0].get('institution_name', ''),
        is_primary=True,
        is_temporary=False,
        phone0_type=PhoneType.objects.get(slug='phone'),
        phone0_country=form_step_data[0].get('phone_country', ''),
        phone0_area=form_step_data[0].get('phone_area', ''),
        phone0_number=form_step_data[0].get('phone_number', ''),
        phone1_type=PhoneType.objects.get(slug='fax'),
        phone1_country=form_step_data[0].get('fax_country', ''),
        phone1_area=form_step_data[0].get('fax_area', ''),
        phone1_number=form_step_data[0].get('fax_number', ''),
        url0_type_id=form_step_data[0].get('url0_type', None),
        url1_type_id=form_step_data[0].get('url1_type', None),
        url2_type_id=form_step_data[0].get('url2_type', None),
        url0_link=form_step_data[0].get('url0_link', ''),
        url1_link=form_step_data[0].get('url1_link', ''),
        url2_link=form_step_data[0].get('url2_link', ''),
        im0_type_id=form_step_data[0].get('im0_type', None),
        im1_type_id=form_step_data[0].get('im1_type', None),
        im2_type_id=form_step_data[0].get('im2_type', None),
        im0_address=form_step_data[0].get('im0_address', ''),
        im1_address=form_step_data[0].get('im1_address', ''),
        im2_address=form_step_data[0].get('im2_address', ''),
        email0_address=form_step_data[0].get('email0_address', ''),
        email1_address=form_step_data[0].get('email1_address', ''),
        email2_address=form_step_data[0].get('email2_address', ''),
    )

    Address.objects.set_for(
        institutional_contact,
        "postal_address",
        country=form_step_data[0].get('country', ''),
        district=form_step_data[0].get('district', ''),
        city=form_step_data[0].get('city', ''),
        street_address=form_step_data[0].get('street_address', ''),
        street_address2=form_step_data[0].get('street_address2', ''),
        postal_code=form_step_data[0].get('postal_code', ''),
        latitude=form_step_data[0].get('latitude', ''),
        longitude=form_step_data[0].get('longitude', ''),
    )

    if hasattr(institution, "create_default_group"):
        person_group = institution.create_default_group()
        person_group.content_object = institution
        person_group.save()
        membership = person_group.groupmembership_set.create(
            user=user,
            role="owners",
            inviter=user,
            confirmer=user,
            is_accepted=True,
        )

    cleaned = form_step_data[3]
    selected_cs = {}
    for item in get_related_queryset(Institution, "creative_sectors"):
        if cleaned.get(PREFIX_CI + str(item.id), False):
            # remove all the parents
            for ancestor in item.get_ancestors():
                if ancestor.id in selected_cs:
                    del (selected_cs[ancestor.id])
            # add current
            selected_cs[item.id] = item
    institution.creative_sectors.add(*selected_cs.values())

    selected_cc = {}
    for item in get_related_queryset(Institution, "context_categories"):
        if cleaned.get(PREFIX_BC + str(item.id), False):
            # remove all the parents
            for ancestor in item.get_ancestors():
                if ancestor.id in selected_cc:
                    del (selected_cc[ancestor.id])
            # add current
            selected_cc[item.id] = item
    institution.context_categories.add(*selected_cc.values())

    selected_ot = {}
    for item in get_related_queryset(Institution, "institution_types"):
        if cleaned.get(PREFIX_OT + str(item.id), False):
            # remove all the parents
            for ancestor in item.get_ancestors():
                if ancestor.id in selected_cs:
                    del (selected_cs[ancestor.id])
            # add current
            selected_ot[item.id] = item
    institution.institution_types.add(*selected_ot.values())

    media_file = form_step_data[1].get('avatar', '')
    if media_file:
        tmp_path = os.path.join(settings.PATH_TMP, media_file['tmp_filename'])
        f = open(tmp_path, 'r')
        filename = tmp_path.rsplit("/", 1)[1]
        image_mods.FileManager.save_file_for_object(
            institution, filename, f.read(), subpath="avatar/"
        )
        f.close()

    # save again triggering signals
    # TODO: check what happens around institution saving: what signals are called and what notifications are created
    # minimize or rework long-lasting tasks
    institution.save()

    # this is used for redirection to the institution details page
    form_steps['success_url'] = institution.get_url_path()
    return form_step_data


ADD_INSTITUTION_FORM_STEPS = {
    0:
        {
            'title': _("main data"),
            'template': "institutions/add_institution_main_data.html",
            'form': MainDataForm,
            'initial_data':
                {
                    'url0_link': 'http://',
                    'url1_link': 'http://',
                    'url2_link': 'http://',
                },
        },
    1:
        {
            'title': _("profile data"),
            'template': "institutions/add_institution_profile.html",
            'form': ProfileForm,
        },
    2:
        {
            'title': _("opening hours and payment"),
            'template': "institutions/add_institution_opening_hours.html",
            'form': OpeningHoursPaymentForm,
        },
    3:
        {
            'title': _("categories"),
            'template': "institutions/add_institution_categories.html",
            'form': CategoriesForm,
        },
    4:
        {
            'title': _("confirm data"),
            'template': "institutions/add_institution_confirm.html",
            'form': forms.Form,  # dummy form
        },
    'onsubmit': submit_step,
    'onsave': save_data,
    'name': 'add_institution',
    'success_url': "/%s/" % URL_ID_INSTITUTIONS,
    'default_path': [0, 1, 2, 3, 4],
}
