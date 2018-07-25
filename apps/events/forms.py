# -*- coding: UTF-8 -*-
import datetime
import os.path

from django.db import models
from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Context
from django.utils.dates import MONTHS
from django.conf import settings
from django.db import models
from django.utils.encoding import smart_unicode, force_unicode
from django.db.models.query import QuerySet

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.forms.fields import AutocompleteField
from base_libs.forms.fields import HierarchicalModelChoiceField
from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.utils.misc import get_translation

image_mods = models.get_app("image_mods")

from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

from jetson.apps.location.models import Address, LocalityType
from jetson.apps.optionset.models import PhoneType, EmailType, URLType
from jetson.apps.utils.forms import ModelChoiceTreeField

from mptt.forms import TreeNodeChoiceField

app = models.get_app("events")
Event, EventTime, URL_ID_EVENT, URL_ID_EVENTS = (
    app.Event, app.EventTime, app.URL_ID_EVENT, app.URL_ID_EVENTS,
    )
EventType = app.EventType

Institution = models.get_model("institutions", "Institution")

EVENT_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, "event_type"))
ORGANIZING_INSTITUTION_CHOICES = XChoiceList(get_related_queryset(Event, "organizing_institution"))
URL_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, "url0_type"))

YEARS_CHOICES = [("", _("Year"))] + [(i, i) for i in range(2008, 2040)]
MONTHS_CHOICES = [("", _("Month"))] + MONTHS.items()
DAYS_CHOICES = [("", _("Day"))] + [(i, i) for i in range(1, 32)]
HOURS_CHOICES = [("", _("HH"))] + [(i, "%02d" % i) for i in range(0, 24)]
MINUTES_CHOICES = [("", _("MM"))] + [(i, "%02d" % i) for i in range(0, 60, 5)]

WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

ORGANIZER_CHOICES = [
    (0, _("selected venue is an organizer")),
    (1, _("organized by other institution")),
    (2, _("organized by myself")),
]

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE

