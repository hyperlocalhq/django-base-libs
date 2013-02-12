# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.models import ModelForm
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms.fields import AutocompleteModelChoiceField
from base_libs.models.settings import MARKUP_HTML_WYSIWYG, MARKUP_PLAIN_TEXT
from base_libs.middleware import get_current_user

Event = models.get_model("events", "Event")
EventTime = models.get_model("events", "EventTime")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from museumsportal.utils.forms import SecondarySubmit
from museumsportal.utils.forms import InlineFormSet
from museumsportal.utils.forms import SplitDateTimeWidget

class BasicInfoForm(ModelForm):
    museum = AutocompleteModelChoiceField(
        required=False,
        label=_("Museum"),
        help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
        app="museums",
        qs_function="get_published_museums",
        display_attr="title",
        add_display_attr="get_address",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight" : False,
            "multipleSeparator": ",,, ",
            },
        )
    organizing_museum = AutocompleteModelChoiceField(
        required=False,
        label=_("Organizing museum"),
        help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
        app="museums",
        qs_function="get_published_museums",
        display_attr="title",
        add_display_attr="get_address",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight" : False,
            "multipleSeparator": ",,, ",
            },
        )
    exhibition = AutocompleteModelChoiceField(
        required=False,
        label=_("Related exhibition"),
        help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
        app="exhibitions",
        qs_function="get_published_exhibitions",
        display_attr="title",
        add_display_attr="get_museum",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight" : False,
            "multipleSeparator": ",,, ",
            },
        )
    class Meta:
        model = Event
        
        fields = ['categories', 'tags', 'languages', 'other_languages',
            'museum', 'location_name', 'street_address', 'street_address2', 'postal_code',
            'district', 'city', 'latitude', 'longitude', 'exhibition',
            'organizing_museum', 'organizer_title', 'organizer_url_link',
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        self.fields['tags'].label = _("Tags separated by comma")
        self.fields['tags'].help_text = ""
        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].help_text = ""
        self.fields['categories'].empty_label = None
        self.fields['languages'].widget = forms.CheckboxSelectMultiple()
        self.fields['languages'].help_text = ""
        self.fields['languages'].empty_label = None

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Basic Info"),
            layout.Row(
                css_class="div-title",
                *('title_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-subtitle",
                *('subtitle_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-description",
                *(layout.Field('description_%s' % lang_code, css_class="tinymce") for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-basic-info",
                ))

        layout_blocks.append(layout.Fieldset(
            _("Where?"),
            layout.Row(
                layout.Div(
                    "museum",
                    "location_name",
                    "street_address",
                    "street_address2",
                    "postal_code",
                    "district",
                    "city",
                    ),
                layout.HTML("""{% load i18n %}
                    <div id="dyn_set_map">
                        <div id="gmap_wrapper">
                            <!-- THE GMAPS WILL BE INSERTED HERE DYNAMICALLY -->
                        </div>
                        <div class="form-actions">
                            <input id="dyn_locate_geo" type="button" class="btn" value="{% trans "Relocate on map" %}" />&zwnj;
                            <input id="dyn_remove_geo" type="button" class="btn" value="{% trans "Remove from map" %}"/>&zwnj;
                        </div>
                    </div>
                """),
                "latitude",
                "longitude",
                ),
            css_class="fieldset-where",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Organizer"),
            layout.Row(
                "organizing_museum",
                "exhibition",
                ),
            layout.Row(
                "organizer_title",
                "organizer_url_link",
                ),
            css_class="fieldset-organizer",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),
            "languages",
            "other_languages",
            "categories",
            "tags",
            css_class="fieldset-categories-tags",
            ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Reset')),
                ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )

class PricesForm(ModelForm):
    class Meta:
        model = Event
        fields = ['admission_price', 'reduced_price']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'meeting_place_%s' % lang_code,
                'booking_info_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(PricesForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'admission_price_info_%s' % lang_code,
                'meeting_place_%s' % lang_code,
                'booking_info_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Prices"),
            layout.Row('admission_price', 'reduced_price'),
            css_class="fieldset-prices",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Details"),
            layout.Row(
                css_class="div-admission_price_info-details",
                *('admission_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-meeting_place-details",
                *('meeting_place_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-booking_info-details",
                *('booking_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-details",
                ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Reset')),
                ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        

class TimesForm(ModelForm):
    class Meta:
        model = Event
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(TimesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Reset')),
                ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        

class EventTimeForm(ModelForm):
    class Meta:
        model = EventTime
        
    def __init__(self, *args, **kwargs):
        super(EventTimeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        layout_blocks.append(
            layout.Row(
                layout.Field("event_date", placeholder="yyyy-mm-dd"),
                layout.Field("start", placeholder="0:00"),
                layout.Field("end", placeholder="0:00"),
                ),
            )

        self.helper.layout = layout.Layout(
            *layout_blocks
            )

EventTimeFormset = inlineformset_factory(Event, EventTime, form=EventTimeForm, formset=InlineFormSet, extra=0)

class GalleryForm(ModelForm):
    class Meta:
        model = Event
        fields = []
        
    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
                layout.Submit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Reset')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
                SecondarySubmit('reset', _('Reset')),
                ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )


def load_data(instance=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True},
            'times': {'_filled': True, 'sets': {'event_times': [],}},
            'prices': {'_filled': True},
            'gallery': {'_filled': True},
            '_pk': instance.pk,
            }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
        form_step_data['basic']['categories'] = instance.categories.all()
        form_step_data['basic']['tags'] = instance.tags
        form_step_data['basic']['languages'] = instance.languages.all()
        form_step_data['basic']['other_languages'] = instance.other_languages
        form_step_data['basic']['museum'] = instance.museum
        form_step_data['basic']['location_name'] = instance.location_name
        form_step_data['basic']['street_address'] = instance.street_address
        form_step_data['basic']['street_address2'] = instance.street_address2
        form_step_data['basic']['postal_code'] = instance.postal_code
        form_step_data['basic']['district'] = instance.district
        form_step_data['basic']['city'] = instance.city
        form_step_data['basic']['latitude'] = instance.latitude
        form_step_data['basic']['longitude'] = instance.longitude
        form_step_data['basic']['exhibition'] = instance.exhibition
        form_step_data['basic']['organizing_museum'] = instance.organizing_museum
        form_step_data['basic']['organizer_title'] = instance.organizer_title
        form_step_data['basic']['organizer_url_link'] = instance.organizer_url_link
    
        for event_time in instance.eventtime_set.all():
            event_time_dict = {}
            event_time_dict['event_date'] = event_time.event_date
            event_time_dict['start'] = event_time.start
            event_time_dict['end'] = event_time.end
            form_step_data['times']['sets']['event_times'].append(event_time_dict)
    
        fields = ['admission_price', 'reduced_price']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'meeting_place_%s' % lang_code,
                'booking_info_%s' % lang_code,
                ]
        for f in fields:
            form_step_data['prices'][f] = getattr(instance, f)

    return form_step_data

def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Event.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Event()

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
            setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
            setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
            setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        instance.other_languages = form_step_data['basic']['other_languages'] 
        instance.museum = form_step_data['basic']['museum']
        instance.location_name = form_step_data['basic']['location_name']
        instance.street_address = form_step_data['basic']['street_address']
        instance.street_address2 = form_step_data['basic']['street_address2'] 
        instance.postal_code = form_step_data['basic']['postal_code']
        instance.district = form_step_data['basic']['district']
        instance.city = form_step_data['basic']['city']
        instance.latitude = form_step_data['basic']['latitude']
        instance.longitude = form_step_data['basic']['longitude']
        instance.exhibition = form_step_data['basic']['exhibition']
        instance.organizing_museum = form_step_data['basic']['organizing_museum']
        instance.organizer_title = form_step_data['basic']['organizer_title']
        instance.organizer_url_link = form_step_data['basic']['organizer_url_link']
        instance.tags = form_step_data['basic']['tags']

        instance.status = "draft"
        instance.save()
        
        if '_pk' not in form_step_data:
            user = get_current_user()
            instance.set_owner(user)
        
        instance.categories.clear()
        for cat in form_step_data['basic']['categories']:
            instance.categories.add(cat)
        
        instance.languages.clear()
        for cat in form_step_data['basic']['languages']:
            instance.languages.add(cat)
        
        form_step_data['_pk'] = instance.pk
            
    return form_step_data

def set_extra_context(current_step, form_steps, form_step_data, instance=None):
    if "_pk" in form_step_data:
        return {'event': Event.objects.get(pk=form_step_data['_pk'])}
    return {}

def save_data(form_steps, form_step_data, instance=None):
    is_new = not instance
    
    if not instance:
        if '_pk' in form_step_data:
            instance = Event.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Event()
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
        setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
        setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
        setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
    instance.other_languages = form_step_data['basic']['other_languages'] 
    instance.museum = form_step_data['basic']['museum']
    instance.location_name = form_step_data['basic']['location_name']
    instance.street_address = form_step_data['basic']['street_address']
    instance.street_address2 = form_step_data['basic']['street_address2'] 
    instance.postal_code = form_step_data['basic']['postal_code']
    instance.district = form_step_data['basic']['district']
    instance.city = form_step_data['basic']['city']
    instance.latitude = form_step_data['basic']['latitude']
    instance.longitude = form_step_data['basic']['longitude']
    instance.exhibition = form_step_data['basic']['exhibition']
    instance.organizing_museum = form_step_data['basic']['organizing_museum']
    instance.organizer_title = form_step_data['basic']['organizer_title']
    instance.organizer_url_link = form_step_data['basic']['organizer_url_link']
    instance.tags = form_step_data['basic']['tags']

    fields = ['admission_price', 'reduced_price']
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        fields += [
            'admission_price_info_%s' % lang_code,
            'meeting_place_%s' % lang_code,
            'booking_info_%s' % lang_code,
            ]
        setattr(instance, "admission_price_info_%s_markup_type" % lang_code, MARKUP_PLAIN_TEXT)
        setattr(instance, "meeting_place_%s_markup_type" % lang_code, MARKUP_PLAIN_TEXT)
        setattr(instance, "booking_info_%s_markup_type" % lang_code, MARKUP_PLAIN_TEXT)
            
    for f in fields:
        setattr(instance, f, form_step_data['prices'][f])

    instance.status = "published"
    instance.save()
    
    if is_new:
        user = get_current_user()
        instance.set_owner(user)    
    
    instance.categories.clear()
    for cat in form_step_data['basic']['categories']:
        instance.categories.add(cat)
    
    instance.languages.clear()
    for cat in form_step_data['basic']['languages']:
        instance.languages.add(cat)
    
    instance.eventtime_set.all().delete()
    for event_time_dict in form_step_data['times']['sets']['event_times']:
        event_time = EventTime(event=instance)
        event_time.event_date = event_time_dict['event_date'] 
        event_time.start = event_time_dict['start']
        event_time.end = event_time_dict['end']
        event_time.save()

    form_steps['success_url'] = instance.get_url_path()
    
    return form_step_data

EVENT_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "events/forms/basic_info_form.html",
        'form': BasicInfoForm,
    },
    'times': {
        'title': _("Times"),
        'template': "events/forms/times_form.html",
        'form': TimesForm,
        'formsets': {
            'event_times': EventTimeFormset,
        }
    },
    'prices': {
        'title': _("Prices"),
        'template': "events/forms/prices_form.html",
        'form': PricesForm,
    },
    'gallery': {
        'title': _("Images"),
        'template': "events/forms/gallery_form.html",
        'form': GalleryForm, # dummy form
    },
    'oninit': load_data,
    'on_set_extra_context': set_extra_context,
    'onsubmit': submit_step,
    'onsave': save_data,
    'name': 'event_registration',
    'default_path': ["basic", "times", "prices", "gallery"],
}

