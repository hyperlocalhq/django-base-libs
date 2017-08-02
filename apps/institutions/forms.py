# -*- coding: UTF-8 -*-
import os

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.db import models
from django.utils.timezone import now as tz_now

from mptt.forms import TreeNodeChoiceField

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.utils.misc import get_related_queryset, get_unique_value, XChoiceList
from base_libs.utils.betterslugify import better_slugify
from base_libs.middleware import get_current_user

from jetson.apps.location.models import LocalityType
from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType
from jetson.apps.utils.forms import ModelMultipleChoiceTreeField
from jetson.apps.utils.forms import ModelChoiceTreeField

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

image_mods = models.get_app("image_mods")

app = models.get_app("people")
Person, IndividualContact, URL_ID_PERSON, URL_ID_PEOPLE = (
    app.Person, app.IndividualContact, app.URL_ID_PERSON, app.URL_ID_PEOPLE,
)

app = models.get_app("institutions")
Institution, InstitutionalContact, URL_ID_INSTITUTION, URL_ID_INSTITUTIONS = (
    app.Institution, app.InstitutionalContact,
    app.URL_ID_INSTITUTION, app.URL_ID_INSTITUTIONS
)
LegalForm = app.LegalForm

WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

LEGAL_FORM_CHOICES = XChoiceList(get_related_queryset(Institution, 'legal_form'))

ESTABLISHMENT_YYYY_CHOICES = Institution._meta.get_field('establishment_yyyy').get_choices()
ESTABLISHMENT_YYYY_CHOICES[0] = ("", _("Year"))
ESTABLISHMENT_MM_CHOICES = Institution._meta.get_field('establishment_mm').get_choices()
ESTABLISHMENT_MM_CHOICES[0] = ("", _("Month"))