class EventForm: # namespace
    
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
    
        related_events = forms.ModelMultipleChoiceField(
            label=_("Related Events"),
            required=False,
            queryset=get_related_queryset(Event, "related_events"),
        )
        
        if Institution:
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
                    "highlight" : False,
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
                "highlight" : False,
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
            initial_related_events = kwargs.get(
                "initial",
                {},
                ).get(
                    "related_events",
                    (),
                    )
            if (
                initial_related_events and
                isinstance(initial_related_events, (list, tuple, QuerySet))
                ):
                if isinstance(initial_related_events[0], models.Model):
                    kwargs['initial']['related_events'] = [
                        force_unicode(obj.pk)
                        for obj in initial_related_events
                        ]
            dynamicforms.Form.__init__(self, *args, **kwargs)
        
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
                           'country'
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
                               'organizer_url_link' 
                        ]:
                            if self._errors.get(field_name, False):
                                del self._errors[field_name]
            else: 
                for field_name in [
                       'organizing_institution',                                   
                       'organizer_title', 
                       'organizer_url_link' 
                ]:
                    if self._errors.get(field_name, False):
                        del self._errors[field_name]

            return self.cleaned_data
        
        def is_valid(self):
            is_valid = super(EventForm.MainDataForm, self).is_valid()
            errors = self._errors
            return is_valid
            
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
            dynamicforms.Form.__init__(self, *args, **kwargs)
            
        def clean(self):
            """"
            Below, there is some (simple and complex) validation logic:
            for example, some fields are not required, if a venue is seleceted.
            the "_errors" stuff there is a bit of a hack, but there seems 
            to be no other possibility to simulate the "required" attribute after
            field validation, because the fields clean method is called
            before and there is some "field required error" raised, which
            we have to eliminate manually. We set all the fields "required", even
            if you can enter alternative data. (You have this nice "*" attached
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
            except:
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
                except:
                    self._errors['end_dd'] = [_("If you want to specify an end date, please enter a valid one.")]

            if end_date and start_date:
                if start_date > end_date:
                    self._errors['end_dd'] = [_("End date must be after start date.")]
                    
            # if end time is specified, day, month and year must be specified
            if self.cleaned_data.get('end_hh', None):
                if not (end_yyyy and end_mm and end_dd):
                    self._errors['end_hh'] = [_("If you choose a time, please enter a valid day, month and year.")]
                    
            return self.cleaned_data
        
        def is_valid(self):
            is_valid = super(EventForm.EventTimeForm, self).is_valid()
            errors = self._errors
            return is_valid

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
        
        mon_open0 = forms.TimeField(required=False)
        mon_close0 = forms.TimeField(required=False)
        mon_open1 = forms.TimeField(required=False)
        mon_close1 = forms.TimeField(required=False)
        mon_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
    
        tue_open0 = forms.TimeField(required=False)
        tue_close0 = forms.TimeField(required=False)
        tue_open1 = forms.TimeField(required=False)
        tue_close1 = forms.TimeField(required=False)
        tue_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
    
        wed_open0 = forms.TimeField(required=False)
        wed_close0 = forms.TimeField(required=False)
        wed_open1 = forms.TimeField(required=False)
        wed_close1 = forms.TimeField(required=False)
        wed_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        thu_open0 = forms.TimeField(required=False)
        thu_close0 = forms.TimeField(required=False)
        thu_open1 = forms.TimeField(required=False)
        thu_close1 = forms.TimeField(required=False)
        thu_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        fri_open0 = forms.TimeField(required=False)
        fri_close0 = forms.TimeField(required=False)
        fri_open1 = forms.TimeField(required=False)
        fri_close1 = forms.TimeField(required=False)
        fri_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        sat_open0 = forms.TimeField(required=False)
        sat_close0 = forms.TimeField(required=False)
        sat_open1 = forms.TimeField(required=False)
        sat_close1 = forms.TimeField(required=False)
        sat_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        sun_open0 = forms.TimeField(required=False)
        sun_close0 = forms.TimeField(required=False)
        sun_open1 = forms.TimeField(required=False)
        sun_close1 = forms.TimeField(required=False)
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
                                self._errors[week_day + '_open1'] = [_("A closing time must not be before an opening time.")]
                        if close1:
                            if not open1:
                                self._errors[week_day + '_open1'] = [_("Please enter an opening time.")]
                        
                        if open1 or close1:
                            if not open0 or not close0:
                                self._errors[week_day + '_open1']  = [_("When specifying breaks, you must enter all data.")]
                            else:
                                if open1 < close0:
                                    self._errors[week_day + '_open1']  = [_("An opening time after break must not be before the closing time to break.")]
                        
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
    
    class ProfileForm(dynamicforms.Form):
        """
        Form for event profile
        """
        description_en = forms.CharField(
            label=_("Description (English)"),
            required=False,
            widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
            )
        description_de = forms.CharField(
            label= _("Description (German)"),
            required=False,
            widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
            )
        
        image = ImageField(
            label= _("Profile photo"),
            help_text= _("You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px.") % STR_LOGO_SIZE,
            required=False,
            min_dimensions=LOGO_SIZE,
            )
        
    class CategoriesForm(dynamicforms.Form):
        
        tags = TagField(
            label= _("Tags"),
            help_text=_("Separate tags with commas"),
            max_length=200,
            required=False,
            widget=TagAutocomplete,
            )

    @staticmethod
    def submit_step(current_step, form_steps, form_step_data):
        return form_step_data

    @staticmethod
    def save_data(form_steps, form_step_data):
        step_main_data = form_step_data['step_main_data']
        step_event_profile = form_step_data['step_event_profile']
        step_fees_opening_hours = form_step_data['step_fees_opening_hours']
        step_categories = form_step_data['step_categories']
        step_confirm_data = form_step_data['step_confirm_data']
        
        # venue data
        venue = None
        if step_main_data.get('venue', None):
            venue = Institution.objects.get(pk=step_main_data['venue'])
            venue_title = venue.get_title()
        else:
            venue_title = step_main_data.get('venue_title', None)
        
        #organizing institution
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
        
        event.title_en=step_main_data.get('title_en', None)
        event.title_de=step_main_data.get('title_de', None)
        if not event.title_en:
            event.title_en = event.title_de
            
        event.description_en=step_event_profile.get('description_en', None)
        event.description_de=step_event_profile.get('description_de', None)
        
        event.event_type = EventType.objects.get(
            pk=step_main_data.get('event_type', None),
            )
        
        event.venue_title=venue_title
        event.venue=venue
        event.organizing_institution=organizing_institution
        event.organizing_person=organizing_person
        event.organizer_title = organizer_title
        event.organizer_url_link = organizer_url_link
        
        event.additional_info_en="" # TODO we do not have that in the mockups 
        event.additional_info_de="" # TODO we do not have that in the mockups

        event.fees_en = step_fees_opening_hours.get('fees_en', '')
        event.fees_de = step_fees_opening_hours.get('fees_de', '')

        event.is_registration_required=False # TODO we do not have that in the mockups
                            
        event.phone0_type=PhoneType.objects.get(slug='phone')
        event.phone0_country=step_main_data.get('phone_country', '')
        event.phone0_area=step_main_data.get('phone_area', '')
        event.phone0_number=step_main_data.get('phone_number', '')
        
        event.phone1_type=PhoneType.objects.get(slug='fax')
        event.phone1_country=step_main_data.get('fax_country', '')
        event.phone1_area=step_main_data.get('fax_area', '')
        event.phone1_number=step_main_data.get('fax_number', '')
        
        event.email0_type=EmailType.objects.get(slug='email')
        event.email0_address=step_main_data.get('email0_address', '')
        
        event.url0_type=URLType.objects.get(slug='web')
        event.url0_link=step_main_data.get('url0_link', '')
        
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
        event.status="published"

        event.save()

        if venue:
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
                )

        # context categories
        cleaned = step_categories
        
        media_file = step_event_profile.get('image', '')
        if media_file:
            tmp_path = os.path.join(settings.PATH_TMP, media_file['tmp_filename'])
            f = open(tmp_path, 'r')
            filename = tmp_path.rsplit("/", 1)[1]
            image_mods.FileManager.save_file_for_object(
                event,
                filename,
                f.read(),
                subpath = "avatar/"
                )
            f.close()

        # save again without triggering any signals
        event.save_base(raw=True)
        
        for ev in step_main_data.get('related_events', ()):
            event.related_events.add(ev)
        
        for time_data in step_main_data['sets'].get("event_times", ()):
            time = EventTime(event=event)
            time.label=time_data.get('label', None)
            
            time.start_yyyy=time_data.get('start_yyyy', None) 
            time.start_mm=time_data.get('start_mm', None) 
            time.start_dd=time_data.get('start_dd', None)
            time.start_hh=time_data.get('start_hh', None)
            time.start_ii=time_data.get('start_ii', None)
            
            time.end_yyyy=time_data.get('end_yyyy', None) 
            time.end_mm=time_data.get('end_mm', None) 
            time.end_dd=time_data.get('end_dd', None)
            time.end_hh=time_data.get('end_hh', None)
            time.end_ii=time_data.get('end_ii', None)
            time.is_all_day=time_data.get('is_all_day', False)
            
            time.save()
        
        form_steps['success_url'] = event.get_url()
        
        return form_step_data

ADD_EVENT_FORM_STEPS = {
    'step_main_data': {
        'title': _("main data"),
        'template': "events/add_event_main_data.html",
        'form': EventForm.MainDataForm,
        'formsets': {
            'event_times': formset_factory(
                EventForm.EventTimeForm,
                can_delete=True,
                extra=1,
                ),
            },
    },
    'step_event_profile': {
        'title': _("event profile"),
        'template': "events/add_event_profile.html",
        'form': EventForm.ProfileForm,
    },
    'step_fees_opening_hours': {
        'title': _("fees and opening hours"),
        'template': "events/add_event_fees.html",
        'form': EventForm.FeesForm,
    },
    'step_categories': {
        'title': _("categories"),
        'template': "events/add_event_categories.html",
        'form': EventForm.CategoriesForm,
    },
    'step_confirm_data': {
        'title': _("confirm data"),
        'template': "events/add_event_confirm.html",
        'form': forms.Form, # dummy form
    },
    'onsubmit': EventForm.submit_step,
    'onsave': EventForm.save_data,
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
    event_type = forms.ModelChoiceField(
        empty_label=_("All"),
        label=_("Event Type"),
        required=False,
        queryset=get_related_queryset(Event, "event_type"),
        )
    locality_type = ModelChoiceTreeField(
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
