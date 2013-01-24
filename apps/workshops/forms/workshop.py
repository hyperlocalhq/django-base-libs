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

Workshop = models.get_model("workshops", "Workshop")
WorkshopTime = models.get_model("workshops", "WorkshopTime")

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
        model = Workshop
        
        fields = ['categories', 'tags', 'age_groups', 'languages', 'other_languages',
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

        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].help_text = ""
        self.fields['categories'].empty_label = None
        
        self.fields['age_groups'].widget = forms.CheckboxSelectMultiple()
        self.fields['age_groups'].help_text = ""
        self.fields['age_groups'].empty_label = None
        
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
            "museum",
            "location_name",
            "street_address",
            "street_address2",
            "postal_code",
            "district",
            "city",
            "latitude",
            "longitude",
            "organizing_museum",
            "organizer_title",
            "organizer_url_link",
            "exhibition",
            css_class="fieldset-where",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),
            "languages",
            "other_languages",
            "age_groups",
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
        model = Workshop
        fields = ['admission_price', 'reduced_price']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'meeting_place_%s' % lang_code,
                'admission_price_info_%s' % lang_code,
                'booking_info_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(PricesForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'arrangements_for_children_%s' % lang_code,
                'free_entrance_for_%s' % lang_code,
                'family_ticket_%s' % lang_code,
                'group_ticket_%s' % lang_code,
                'free_entrance_times_%s' % lang_code,
                'yearly_ticket_%s' % lang_code,
                'other_tickets_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Prices"),
            'free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
            css_class="fieldset-prices",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Details"),
            layout.Div(
                'show_admission_price_info',
                'show_reduced_price_info',
                'show_arrangements_for_children',
                'show_free_entrance_for',
                'show_family_ticket',
                'show_group_ticket',
                'show_free_entrance_times',
                'show_yearly_ticket',
                'show_other_tickets', 
                css_class="inline",
                ),
            layout.Row(
                css_class="div-admission_price_info-details",
                *('admission_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-reduced_price_info-details",
                *('reduced_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-arrangements_for_children-details",
                *('arrangements_for_children_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-free_entrance_for-details",
                *('free_entrance_for_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-family_ticket-details",
                *('family_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-group_ticket-details",
                *('group_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-free_entrance_times-details",
                *('free_entrance_times_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-yearly_ticket-details",
                *('yearly_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-other_tickets-details",
                *('other_tickets_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
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
        model = Workshop
        fields = ['workshop_date', 'start', 'end']

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


def load_data(instance=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True},
            'times': {'_filled': True},
            'prices': {'_filled': True},
            }
        return form_step_data
        
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
        form_step_data['basic']['start'] = instance.start
        form_step_data['basic']['end'] = instance.end
        form_step_data['basic']['permanent'] = instance.permanent
        form_step_data['basic']['workshop_extended'] = instance.workshop_extended
        form_step_data['basic']['museum'] = instance.museum
        form_step_data['basic']['location_name'] = instance.location_name
        form_step_data['basic']['street_address'] = instance.street_address
        form_step_data['basic']['street_address2'] = instance.street_address2
        form_step_data['basic']['postal_code'] = instance.postal_code
        form_step_data['basic']['district'] = instance.district
        form_step_data['basic']['city'] = instance.city
        form_step_data['basic']['latitude'] = instance.latitude
        form_step_data['basic']['longitude'] = instance.longitude
        form_step_data['basic']['organizing_museum'] = instance.organizing_museum
        form_step_data['basic']['organizer_title'] = instance.organizer_title
        form_step_data['basic']['organizer_url_link'] = instance.organizer_url_link
        form_step_data['basic']['categories'] = instance.categories.all()
        form_step_data['basic']['tags'] = instance.tags
    
        for season in instance.season_set.all():
            season_dict = {}
            season_dict['start'] = season.start
            season_dict['end'] = season.end
            season_dict['is_appointment_based'] = season.is_appointment_based
            season_dict['mon_open'] = season.mon_open
            season_dict['mon_break_close'] = season.mon_break_close
            season_dict['mon_break_open'] = season.mon_break_open
            season_dict['mon_close'] = season.mon_close
            season_dict['mon_is_closed'] = not season.mon_open
            season_dict['tue_open'] = season.tue_open
            season_dict['tue_break_close'] = season.tue_break_close
            season_dict['tue_break_open'] = season.tue_break_open
            season_dict['tue_close'] = season.tue_close
            season_dict['tue_is_closed'] = not season.tue_open
            season_dict['wed_open'] = season.wed_open
            season_dict['wed_break_close'] = season.wed_break_close
            season_dict['wed_break_open'] = season.wed_break_open
            season_dict['wed_close'] = season.wed_close
            season_dict['wed_is_closed'] = not season.wed_open
            season_dict['thu_open'] = season.thu_open
            season_dict['thu_break_close'] = season.thu_break_close
            season_dict['thu_break_open'] = season.thu_break_open
            season_dict['thu_close'] = season.thu_close
            season_dict['thu_is_closed'] = not season.thu_open
            season_dict['fri_open'] = season.fri_open
            season_dict['fri_break_close'] = season.fri_break_close
            season_dict['fri_break_open'] = season.fri_break_open
            season_dict['fri_close'] = season.fri_close
            season_dict['fri_is_closed'] = not season.fri_open
            season_dict['sat_open'] = season.sat_open
            season_dict['sat_break_close'] = season.sat_break_close
            season_dict['sat_break_open'] = season.sat_break_open
            season_dict['sat_close'] = season.sat_close
            season_dict['sat_is_closed'] = not season.sat_open
            season_dict['sun_open'] = season.sun_open
            season_dict['sun_break_close'] = season.sun_break_close
            season_dict['sun_break_open'] = season.sun_break_open
            season_dict['sun_close'] = season.sun_close
            season_dict['sun_is_closed'] = not season.sun_open
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                season_dict['last_entry_%s' % lang_code] = getattr(season, 'last_entry_%s' % lang_code)
                season_dict['exceptions_%s' % lang_code] = getattr(season, 'exceptions_%s' % lang_code)
            form_step_data['opening']['sets']['seasons'].append(season_dict)
            
        for special_opening in instance.specialopeningtime_set.all():
            special_opening_dict = {}
            special_opening_dict['yyyy'] = special_opening.yyyy
            special_opening_dict['get_yyyy_display'] = special_opening.get_yyyy_display()
            special_opening_dict['mm'] = special_opening.mm
            special_opening_dict['get_mm_display'] = special_opening.get_mm_display()
            special_opening_dict['dd'] = special_opening.dd
            special_opening_dict['get_dd_display'] = special_opening.get_dd_display()
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                special_opening_dict['day_label_%s' % lang_code] = getattr(special_opening, 'day_label_%s' % lang_code)
                special_opening_dict['exceptions_%s' % lang_code] = getattr(special_opening, 'exceptions_%s' % lang_code)
            special_opening_dict['is_closed'] = special_opening.is_closed
            special_opening_dict['is_regular'] = special_opening.is_regular
            special_opening_dict['opening'] = special_opening.opening
            special_opening_dict['break_close'] = special_opening.break_close
            special_opening_dict['break_open'] = special_opening.break_open
            special_opening_dict['closing'] = special_opening.closing
            form_step_data['opening']['sets']['special_openings'].append(special_opening_dict)
    
        fields = ['free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
            'show_admission_price_info',
            'show_reduced_price_info',
            'show_arrangements_for_children',
            'show_free_entrance_for',
            'show_family_ticket',
            'show_group_ticket',
            'show_free_entrance_times',
            'show_yearly_ticket',
            'show_other_tickets',
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'arrangements_for_children_%s' % lang_code,
                'free_entrance_for_%s' % lang_code,
                'family_ticket_%s' % lang_code,
                'group_ticket_%s' % lang_code,
                'free_entrance_times_%s' % lang_code,
                'yearly_ticket_%s' % lang_code,
                'other_tickets_%s' % lang_code,
                ]
        for f in fields:
            form_step_data['prices'][f] = getattr(instance, f)
    
        form_step_data['accessibility']['suitable_for_disabled'] = instance.suitable_for_disabled
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['accessibility']['suitable_for_disabled_info_%s' % lang_code] = getattr(instance, 'suitable_for_disabled_info_%s' % lang_code)

    return form_step_data

def submit_step(current_step, form_steps, form_step_data, instance=None):
    museum = form_step_data.get('basic', {}).get('museum', None)
    if current_step == "basic" and museum:
        # fill in Opening hours from museum
        if not form_step_data.get('opening', {}).get('_filled', False):
            form_step_data['opening'] = {'_filled': True, 'sets': {'seasons': [], 'special_openings': []}}
            for season in museum.season_set.all():
                season_dict = {}
                season_dict['start'] = season.start
                season_dict['end'] = season.end
                season_dict['is_appointment_based'] = season.is_appointment_based
                season_dict['mon_open'] = season.mon_open
                season_dict['mon_break_close'] = season.mon_break_close
                season_dict['mon_break_open'] = season.mon_break_open
                season_dict['mon_close'] = season.mon_close
                season_dict['mon_is_closed'] = not season.mon_open
                season_dict['tue_open'] = season.tue_open
                season_dict['tue_break_close'] = season.tue_break_close
                season_dict['tue_break_open'] = season.tue_break_open
                season_dict['tue_close'] = season.tue_close
                season_dict['tue_is_closed'] = not season.tue_open
                season_dict['wed_open'] = season.wed_open
                season_dict['wed_break_close'] = season.wed_break_close
                season_dict['wed_break_open'] = season.wed_break_open
                season_dict['wed_close'] = season.wed_close
                season_dict['wed_is_closed'] = not season.wed_open
                season_dict['thu_open'] = season.thu_open
                season_dict['thu_break_close'] = season.thu_break_close
                season_dict['thu_break_open'] = season.thu_break_open
                season_dict['thu_close'] = season.thu_close
                season_dict['thu_is_closed'] = not season.thu_open
                season_dict['fri_open'] = season.fri_open
                season_dict['fri_break_close'] = season.fri_break_close
                season_dict['fri_break_open'] = season.fri_break_open
                season_dict['fri_close'] = season.fri_close
                season_dict['fri_is_closed'] = not season.fri_open
                season_dict['sat_open'] = season.sat_open
                season_dict['sat_break_close'] = season.sat_break_close
                season_dict['sat_break_open'] = season.sat_break_open
                season_dict['sat_close'] = season.sat_close
                season_dict['sat_is_closed'] = not season.sat_open
                season_dict['sun_open'] = season.sun_open
                season_dict['sun_break_close'] = season.sun_break_close
                season_dict['sun_break_open'] = season.sun_break_open
                season_dict['sun_close'] = season.sun_close
                season_dict['sun_is_closed'] = not season.sun_open
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    season_dict['last_entry_%s' % lang_code] = getattr(season, 'last_entry_%s' % lang_code)
                    season_dict['exceptions_%s' % lang_code] = getattr(season, 'exceptions_%s' % lang_code)
                form_step_data['opening']['sets']['seasons'].append(season_dict)
                
            for special_opening in museum.specialopeningtime_set.all():
                special_opening_dict = {}
                special_opening_dict['yyyy'] = special_opening.yyyy
                special_opening_dict['get_yyyy_display'] = special_opening.get_yyyy_display()
                special_opening_dict['mm'] = special_opening.mm
                special_opening_dict['get_mm_display'] = special_opening.get_mm_display()
                special_opening_dict['dd'] = special_opening.dd
                special_opening_dict['get_dd_display'] = special_opening.get_dd_display()
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    special_opening_dict['day_label_%s' % lang_code] = getattr(special_opening, 'day_label_%s' % lang_code)
                    special_opening_dict['exceptions_%s' % lang_code] = getattr(special_opening, 'exceptions_%s' % lang_code)
                special_opening_dict['is_closed'] = special_opening.is_closed
                special_opening_dict['is_regular'] = special_opening.is_regular
                special_opening_dict['opening'] = special_opening.opening
                special_opening_dict['break_close'] = special_opening.break_close
                special_opening_dict['break_open'] = special_opening.break_open
                special_opening_dict['closing'] = special_opening.closing
                form_step_data['opening']['sets']['special_openings'].append(special_opening_dict)
        
        # fill in prices from museum
        if not form_step_data.get('prices', {}).get('_filled', False):
            form_step_data['prices'] = {'_filled': True}
            fields = ['free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass'
                'show_admission_price_info',
                'show_reduced_price_info',
                'show_arrangements_for_children',
                'show_free_entrance_for',
                'show_family_ticket',
                'show_group_ticket',
                'show_free_entrance_times',
                'show_yearly_ticket',
                'show_other_tickets',
                ]
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                fields += [
                    'admission_price_info_%s' % lang_code,
                    'reduced_price_info_%s' % lang_code,
                    'arrangements_for_children_%s' % lang_code,
                    'free_entrance_for_%s' % lang_code,
                    'family_ticket_%s' % lang_code,
                    'group_ticket_%s' % lang_code,
                    'free_entrance_times_%s' % lang_code,
                    'yearly_ticket_%s' % lang_code,
                    'other_tickets_%s' % lang_code,
                    ]
            for f in fields:
                form_step_data['prices'][f] = getattr(museum, f)

    return form_step_data

def save_data(form_steps, form_step_data, instance=None):
    is_new = not instance
    
    if not instance:
        instance = Workshop()
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
        setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
        setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
        setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
    instance.start = form_step_data['basic']['start'] 
    instance.end = form_step_data['basic']['end']
    instance.permanent = form_step_data['basic']['permanent'] 
    instance.workshop_extended = form_step_data['basic']['workshop_extended'] 
    instance.museum = form_step_data['basic']['museum']
    instance.location_name = form_step_data['basic']['location_name']
    instance.street_address = form_step_data['basic']['street_address']
    instance.street_address2 = form_step_data['basic']['street_address2'] 
    instance.postal_code = form_step_data['basic']['postal_code']
    instance.district = form_step_data['basic']['district']
    instance.city = form_step_data['basic']['city']
    instance.latitude = form_step_data['basic']['latitude']
    instance.longitude = form_step_data['basic']['longitude']
    instance.organizing_museum = form_step_data['basic']['organizing_museum']
    instance.organizer_title = form_step_data['basic']['organizer_title']
    instance.organizer_url_link = form_step_data['basic']['organizer_url_link']
    instance.tags = form_step_data['basic']['tags']

    fields = ['free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
        'show_admission_price_info',
        'show_reduced_price_info',
        'show_arrangements_for_children',
        'show_free_entrance_for',
        'show_family_ticket',
        'show_group_ticket',
        'show_free_entrance_times',
        'show_yearly_ticket',
        'show_other_tickets',
        ]
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        fields += [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
            'arrangements_for_children_%s' % lang_code,
            'free_entrance_for_%s' % lang_code,
            'family_ticket_%s' % lang_code,
            'group_ticket_%s' % lang_code,
            'free_entrance_times_%s' % lang_code,
            'yearly_ticket_%s' % lang_code,
            'other_tickets_%s' % lang_code,
            ]
    for f in fields:
        setattr(instance, f, form_step_data['prices'][f])

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        for f in [
            'admission_price_info_%s' % lang_code,
            'reduced_price_info_%s' % lang_code,
            'arrangements_for_children_%s' % lang_code,
            'free_entrance_for_%s' % lang_code,
            'family_ticket_%s' % lang_code,
            'group_ticket_%s' % lang_code,
            'free_entrance_times_%s' % lang_code,
            'yearly_ticket_%s' % lang_code,
            'other_tickets_%s' % lang_code,
            ]:
            setattr(instance, f + "_markup_type", MARKUP_PLAIN_TEXT)

    instance.suitable_for_disabled = form_step_data['accessibility']['suitable_for_disabled']
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'suitable_for_disabled_info_%s' % lang_code, form_step_data['accessibility']['suitable_for_disabled_info_%s' % lang_code])
    
    instance.status = "published"
    instance.save()
    
    if is_new:
        user = get_current_user()
        instance.set_owner(user)    
    
    instance.categories.clear()
    for cat in form_step_data['basic']['categories']:
        instance.categories.add(cat)
    
    instance.season_set.all().delete()
    for season_dict in form_step_data['opening']['sets']['seasons']:
        season = Season(workshop=instance)
        season.start = season_dict['start'] 
        season.end = season_dict['end'] 
        season.is_appointment_based = season_dict['is_appointment_based'] 
        if not season_dict['mon_is_closed']:
            season.mon_open = season_dict['mon_open'] 
            season.mon_break_close = season_dict['mon_break_close'] 
            season.mon_break_open = season_dict['mon_break_open']
            season.mon_close = season_dict['mon_close']
        if not season_dict['tue_is_closed']:
            season.tue_open = season_dict['tue_open'] 
            season.tue_break_close = season_dict['tue_break_close'] 
            season.tue_break_open = season_dict['tue_break_open'] 
            season.tue_close = season_dict['tue_close'] 
        if not season_dict['wed_is_closed']:
            season.wed_open = season_dict['wed_open']
            season.wed_break_close = season_dict['wed_break_close'] 
            season.wed_break_open = season_dict['wed_break_open'] 
            season.wed_close = season_dict['wed_close'] 
        if not season_dict['thu_is_closed']:
            season.thu_open = season_dict['thu_open'] 
            season.thu_break_close = season_dict['thu_break_close'] 
            season.thu_break_open = season_dict['thu_break_open'] 
            season.thu_close = season_dict['thu_close'] 
        if not season_dict['fri_is_closed']:
            season.fri_open = season_dict['fri_open'] 
            season.fri_break_close = season_dict['fri_break_close'] 
            season.fri_break_open = season_dict['fri_break_open'] 
            season.fri_close = season_dict['fri_close'] 
        if not season_dict['sat_is_closed']:
            season.sat_open = season_dict['sat_open']
            season.sat_break_close = season_dict['sat_break_close'] 
            season.sat_break_open = season_dict['sat_break_open']
            season.sat_close = season_dict['sat_close']
        if not season_dict['sun_is_closed']:
            season.sun_open = season_dict['sun_open'] 
            season.sun_break_close = season_dict['sun_break_close'] 
            season.sun_break_open = season_dict['sun_break_open'] 
            season.sun_close = season_dict['sun_close']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
            setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
            setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
        season.save()
        
    instance.specialopeningtime_set.all().delete()
    for special_opening_dict in form_step_data['opening']['sets']['special_openings']:
        special_opening = SpecialOpeningTime(workshop=instance)
        special_opening.yyyy = special_opening_dict['yyyy'] 
        special_opening.mm = special_opening_dict['mm']
        special_opening.dd = special_opening_dict['dd']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(special_opening, 'day_label_%s' % lang_code, special_opening_dict['day_label_%s' % lang_code])
            setattr(special_opening, 'exceptions_%s' % lang_code, special_opening_dict['exceptions_%s' % lang_code])
            setattr(special_opening, 'exceptions_%s_markup_type' % lang_code, MARKUP_PLAIN_TEXT)
        special_opening.is_closed = special_opening_dict['is_closed'] 
        special_opening.is_regular = special_opening_dict['is_regular'] 
        special_opening.opening = special_opening_dict['opening'] 
        special_opening.break_close = special_opening_dict['break_close'] 
        special_opening.break_open = special_opening_dict['break_open'] 
        special_opening.closing = special_opening_dict['closing']
        special_opening.save()

    form_steps['success_url'] = instance.get_url_path()
    
    return form_step_data

WORKSHOP_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "workshops/forms/basic_info_form.html",
        'form': BasicInfoForm,
    },
    'times': {
        'title': _("Times"),
        'template': "workshops/forms/times_form.html",
        'form': TimesForm,
    },
    'prices': {
        'title': _("Prices"),
        'template': "workshops/forms/prices_form.html",
        'form': PricesForm,
    },
    'oninit': load_data,
    'onsubmit': submit_step,
    'onsave': save_data,
    'name': 'workshop_registration',
    'default_path': ["basic", "times", "prices"],
}