URL_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'url0_type'))
IM_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'im0_type'))
LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'location_type'))
INSTITUTION_LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(InstitutionalContact, 'location_type'))

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
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
    )
    country = forms.ChoiceField(
        required=True,
        choices=Address._meta.get_field("country").get_choices(),
        label=_("Country"),
    )
    longitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
    )
    latitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
    )
    phone_country = forms.CharField(
        label=_("Phone Country Code"),
        required=False,
        max_length=4,
        initial="49",
    )
    phone_area = forms.CharField(
        label=_("Phone Area Code"),
        required=False,
        max_length=5,
    )
    phone_number = forms.CharField(
        label=_("Phone number"),
        required=False,
        max_length=15,
    )
    fax_country = forms.CharField(
        label=_("Fax Country Code"),
        required=False,
        max_length=4,
        initial="49",
    )
    fax_area = forms.CharField(
        label=_("Fax Area Code"),
        required=False,
        max_length=5,
    )
    fax_number = forms.CharField(
        label=_("Fax Number"),
        required=False,
        max_length=15,
    )
    mobile_country = forms.CharField(
        label=_("Mobile Country Code"),
        required=False,
        max_length=4,
        initial="49",
    )
    mobile_area = forms.CharField(
        label=_("Mobile Area Code"),
        required=False,
        max_length=5,
    )
    mobile_number = forms.CharField(
        label=_("Mobile Number"),
        required=False,
        max_length=15,
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
                layout.MultiField(
                    string_concat(_('ZIP'), "*, ", _('City'), "*"),
                    layout.Field(
                        "postal_code",
                        wrapper_class = "col-xs-4 col-sm-5 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "city",
                        wrapper_class = "col-xs-8 col-sm-7 col-md-9 col-lg-9",
                        template = "ccb_form/multifield.html"
                    )
                ),
                "country",
                layout.HTML("""{% include "ccb_form/custom_widgets/editable_map.html" %}"""),
                css_id="fieldset_institution_select",
            ),
            layout.Fieldset(
                _("Phones"),
                layout.MultiField(
                    _("Phone"),
                    layout.Field(
                        "phone_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    _("Fax"),
                    layout.Field(
                        "fax_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fax_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fax_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    _("Mobile"),
                    layout.Field(
                        "mobile_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mobile_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mobile_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels"
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
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Url')),
                    layout.Field(
                        "url0_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template="ccb_form/multifield.html",
                    ),
                    layout.Field(
                        "url0_link",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template="ccb_form/multifield.html",
                        placeholder="http://",
                    ),
                ),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Url')),
                    layout.Field(
                        "url1_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template="ccb_form/multifield.html",
                    ),
                    layout.Field(
                        "url1_link",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template="ccb_form/multifield.html",
                        placeholder="http://",
                    ),
                ),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Url')),
                    layout.Field(
                        "url2_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template="ccb_form/multifield.html",
                    ),
                    layout.Field(
                        "url2_link",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template="ccb_form/multifield.html",
                        placeholder="http://",
                    ),
                ),
            ),
            layout.Fieldset(
                _("Instant Messengers"),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Address')),
                    layout.Field(
                        "im0_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "im0_address",
                        wrapper_class="col-xs-6 col-sm-6 col-md-8 col-lg-8",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Address')),
                    layout.Field(
                        "im1_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "im1_address",
                        wrapper_class="col-xs-6 col-sm-6 col-md-8 col-lg-8",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    string_concat(_('Type'), ", ", _('Address')),
                    layout.Field(
                        "im2_type",
                        wrapper_class="col-xs-6 col-sm-6 col-md-4 col-lg-4",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "im2_address",
                        wrapper_class="col-xs-6 col-sm-6 col-md-8 col-lg-8",
                        template = "ccb_form/multifield.html"
                    ),
                ),
            ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
            )
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
        label=' ',
        help_text=_(
            "You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_LOGO_SIZE,
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
                layout.HTML("""{% load image_modifications %}
                    {% if form_step_data.1.avatar %}
                        <dt>"""+(_("Profile photo")+"")+"""</dt><dd><img class="avatar" src="/{{ LANGUAGE_CODE }}/helper/tmpimage/{{ form_step_data.1.avatar.tmp_filename }}/{{ LOGO_PREVIEW_SIZE }}/" alt="{{ object.get_title|escape }}"/></dd>
                    {% else %}
                        <dt>"""+(_("Profile photo")+"")+"""</dt><dd><img class="avatar" src="{{ STATIC_URL }}site/img/placeholder/institution.png" alt="{{ object.get_title|escape }}"/></dd>
                    {% endif %}
                """),
                "avatar",
            ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
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
        widget=forms.TimeInput(format = '%H:%M'),
    )
    mon_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    mon_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    mon_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    mon_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    tue_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    tue_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    tue_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    tue_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    tue_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    wed_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    wed_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    wed_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    wed_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    wed_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    thu_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    thu_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    thu_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    thu_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    thu_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    fri_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    fri_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    fri_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    fri_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    fri_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sat_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sat_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sat_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sat_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sat_is_closed = forms.BooleanField(
        label=_("Closed"),
        required=False,
        initial=False,
    )

    sun_open0 = forms.TimeField(
        label=_("opens"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sun_close0 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sun_open1 = forms.TimeField(
        label=_("opens again"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
    )
    sun_close1 = forms.TimeField(
        label=_("closes"),
        required=False,
        widget=forms.TimeInput(format = '%H:%M'),
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
                string_concat(_("Opening Time"), " - ",  _("Closing Time")),
                layout.MultiField(
                    _("Monday"),
                    layout.Field(
                        "mon_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_mon",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mon_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_mon",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mon_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed mon"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "mon_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "mon_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_mon"
                ),
                
                "show_breaks",
                layout.HTML("""{% load i18n %}
                    <dt></dt><dd><p><a id="apply_to_all_days" href="#">{% trans "Apply to all days" %}</a></p></dd>
                    <dd class="clearfix">&nbsp;</dd>
                """),
                
                layout.MultiField(
                    _("Tuesday"),
                    layout.Field(
                        "tue_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_tue",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "tue_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_tue",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "tue_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed tue"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "tue_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "tue_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_tue"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Wednesday"),
                    layout.Field(
                        "wed_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_wed",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "wed_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_wed",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "wed_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed wed"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "wed_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "wed_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_wed"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Thursday"),
                    layout.Field(
                        "thu_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_thu",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "thu_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_thu",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "thu_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed thu"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "thu_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "thu_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_thu"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Friday"),
                    layout.Field(
                        "fri_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_fri",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fri_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_fri",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fri_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed fri"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "fri_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fri_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_fri"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Saturday"),
                    layout.Field(
                        "sat_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_sat",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sat_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_sat",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sat_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed sat"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "sat_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sat_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_sat"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),
                
                layout.MultiField(
                    _("Sunday"),
                    layout.Field(
                        "sun_open0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_sun",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sun_close0",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3 closed_sun",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sun_is_closed",
                        wrapper_class="col-xs-12 col-sm-12 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html",
                        css_class = "closed sun"
                    ),
                    css_class = "show-labels"
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "sun_open1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "sun_close1",
                        wrapper_class="col-xs-6 col-sm-6 col-md-3 col-lg-3",
                        template = "ccb_form/multifield.html"
                    ),
                    css_class = "show-labels break closed_sun"
                ),
                
                layout.HTML("""<dd class="clearfix">&nbsp;</dd>"""),

                "exceptions_de",
                "exceptions_en",
                "is_appointment_based",
                
                css_class = "opening-hours"
            ),
            
            layout.Fieldset(
                _("Payment Options"),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_cash_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_card_visa_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_invoice_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_card_mastercard_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_on_delivery_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_card_americanexpress_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_ec_maestro_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_giropay_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                layout.MultiField(
                    ' ',
                    layout.Field(
                        "is_prepayment_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "is_paypal_ok",
                        wrapper_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        template = "ccb_form/multifield.html"
                    ),
                ),
                css_class = "no-label"
            ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
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
                        self._errors[week_day + '_open0'] = [_("Please enter a closing time.")]
                    elif close0 < open0:
                        self._errors[week_day + '_open0'] = [_("A closing time must not be before an opening time.")]
                if close0:
                    if not open0:
                        self._errors[week_day + '_open0'] = [_("Please enter an opening time.")]

                if show_breaks:
                    if open1:
                        if not close1:
                            self._errors[week_day + '_open1'] = [_("Please enter a closing time.")]
                        elif close1 < open1:
                            self._errors[week_day + '_open1'] = [
                                _("A closing time must not be before an opening time.")]
                    if close1:
                        if not open1:
                            self._errors[week_day + '_open1'] = [_("Please enter an opening time.")]

                    if open1 or close1:
                        if not open0 or not close0:
                            self._errors[week_day + '_open1'] = [_("When specifying breaks, you must enter all data.")]
                        else:
                            if open1 < close0:
                                self._errors[week_day + '_open1'] = [
                                    _("An opening time after break must not be before the closing time to break.")]

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
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        queryset=get_related_queryset(Institution, "categories"),
        required=True,
    )

    institution_types = ModelMultipleChoiceTreeField(
        label=_("Types"),
        queryset=get_related_queryset(Institution, "institution_types"),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(CategoriesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Categories"),
                layout.Field("categories", template="ccb_form/custom_widgets/checkboxselectmultipletree.html"),
                css_class="no-label",
            ),
            layout.Fieldset(
                _("Institution Types"),
                layout.Field("institution_types", template="ccb_form/custom_widgets/checkboxselectmultipletree.html"),
                css_class="no-label",
            ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
            )
        )
        
        

def submit_step(current_step, form_steps, form_step_data):
    return form_step_data


def save_data(form_steps, form_step_data):
    from ccb.apps.site_specific.models import ContextItem
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

    slug = get_unique_value(
        ContextItem.objects.filter(content_type__model__in=("person", "institution")),
        better_slugify(form_step_data[0].get('institution_name', '')).replace("-", "_"),
        field_name="slug",
        separator="_",
        ignore_case=True,
    )
    institution = Institution(
        title=form_step_data[0].get('institution_name', ''),
        title2=form_step_data[0].get('institution_name2', ''),
        slug=slug,
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
                institution,
                "%s_%s" % (d, f),
                form_step_data[2].get('%s_%s' % (d, f), None)
            )

    institution.exceptions_en = form_step_data[2].get('exceptions_en', '')
    institution.exceptions_de = form_step_data[2].get('exceptions_de', '')
    institution.is_appointment_based = form_step_data[2].get('is_appointment_based', False)

    # payment
    institution.is_card_visa_ok = form_step_data[2].get('is_card_visa_ok', None)
    institution.is_card_mastercard_ok = form_step_data[2].get('is_card_mastercard_ok', None)
    institution.is_card_americanexpress_ok = form_step_data[2].get('is_card_americanexpress_ok', None)
    institution.is_paypal_ok = form_step_data[2].get('is_paypal_ok', None)
    institution.is_cash_ok = form_step_data[2].get('is_cash_ok', None)
    institution.is_transaction_ok = form_step_data[2].get('is_transaction_ok', None)
    institution.is_prepayment_ok = form_step_data[2].get('is_prepayment_ok', None)
    institution.is_on_delivery_ok = form_step_data[2].get('is_on_delivery_ok', None)
    institution.is_invoice_ok = form_step_data[2].get('is_invoice_ok', None)
    institution.is_ec_maestro_ok = form_step_data[2].get('is_ec_maestro_ok', None)
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
    institution.categories.add(*cleaned['categories'])
    institution.institution_types.add(*cleaned['institution_types'])

    media_file = form_step_data[1].get('avatar', '')
    if media_file:
        tmp_path = os.path.join(settings.PATH_TMP, media_file['tmp_filename'])
        f = open(tmp_path, 'r')
        filename = tmp_path.rsplit("/", 1)[1]
        image_mods.FileManager.save_file_for_object(
            institution,
            filename,
            f.read(),
            subpath="avatar/"
        )
        f.close()

    # save again triggering signals
    # TODO: check what happens around institution saving: what signals are called and what notifications are created
    # minimize or rework long-lasting tasks
    institution.calculate_completeness()
    institution.save()

    # this is used for redirection to the institution details page
    form_steps['success_url'] = institution.get_url_path()
    return form_step_data


ADD_INSTITUTION_FORM_STEPS = {
    0: {
        'title': _("main data"),
        'template': "institutions/add_institution_main_data.html",
        'form': MainDataForm,
    },
    1: {
        'title': _("profile data"),
        'template': "institutions/add_institution_profile.html",
        'form': ProfileForm,
    },
    2: {
        'title': _("opening hours and payment"),
        'template': "institutions/add_institution_opening_hours.html",
        'form': OpeningHoursPaymentForm,
    },
    3: {
        'title': _("categories"),
        'template': "institutions/add_institution_categories.html",
        'form': CategoriesForm,
    },

    4: {
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


class InstitutionSearchForm(dynamicforms.Form):
    creative_sector = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Creative Sector"),
        required=False,
        queryset=get_related_queryset(Institution, "creative_sectors"),
    )
    context_category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Business Category"),
        required=False,
        queryset=get_related_queryset(Institution, "context_categories"),
    )
    institution_type = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Type"),
        required=False,
        queryset=get_related_queryset(Institution, "institution_types"),
    )
    locality_type = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Location Type"),
        required=False,
        queryset=LocalityType.objects.order_by("tree_id", "lft"),
    )

    def __init__(self, *args, **kwargs):
        super(InstitutionSearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("creative_sector", template = "ccb_form/custom_widgets/filter_field.html"),
                layout.Field("context_category", template = "ccb_form/custom_widgets/filter_field.html"),
                layout.Field("institution_type", template = "ccb_form/custom_widgets/filter_field.html"),
                layout.Field("locality_type", template="ccb_form/custom_widgets/locality_type_filter_field.html"),
                template = "ccb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )
