# -*- coding: UTF-8 -*-
import datetime
import os.path

from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.dates import MONTHS
from django.conf import settings
from django.db import models
from django.utils.encoding import force_unicode

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.forms.fields import AutocompleteField
from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

from jetson.apps.location.models import Address, LocalityType
from jetson.apps.optionset.models import PhoneType, EmailType, URLType
from jetson.apps.utils.forms import ModelMultipleChoiceTreeField

from ccb.apps.site_specific.models import ContextItem

from mptt.forms import TreeNodeChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

image_mods = models.get_app("image_mods")

app = models.get_app("events")
Event, EventType, EventTime, EventTimeLabel, URL_ID_EVENT, URL_ID_EVENTS = (
    app.Event, app.EventType, app.EventTime, app.EventTimeLabel, app.URL_ID_EVENT, app.URL_ID_EVENTS,
)

Institution = models.get_model("institutions", "Institution")

EVENT_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, "event_type"))
ORGANIZING_INSTITUTION_CHOICES = XChoiceList(get_related_queryset(Event, "organizing_institution"))
URL_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, "url0_type"))

YEARS_CHOICES = [("", _("Year"))] + [(i, i) for i in range(2008, 2040)]
MONTHS_CHOICES = [("", _("Month"))] + MONTHS.items()
DAYS_CHOICES = [("", _("Day"))] + [(i, i) for i in range(1, 32)]
HOURS_CHOICES = [("", _("HH"))] + [(i, u"%02d" % i) for i in range(0, 24)]
MINUTES_CHOICES = [("", _("MM"))] + [(i, u"%02d" % i) for i in range(0, 60, 5)]

WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

ORGANIZER_CHOICES = [
    (0, _("selected venue is an organizer")),
    (1, _("organized by other institution")),
    (2, _("organized by myself")),
]

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE


# Collect translatable strings
_("Not listed? Enter manually")
_("Address")
_("Change selection")
_("Back to selection")
_("Phone")
_("Fax")
_("URL")
_("Apply to all days")


class MainDataForm(dynamicforms.Form):
    """
    Form for event "main data"
    """
    title_de = forms.CharField(
        label=_("Title (German)"),
        required=True,
    )

    title_en = forms.CharField(
        label=_("Title (English)"),
        required=False,
    )

    event_type = forms.ChoiceField(
        required=True,
        choices=EVENT_TYPE_CHOICES,
        label=_("Event Type"),
    )

    # related_events = forms.ModelMultipleChoiceField(
    #    required=False,
    #   queryset=get_related_queryset(Event, "related_events").only("id", "title", "title_de", "title_en"),
    #    label=_("Related Events"),
    # )

    """
    venue:
    
    The parameters below are as follows:
    app:              the "app"
    qs_function:      the function to get the queryset, 
                      must be placed in ajax.py under <app> 
                      folder
    display_atrr:     a model field or function to get the 
                      required display title for the autocomplete
                      field
    add_display_atrr: a model field or function to get the 
                      required display descriptione for the 
                      autocomplete field
    """
    venue = AutocompleteField(
        required=True,
        label=_("Venue"),
        help_text=_("Please enter a letter to display a list of available venues"),
        app="events",
        qs_function="get_venues",
        display_attr="title",
        add_display_attr="get_address_string",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight": False,
        }
    )

    venue_title = forms.CharField(
        required=True,
        label=_("Name"),
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
    )
    postal_code = forms.CharField(
        required=True,
        label=_("Postal Code"),
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

    email0_address = forms.EmailField(
        required=False,
        label=_("E-mail"),
    )

    url0_link = forms.URLField(
        required=False,
        label=_("Website"),
    )

    organizer_ind = forms.ChoiceField(
        initial=0,
        choices=ORGANIZER_CHOICES,
        widget=forms.RadioSelect()
    )

    organizing_institution = AutocompleteField(
        required=True,
        label=_("Organizing institution"),
        help_text=_("Please enter a letter to display a list of available institutions"),
        app="events",
        qs_function="get_organizing_institutions",
        display_attr="title",
        add_display_attr="get_address_string",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight": False,
        }
    )

    organizer_title = forms.CharField(
        required=True,
        label=_("Name of Institution"),
    )

    organizer_url_link = forms.URLField(
        required=True,
        label=_("Website"),
    )

    def __init__(self, *args, **kwargs):
        # initial_related_events = kwargs.get(
        #    "initial",
        #    {},
        #    ).get(
        #        "related_events",
        #        (),
        #        )
        # if (
        #    initial_related_events and
        #    isinstance(initial_related_events, (list, tuple, QuerySet))
        #    ):
        #    if isinstance(initial_related_events[0], models.Model):
        #        kwargs['initial']['related_events'] = [
        #            force_unicode(obj.pk)
        #            for obj in initial_related_events
        #            ]
        super(MainDataForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Title"),
                "title_de",
                "title_en",
                "event_type",
            ),
            layout.Fieldset(
                _("Period"),
                layout.HTML("""{% load crispy_forms_tags i18n %}
                {{ formsets.event_times.management_form }}
                <div id="event_times">
                    {% for event_time_form in formsets.event_times.forms %}
                        <div class="event_time formset-form tabular-inline">
                            {% crispy event_time_form %}
                        </div>
                    {% endfor %}
                </div>
                <!-- used by javascript -->
                <div id="event_times_empty_form" class="event_time formset-form tabular-inline" style="display: none">
                    {% with formsets.event_times.empty_form as event_time_form %}
                        {% if event_time_form %}
                            {% crispy event_time_form %}
                        {% endif %}
                    {% endwith %}
                </div>
                """),
                css_id="event_times_fieldset",
            ),
            layout.Fieldset(
                _("Venue"),
                "venue",
                layout.HTML("""{% load i18n %}
                    <p>
                        <a id="id_venue_not_listed" href="#">{% trans "Not listed? Enter manually" %}</a>
                    </p>
                """),
                css_id="id_block_venue_select",
            ),
            layout.Fieldset(
                _("Venue"),
                # TODO: decide how to rework the markup for bootstrap
                layout.HTML("""{% load i18n %}
                    <ul class="def_list">
                        <li class="add_manually_list_label">
                            <label>
                                {% trans "Address" %}:
                            </label>
                        </li>
                        <li id="id_venue_address_title" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_venue_address_street_address" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_venue_address_street_address2" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_venue_address_postal_code" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_venue_address_city" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_venue_address_country" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li class="add_manually_list">
                            <a id="id_venue_change" href="#">
                                {% trans "Change selection" %}
                            </a>
                        </li>
                    </ul>
                """),
                css_id="id_block_venue_address_display",
            ),
            layout.Fieldset(
                _("Venue"),
                "venue_title",
                layout.HTML("""{% load i18n %}
                    <p>
                        <a id="id_venue_select" href="#">
                            {% trans "Back to selection" %}
                        </a>
                    </p>
                """),
                css_id="id_block_venue_name_input",
            ),
            layout.Fieldset(
                _("Address"),
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
                "latitude",  # hidden field
                "longitude",  # hidden field
            ),
            layout.Fieldset(
                _("Map"),
                layout.HTML("""{% include "bootstrap3/custom_widgets/editable_map.html" %}"""),
            ),
            layout.Fieldset(
                _("Information about this Event"),
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
                css_id="id_block_venue_contact_input",
            ),
            layout.Fieldset(
                _("Organizer"),
                "organizer_ind",
            ),
            layout.Fieldset(
                _("Organizing institution"),
                "organizing_institution",
                layout.HTML("""{% load i18n %}
                <p>
                    <a id="id_org_inst_not_listed" href="#">{% trans "Not listed? Enter manually" %}</a>
                </p>
                """),
                css_id="id_block_org_inst_select",
            ),
            layout.Fieldset(
                _("Organizer address"),
                layout.HTML("""{% load i18n %}
                    <ul class="address def_list">
                        <li class="add_manually_list_label">
                            <label>{% trans "Address" %}:</label>
                        </li>
                        <li id="id_org_inst_address_title" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_org_inst_address_street_address" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_org_inst_address_street_address2" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_org_inst_address_postal_code" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_org_inst_address_city" class="add_manually_list">
                            <strong></strong>
                        </li>
                        <li id="id_org_inst_address_country" class="add_manually_list">
                            <strong></strong>
                        </li>
                    </ul>
                    <ul class="def_list" id="id_org_inst_phone_container">
                        <li class="add_manually_list_label">
                            <label>
                                {% trans "Phone" %}:
                            </label>
                        </li>
                        <li id="id_org_inst_phone" class="add_manually_list">
                            <strong></strong>
                        </li>
                    </ul>
                    <ul class="def_list" id="id_org_inst_fax_container">
                        <li class="add_manually_list_label">
                            <label>
                                {% trans "Fax" %}:
                            </label>
                        </li>
                        <li id="id_org_inst_fax" class="add_manually_list">
                            <strong></strong>
                        </li>
                    </ul>
                    <ul class="def_list" id="id_org_inst_url0_link_container">
                        <li class="add_manually_list_label">
                            <label>
                                {% trans "URL" %}:
                            </label>
                        </li>
                        <li id="id_org_inst_url0_link" class="add_manually_list">
                            <strong></strong>
                        </li>
                    </ul>
                    <p>
                        <a id="id_org_inst_change" href="#">{% trans "Change selection" %}</a>
                    </p>
                """),
            ),
            layout.Fieldset(
                _("Organizing institution"),
                "organizer_title",
                "organizer_url_link",
                css_id="id_block_org_inst_data_input",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
            )
        )

    def clean(self):
        """"
        Below, there is some (simple and complex) validation logic:
        for example, some fields are not required, if a venue is selected.
        the "_errors" stuff there is a bit of a hack, but there seems 
        to be no other possibility to simulate the "required" attribute after
        field validation, because the fields clean method is called
        before and there is some "field required error" raised, which
        we have to eliminate manually. We set all the fields "required", even
        if you can enter alternative data. (You have this nice "*" attached
        to the label of the field indicating that you must fill in!
        (TODO Aidas, maybe you know something better!)
        """

        # if venue is selected, the venue_title etc need not to be filled in and vice versa!
        if self.cleaned_data.get('venue_title', None):
            del self._errors['venue']
        else:
            if self.cleaned_data.get('venue', None):
                for field_name in [
                    'venue_title',
                    'street_address',
                    'postal_code',
                    'city',
                    'country',
                ]:
                    if self._errors.get(field_name, False):
                        del self._errors[field_name]

        # organizing institution logic
        organizer_ind = int(self.cleaned_data['organizer_ind'])
        if organizer_ind == 1:
            if self.cleaned_data.get('organizer_title', "") != "":
                if self._errors.get('organizing_institution', False):
                    del self._errors['organizing_institution']
            else:
                if self.cleaned_data.get('organizing_institution', "") != "":
                    for field_name in [
                        'organizer_title',
                        'organizer_url_link',
                    ]:
                        if self._errors.get(field_name, False):
                            del self._errors[field_name]
        else:
            for field_name in [
                'organizing_institution',
                'organizer_title',
                'organizer_url_link',
            ]:
                if self._errors.get(field_name, False):
                    del self._errors[field_name]

        return self.cleaned_data


class EventTimeForm(dynamicforms.Form):
    """
    Form for event "main data"
    """

    label = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(EventTime, "label"),
    )

    start_yyyy = forms.ChoiceField(
        required=True,
        choices=YEARS_CHOICES,
        label=_("Start Year"),
    )

    start_mm = forms.ChoiceField(
        required=False,
        choices=MONTHS_CHOICES,
        label=_("Start Month"),
    )

    start_dd = forms.ChoiceField(
        required=False,
        choices=DAYS_CHOICES,
        label=_("Start Day"),
    )

    start_hh = forms.ChoiceField(
        required=False,
        choices=HOURS_CHOICES,
        label=_("Start Hours"),
    )

    start_ii = forms.ChoiceField(
        required=False,
        choices=MINUTES_CHOICES,
        label=_("Start Minutes"),
    )

    end_yyyy = forms.ChoiceField(
        required=False,
        choices=YEARS_CHOICES,
        label=_("End Year"),
    )

    end_mm = forms.ChoiceField(
        required=False,
        choices=MONTHS_CHOICES,
        label=_("End Month"),
    )

    end_dd = forms.ChoiceField(
        required=False,
        choices=DAYS_CHOICES,
        label=_("End Day"),
    )

    end_hh = forms.ChoiceField(
        required=False,
        choices=HOURS_CHOICES,
        label=_("End Hours"),
    )

    end_ii = forms.ChoiceField(
        required=False,
        choices=MINUTES_CHOICES,
        label=_("End Minutes"),
    )

    is_all_day = forms.BooleanField(
        required=False,
        label=_("All Day")
    )

    def __init__(self, *args, **kwargs):
        initial_label = kwargs.get("initial", {}).get("label", None)
        if initial_label and isinstance(initial_label, models.Model):
            kwargs['initial']['label'] = force_unicode(initial_label.pk)
        super(EventTimeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Div(
                "label",
                layout.Row(
                    layout.Div(
                        layout.HTML(_("Start")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_dd",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_mm",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_yyyy",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_hh",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "start_ii",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "is_all_day",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "has_end_date",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(_("End")),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_dd",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_mm",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_yyyy",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_hh",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        "end_ii",
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                    layout.Div(
                        layout.HTML("&nbsp;"),
                        css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3",
                    ),
                ),
            )
        )

    def clean(self):
        """"
        Below, there is some (simple and complex) validation logic:
        for example, some fields are not required, if a venue is seleceted.
        the "_errors" stuff there is a bit of a hack, but there seems 
        to be no other possibility to simulate the "required" attribute after
        field validation, because the fields clean method is called
        before and there is some "field required error" raised, which
        we have to eliminate manually. We set all the fields "required", even
        if you can enter alternatiave data. (You have this nice "*" attached
        to the label of the field indicating that you must fill in!
        (TODO Aidas, maybe you know something better!)
        """

        # start date must be valid!
        start_date = None
        end_date = None
        start_yyyy = self.cleaned_data.get('start_yyyy', None)
        start_mm = self.cleaned_data.get('start_mm', None)
        start_dd = self.cleaned_data.get('start_dd', None)

        # any error handling is overwritten!
        if self._errors.get('start_yyyy', False):
            del self._errors['start_yyyy']
        if self._errors.get('start_mm', False):
            del self._errors['start_mm']
        if self._errors.get('start_dd', False):
            del self._errors['start_dd']

        if start_dd:
            if not start_mm:
                self._errors['start_dd'] = [_("Please enter a valid month.")]
        try:
            start_date = datetime.date(int(start_yyyy), int(start_mm or 1), int(start_dd or 1))
        except Exception:
            self._errors['start_dd'] = [_("Please enter a valid date.")]

        # start time or "all day must be entered"
        if 'start_hh' in self._errors or 'start_ii' in self._errors:
            self._errors['start_dd'] = [_("Please enter a valid time using format 'HH:MM' or choose 'All Day'")]
            if self.cleaned_data.get('is_all_day', False):
                del self._errors['start_hh']
                del self._errors['start_ii']

        if self.cleaned_data.get('start_hh', None) and not self.cleaned_data.get('start_ii', None):
            self.cleaned_data['start_ii'] = '0'

        if self.cleaned_data.get('end_hh', None) and not self.cleaned_data.get('end_ii', None):
            self.cleaned_data['end_ii'] = '0'



        # if start time is specified, day, month and year must be specified
        if self.cleaned_data.get('start_hh', None):
            if not (start_yyyy and start_mm and start_dd):
                self._errors['start_hh'] = [_("If you choose a time, please enter a valid day, month and year.")]

        # if end date is specified, all fields must be specified!
        end_yyyy = self.cleaned_data.get('end_yyyy', None)
        end_mm = self.cleaned_data.get('end_mm', None)
        end_dd = self.cleaned_data.get('end_dd', None)

        if self._errors.get('end_yyyy', False):
            del self._errors['end_yyyy']
        if self._errors.get('end_mm', False):
            del self._errors['end_mm']
        if self._errors.get('end_dd', False):
            del self._errors['end_dd']

        if end_yyyy or end_mm or end_dd:
            if end_dd:
                if not end_mm:
                    self._errors['end_dd'] = [_("Please enter a valid month.")]
            try:
                end_date = datetime.date(int(end_yyyy), int(end_mm or 1), int(end_dd or 1))
            except Exception:
                self._errors['end_dd'] = [_("If you want to specify an end date, please enter a valid one.")]

        if end_date and start_date:
            if start_date > end_date:
                self._errors['end_dd'] = [_("End date must be after start date.")]

        # if end time is specified, day, month and year must be specified
        if self.cleaned_data.get('end_hh', None):
            if not (end_yyyy and end_mm and end_dd):
                self._errors['end_hh'] = [_("If you choose a time, please enter a valid day, month and year.")]

        return self.cleaned_data


class ProfileForm(dynamicforms.Form):
    """
    Form for event profile
    """
    description_en = forms.CharField(
        label=_("Description (English)"),
        required=False,
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
    )
    description_de = forms.CharField(
        label=_("Description (German)"),
        required=False,
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
    )

    image = ImageField(
        label=_("Profile photo"),
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
                    {% if form_step_data.step_event_profile.image %}
                        <img src="/helper/tmpimage/{{ form_step_data.step_event_profile.image.tmp_filename }}/{{ LOGO_PREVIEW_SIZE }}/" alt="{{ object.get_title|escape }}"/>
                    {% else %}
                        <img src="{{ DEFAULT_FORM_LOGO_4_EVENT }}" alt="{{ object.get_title|escape }}"/>
                    {% endif %}
                """),
                "image",
            ),
            bootstrap.FormActions(
                layout.Submit('reset', _('Reset')),
                layout.HTML("""{% include "bootstrap3/custom_widgets/previous_button.html" %}"""),
                layout.Submit('submit', _('Next')),
            )
        )


class FeesForm(dynamicforms.Form):
    """
    Form for event fees and opening ours
    """

    fees_en = forms.CharField(
        label=_('Fees (English)'),
        required=False,
        widget=forms.Textarea,
    )
    fees_de = forms.CharField(
        label=_('Fees (German)'),
        required=False,
        widget=forms.Textarea,
    )

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

    def __init__(self, *args, **kwargs):
        super(FeesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Fees"),
                "fees_de",
                "fees_en",
            ),
            layout.Fieldset(
                string_concat(_("Opening Time"), " - ",  _("Closing Time")),
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
                        layout.HTML("""{% load i18n %}
                            <p>
                                <a id="id_apply_all_days" href="#">{% trans "Apply to all days" %}</a>
                            </p>
                        """),
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
            bootstrap.FormActions(
                layout.Submit('reset', _('Reset')),
                layout.HTML("""{% include "bootstrap3/custom_widgets/previous_button.html" %}"""),
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
                        self._errors[week_day + '_open0'] = [_("Please enter a closing time.")]
                    elif close0 < open0:
                        self._errors[week_day + '_open0'] = [
                            _("A closing time must not be before an opening time.")]
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
                            self._errors[week_day + '_open1'] = [
                                _("When specifying breaks, you must enter all data.")]
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
        queryset=get_related_queryset(Event, "categories"),
        required=True,
    )

    tags = TagField(
        label=_("Tags"),
        help_text=_("Separate tags with commas."),
        max_length=200,
        required=False,
        widget=TagAutocomplete,
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
                layout.Div(layout.Field("categories", template="ccb_form/custom_widgets/checkboxselectmultipletree.html")),
            ),
            layout.Fieldset(
                _("Tags"),
                "tags",
            ),
            bootstrap.FormActions(
                layout.Submit('reset', _('Reset')),
                layout.HTML("""{% include "bootstrap3/custom_widgets/previous_button.html" %}"""),
                layout.Submit('submit', _('Next')),
            )
        )


def submit_step(current_step, form_steps, form_step_data):
    return form_step_data


def save_data(form_steps, form_step_data):
    step_main_data = form_step_data['step_main_data']
    step_event_profile = form_step_data['step_event_profile']
    step_fees_opening_hours = form_step_data['step_fees_opening_hours']
    step_categories = form_step_data['step_categories']
    step_confirm_data = form_step_data['step_confirm_data']
    user = get_current_user()

    # venue data
    venue = None
    if step_main_data.get('venue', None):
        venue = Institution.objects.get(pk=step_main_data['venue'])
        venue_title = venue.get_title()
    else:
        venue_title = step_main_data.get('venue_title', None)

        venue = Institution(
            title=venue_title,
            slug=get_unique_value(Institution, better_slugify(venue_title).replace("-", "_"), separator="_"),
        )
        venue.status = "event_location"
        venue.save()
        institutional_contact = venue.institutionalcontact_set.create(
            is_primary=True,
            is_temporary=False,
            phone0_type=PhoneType.objects.get(slug='phone'),
            phone0_country=step_main_data.get('phone_country', ''),
            phone0_area=step_main_data.get('phone_area', ''),
            phone0_number=step_main_data.get('phone_number', ''),
            phone1_type=PhoneType.objects.get(slug='fax'),
            phone1_country=step_main_data.get('fax_country', ''),
            phone1_area=step_main_data.get('fax_area', ''),
            phone1_number=step_main_data.get('fax_number', ''),
            url0_type_id=step_main_data.get('url0_type', None),
            url0_link=step_main_data.get('url0_link', ''),
        )
        Address.objects.set_for(
            institutional_contact,
            "postal_address",
            country=step_main_data.get('country', None),
            city=step_main_data.get('city', None),
            street_address=step_main_data.get('street_address', None),
            street_address2=step_main_data.get('street_address2', None),
            postal_code=step_main_data.get('postal_code', None),
            latitude=step_main_data.get('latitude', None),
            longitude=step_main_data.get('longitude', None),
        )
        '''
        if hasattr(venue, "create_default_group"):
            person_group = venue.create_default_group()
            person_group.content_object = venue
            person_group.save()
            membership = person_group.groupmembership_set.create(
                user = user,
                role = "owners",
                inviter = user,
                confirmer = user,
                is_accepted = True,
                )
        '''

    # organizing institution
    organizing_institution = None
    organizing_person = None
    organizer_title = None
    organizer_url_link = None
    organizer_ind = int(step_main_data.get('organizer_ind', 0))
    # venue is organizer
    if organizer_ind == 0:
        if venue:
            organizing_institution = venue
        """
        TODO As Reinhard decided, that we do not create any institutions
        implicitly, so, if no venue is selcted (but only a venue title with
        poatal_address is entered, no institution is created).
        """
        # I am the organizer!
    elif organizer_ind == 2:
        organizing_person = get_current_user().profile
    # orgnaizer is selected separately    
    else:
        if step_main_data.get('organizing_institution', None):
            organizing_institution = Institution.objects.get(
                pk=step_main_data['organizing_institution'],
            )
        else:
            organizer_title = step_main_data.get('organizer_title', None)
            organizer_url_link = step_main_data.get('organizer_url_link', None)

    event = Event()

    event.title_en = step_main_data.get('title_en', None)
    event.title_de = step_main_data.get('title_de', None)
    if not event.title_en:
        event.title_en = event.title_de

    event.description_en = step_event_profile.get('description_en', None)
    event.description_de = step_event_profile.get('description_de', None)

    event.event_type = EventType.objects.get(
        pk=step_main_data.get('event_type', None),
    )

    event.venue_title = venue_title
    event.venue = venue
    event.organizing_institution = organizing_institution
    event.organizing_person = organizing_person
    event.organizer_title = organizer_title
    event.organizer_url_link = organizer_url_link

    event.additional_info_en = ""  # TODO we do not have that in the mockups
    event.additional_info_de = ""  # TODO we do not have that in the mockups

    event.fees_en = step_fees_opening_hours.get('fees_en', '')
    event.fees_de = step_fees_opening_hours.get('fees_de', '')

    event.is_registration_required = False  # TODO we do not have that in the mockups

    event.phone0_type = PhoneType.objects.get(slug='phone')
    event.phone0_country = step_main_data.get('phone_country', '')
    event.phone0_area = step_main_data.get('phone_area', '')
    event.phone0_number = step_main_data.get('phone_number', '')

    event.phone1_type = PhoneType.objects.get(slug='fax')
    event.phone1_country = step_main_data.get('fax_country', '')
    event.phone1_area = step_main_data.get('fax_area', '')
    event.phone1_number = step_main_data.get('fax_number', '')

    event.email0_type = EmailType.objects.get(slug='email')
    event.email0_address = step_main_data.get('email0_address', '')

    event.url0_type = URLType.objects.get(slug='web')
    event.url0_link = step_main_data.get('url0_link', '')

    for f in ("open", "break_close", "break_open", "close"):
        for d in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
            setattr(
                event,
                "%s_%s" % (d, f),
                step_fees_opening_hours.get('%s_%s' % (d, f), None)
            )

    event.exceptions_en = step_fees_opening_hours.get('exceptions_en', '')
    event.exceptions_de = step_fees_opening_hours.get('exceptions_de', '')
    event.is_appointment_based = step_fees_opening_hours.get('is_appointment_based', False)

    event.tags = step_categories.get('tags', '')

    # TODO should we really publish the event immediately?
    event.status = "published"

    event.save()

    if venue and venue.get_contacts():
        Address.objects.set_for(
            event,
            "postal_address",
            **venue.get_contacts()[0].postal_address.get_dict()
        )
    else:
        Address.objects.set_for(
            event,
            "postal_address",
            country=step_main_data.get('country', None),
            city=step_main_data.get('city', None),
            street_address=step_main_data.get('street_address', None),
            street_address2=step_main_data.get('street_address2', None),
            postal_code=step_main_data.get('postal_code', None),
            latitude=step_main_data.get('latitude', None),
            longitude=step_main_data.get('longitude', None),
        )

    # creative sectors and context categories
    cleaned = step_categories
    event.categories.add(*cleaned['categories'])

    media_file = step_event_profile.get('image', '')
    if media_file:
        tmp_path = os.path.join(settings.PATH_TMP, media_file['tmp_filename'])
        f = open(tmp_path, 'r')
        filename = tmp_path.rsplit("/", 1)[1]
        image_mods.FileManager.save_file_for_object(
            event,
            filename,
            f.read(),
            subpath="avatar/"
        )
        f.close()

    # save again without triggering any signals
    event.save_base(raw=True)

    # for ev in step_main_data.get('related_events', ()):
    #    event.related_events.add(ev)

    for time_data in step_main_data['sets'].get("event_times", ()):
        time = EventTime(event=event)
        label_id = time_data.get('label', None)
        if label_id:
            time.label = EventTimeLabel.objects.get(pk=label_id)

        time.start_yyyy = time_data.get('start_yyyy', None)
        time.start_mm = time_data.get('start_mm', None)
        time.start_dd = time_data.get('start_dd', None)
        time.start_hh = time_data.get('start_hh', None)
        if time.start_hh:
            start_ii_default = 0
        else:
            start_ii_default = None
        time.start_ii = time_data.get('start_ii', start_ii_default)

        time.end_yyyy = time_data.get('end_yyyy', None)
        time.end_mm = time_data.get('end_mm', None)
        time.end_dd = time_data.get('end_dd', None)
        time.end_hh = time_data.get('end_hh', None)
        if time.end_hh:
            end_ii_default = 0
        else:
            end_ii_default = None
        time.end_ii = time_data.get('end_ii', end_ii_default)
        time.is_all_day = time_data.get('is_all_day', False)

        time.save()

    form_steps['success_url'] = event.get_url_path()

    return form_step_data


ADD_EVENT_FORM_STEPS = {
    'step_main_data': {
        'title': _("main data"),
        'template': "events/add_event_main_data.html",
        'form': MainDataForm,
        'formsets': {
            'event_times': formset_factory(
                EventTimeForm,
                can_delete=True,
            ),
        },
    },
    'step_event_profile': {
        'title': _("event profile"),
        'template': "events/add_event_profile.html",
        'form': ProfileForm,
    },
    'step_fees_opening_hours': {
        'title': _("fees and opening hours"),
        'template': "events/add_event_fees.html",
        'form': FeesForm,
    },
    'step_categories': {
        'title': _("categories"),
        'template': "events/add_event_categories.html",
        'form': CategoriesForm,
    },
    'step_confirm_data': {
        'title': _("confirm data"),
        'template': "events/add_event_confirm.html",
        'form': forms.Form,  # dummy form
    },
    'onsubmit': submit_step,
    'onsave': save_data,
    'name': 'add_event',
    'success_url': "/%s/" % URL_ID_EVENTS,
    'default_path': [
        'step_main_data',
        'step_event_profile',
        'step_fees_opening_hours',
        'step_categories',
        'step_confirm_data',
    ],
}


class EventSearchForm(dynamicforms.Form):
    category = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Category"),
        required=False,
        queryset=get_related_queryset(ContextItem, "categories"),
    )
    event_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Event Type"),
        required=False,
        queryset=get_related_queryset(Event, "event_type"),
    )
    locality_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Location Type"),
        required=False,
        queryset=LocalityType.objects.order_by("tree_id", "lft"),
    )
    keywords = forms.CharField(
        label=_("Keyword(s)"),
        required=False,
    )
    is_featured = forms.BooleanField(
        label=_("Featured events only"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(EventSearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "object_list_filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                "category",
                "event_type",
                "locality_type",
                "keywords",
                "is_featured",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )

    def get_query(self):
        from django.template.defaultfilters import urlencode
        if self.is_valid():
            cleaned = self.cleaned_data
            return "&".join([
                ("%s=%s" % (k, urlencode(isinstance(v, models.Model) and v.pk or v)))
                for (k, v) in cleaned.items()
                if v
            ])
        return ""
