# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.models import ModelForm
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from babeldjango.templatetags.babel import decimalfmt

from base_libs.forms.fields import AutocompleteModelChoiceField, DecimalField
from base_libs.models.settings import MARKUP_HTML_WYSIWYG, MARKUP_PLAIN_TEXT
from base_libs.middleware import get_current_user

Museum = models.get_model("museums", "Museum")
Exhibition = models.get_model("exhibitions", "Exhibition")
Event = models.get_model("events", "Event")
EventTime = models.get_model("events", "EventTime")
Organizer = models.get_model("events", "Organizer")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

from museumsportal.utils.forms import SecondarySubmit
from museumsportal.utils.forms import InlineFormSet
from museumsportal.utils.forms import SplitDateTimeWidget

class BasicInfoForm(ModelForm):
    museum = AutocompleteModelChoiceField(
        required=False,
        label=_("Museum from the list <b>(active)</b> / <a href=\"#\">Free location</a>"),
        # help_text=_("If location doesn't exist in the database, please click <a href=\"#\">here</a> to enter it."),
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
        # help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
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
        
        fields = ['categories', 'tags', 'languages', 'other_languages', 'suitable_for_children',
            'museum', 'location_name', 'street_address', 'street_address2', 'postal_code',
            'district', 'city', 'latitude', 'longitude', 'exhibition',
            ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'press_text_%s' % lang_code,
                'website_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            self.fields['website_%s' % lang_code] = forms.URLField(
                label=_("Website"),
                required=False,
                )

        self.fields['street_address'].required = True
        self.fields['postal_code'].required = True
        self.fields['city'].required = True

        self.fields['tags'].widget = forms.TextInput()
        self.fields['tags'].help_text = ""
        self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        self.fields['categories'].help_text = ""
        self.fields['categories'].empty_label = None
        self.fields['languages'].widget = forms.CheckboxSelectMultiple()
        self.fields['languages'].help_text = ""
        self.fields['languages'].empty_label = None

        self.fields['location_name'].label = _("Free location <b>(active)</b> / <a href=\"#\">Museum from the list</a>")
        # self.fields['location_name'].help_text = _("If you want to select a location from the database, please click <a href=\"#\">here</a>.")

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'press_text_%s' % lang_code,
                'website_%s' % lang_code,
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
                css_class="div-press_text",
                *(layout.Field('press_text_%s' % lang_code, css_class="tinymce") for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-website",
                *(layout.Field('website_%s' % lang_code, placeholder="http://") for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            css_class="fieldset-basic-info",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Location"),
            layout.Row(
                layout.Div(
                    layout.Field("museum", template="bootstrap/field_marked_as_required.html"),
                    layout.Field("location_name", template="bootstrap/field_marked_as_required.html"),
                    "street_address",
                    "street_address2",
                    "postal_code",
                    "district",
                    "city",
                    ),
                layout.HTML("""{% load i18n %}
                    <div id="dyn_set_map">
                        <label>{% trans "Location" %}</label>
                        <div class="event_map" id="gmap_wrapper">
                            <!-- THE GMAPS WILL BE INSERTED HERE DYNAMICALLY -->
                        </div>
                        <div class="form-actions">
                            <input id="dyn_locate_geo" type="button" class="btn btn-small" value="{% trans "Relocate on map" %}" />&zwnj;
                            <!--<input id="dyn_remove_geo" type="button" class="btn btn-small" value="{% trans "Remove from map" %}"/>&zwnj;-->
                        </div>
                    </div>
                """),
                "latitude",
                "longitude",
                ),
            css_class="fieldset-where",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Organizers (when differ from location)"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.organizers.management_form }}
            <div id="organizers">
                {% for form in formsets.organizers.forms %}
                    <div class="organizer formset-form tabular-inline">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="organizers_empty_form" class="organizer formset-form tabular-inline" style="display: none">
                {% with formsets.organizers.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="organizers_fieldset",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Related exhibition"),
            "exhibition",
            css_class="fieldset-related-exhibition",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),
            
            layout.Row(
                layout.Div("languages", css_class="min"),
                layout.Div("other_languages", css_class="max"),
                css_class="flex merge",
                ),
            
            layout.Row(
                layout.Div("categories", css_class="min"),
                layout.Div(layout.HTML("""<label>&nbsp;</label> """),"suitable_for_children", css_class="inline max"),
                css_class="flex merge",
                ),

            layout.Row("tags"),

            css_class="fieldset-categories-tags",
            ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )

    def clean(self):
        cleaned_data = super(BasicInfoForm, self).clean()
        if not cleaned_data.get("museum") and not cleaned_data.get("location_name"):
            self._errors['museum'] = self.error_class([_("This field is required.")])
            del cleaned_data['museum']
            del cleaned_data['location_name']
        return cleaned_data

class OrganizerForm(ModelForm):
    organizing_museum = AutocompleteModelChoiceField(
        required=False,
        label=_("Museum from the list <b>(active)</b> / <a href=\"#\">Other Organizer</a>"),
        # help_text=_("If organizer doesn't exist in the database, please click <a href=\"#\">here</a> to enter it."),
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
    
    class Meta:
        model = Organizer
    def __init__(self, *args, **kwargs):
        super(OrganizerForm, self).__init__(*args, **kwargs)

        self.fields['organizer_title'].label = _("Other Organizer <b>(active)</b> / <a href=\"#\">Museum from the list</a>")
        self.fields['organizer_url_link'].label = _("Website")
        # self.fields['organizer_title'].help_text = _("If you want to select an organizer from the database, please click <a href=\"#\">here</a>.")

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Div(
                layout.Row(
                    layout.Div("organizing_museum", css_class="max"), 
                    css_class="flex",
                    ),
                layout.Row(
                    layout.Div("organizer_title"),
                    layout.Div(layout.Field("organizer_url_link", placeholder="http://"), css_class="max"),
                    css_class="flex",
                    ),
                css_class="div_organizer"
                )
            )

        self.helper.layout = layout.Layout(
            *layout_blocks
            )

OrganizerFormset = inlineformset_factory(Event, Organizer, form=OrganizerForm, formset=InlineFormSet, extra=0)


class PricesForm(ModelForm):
    admission_price = DecimalField(
        label=_(u"Admission price (€)"),
        max_digits=5,
        decimal_places=2,
        required=False,
        )
    reduced_price = DecimalField(
        label=_(u"Reduced admission price (€)"),
        max_digits=5,
        decimal_places=2,
        required=False,
        )
    class Meta:
        model = Event
        fields = ['free_admission', 'admission_price', 'reduced_price']
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
            layout.Row('free_admission', css_class="inline"),
            layout.Row(
                layout.Field('admission_price', placeholder=decimalfmt(0, "#,##0.00")),
                layout.Field('reduced_price', placeholder=decimalfmt(0, "#,##0.00")),
                ),
            layout.Row(
                css_class="div-admission_price_info-details",
                *('admission_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            css_class="fieldset-prices",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Details"),
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
                SecondarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
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
                SecondarySubmit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        

class EventTimeForm(ModelForm):
    class Meta:
        model = EventTime
        
    def __init__(self, *args, **kwargs):
        super(EventTimeForm, self).__init__(*args, **kwargs)
        self.fields['event_date'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['event_date'].input_formats=('%d.%m.%Y',)
        
        self.fields['start'].required = True
        self.fields['start'].widget = forms.TimeInput(format='%H:%M')
        self.fields['end'].widget = forms.TimeInput(format='%H:%M')
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        layout_blocks.append(
            layout.Row(
                layout.Field("event_date", placeholder="dd.mm.yyyy", autocomplete="off"),
                layout.Field("start", placeholder="00:00"),
                layout.Field("end", placeholder="00:00"),
                css_class="flex",
                ),
            )

        self.helper.layout = layout.Layout(
            *layout_blocks
            )

EventTimeFormset = inlineformset_factory(Event, EventTime, form=EventTimeForm, formset=InlineFormSet, extra=0)

class BatchEventTimeForm(forms.Form):
    range_start = forms.DateField(
        label=_("Start"),
        required=True,
        )
    range_end = forms.DateField(
        label=_("End"),
        required=True,
        )
    repeat = forms.ChoiceField(
        label=_("Repeat"),
        required=True,
        choices=((1, _("Every week")), (2, _("Every second week"))),
        )
    mon_start = forms.TimeField(
        label=_("Starts on Monday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    mon_end = forms.TimeField(
        label=_("Ends on Monday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    tue_start = forms.TimeField(
        label=_("Starts on Tuesday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    tue_end = forms.TimeField(
        label=_("Ends on Tuesday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    wed_start = forms.TimeField(
        label=_("Starts on Wednesday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    wed_end = forms.TimeField(
        label=_("Ends on Wednesday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    thu_start = forms.TimeField(
        label=_("Starts on Thursday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    thu_end = forms.TimeField(
        label=_("Ends on Thursday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    fri_start = forms.TimeField(
        label=_("Starts on Friday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    fri_end = forms.TimeField(
        label=_("Ends on Friday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    sat_start = forms.TimeField(
        label=_("Starts on Saturday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    sat_end = forms.TimeField(
        label=_("Ends on Saturday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    sun_start = forms.TimeField(
        label=_("Starts on Sunday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )
    sun_end = forms.TimeField(
        label=_("Ends on Sunday"),
        required=False,
        widget=forms.TimeInput(format='%H:%M'),
        )

    def __init__(self, *args, **kwargs):
        super(BatchEventTimeForm, self).__init__(*args, **kwargs)
        self.fields['range_start'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['range_start'].input_formats=('%d.%m.%Y',)
        
        self.fields['range_end'].widget = forms.DateInput(format='%d.%m.%Y')
        self.fields['range_end'].input_formats=('%d.%m.%Y',)
        
        self.helper = FormHelper()
        self.helper.form_id = "batch_event_time_form"
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Batch event time creation"),
            
            layout.Row(
                layout.Field("range_start", placeholder="dd.mm.yyyy"),
                layout.Field("range_end", placeholder="dd.mm.yyyy"),
                ),
            "repeat",
            layout.Row(
                layout.Field("mon_start", placeholder="00:00"),
                layout.Field("tue_start", placeholder="00:00"),
                layout.Field("wed_start", placeholder="00:00"),
                layout.Field("thu_start", placeholder="00:00"),
                layout.Field("fri_start", placeholder="00:00"),
                layout.Field("sat_start", placeholder="00:00"),
                layout.Field("sun_start", placeholder="00:00"),
                ),
            layout.Row(
                layout.Field("mon_end", placeholder="00:00"),
                layout.Field("tue_end", placeholder="00:00"),
                layout.Field("wed_end", placeholder="00:00"),
                layout.Field("thu_end", placeholder="00:00"),
                layout.Field("fri_end", placeholder="00:00"),
                layout.Field("sat_end", placeholder="00:00"),
                layout.Field("sun_end", placeholder="00:00"),
                ),
            ))
        
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('submit', _('Create event times')),
            layout.Button('go_back', _('Go back')),
            ))

        self.helper.layout = layout.Layout(
            *layout_blocks
            )

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
                layout.Submit('save_and_close', _('Close')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
                SecondarySubmit('reset', _('Cancel')),
                ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )


def load_data(instance=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True, 'sets': {'organizers': []}},
            'times': {'_filled': True, 'sets': {'event_times': [],}},
            'prices': {'_filled': True},
            'gallery': {'_filled': True},
            '_pk': instance.pk,
            }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
            form_step_data['basic']['press_text_%s' % lang_code] = getattr(instance, 'press_text_%s' % lang_code)
            form_step_data['basic']['website_%s' % lang_code] = getattr(instance, 'website_%s' % lang_code)
        form_step_data['basic']['categories'] = instance.categories.all()
        form_step_data['basic']['tags'] = instance.tags
        form_step_data['basic']['languages'] = instance.languages.all()
        form_step_data['basic']['other_languages'] = instance.other_languages
        form_step_data['basic']['suitable_for_children'] = instance.suitable_for_children
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
    
        for organizer in instance.organizer_set.all():
            organizer_dict = {}
            organizer_dict['organizing_museum'] = organizer.organizing_museum
            organizer_dict['organizer_title'] = organizer.organizer_title
            organizer_dict['organizer_url_link'] = organizer.organizer_url_link
            form_step_data['basic']['sets']['organizers'].append(organizer_dict)
            
        for event_time in instance.eventtime_set.all():
            event_time_dict = {}
            event_time_dict['event_date'] = event_time.event_date
            event_time_dict['start'] = event_time.start
            event_time_dict['end'] = event_time.end
            form_step_data['times']['sets']['event_times'].append(event_time_dict)
    
        fields = ['free_admission', 'admission_price', 'reduced_price']
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
            setattr(instance, 'press_text_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
            setattr(instance, 'website_%s' % lang_code, form_step_data['basic']['website_%s' % lang_code])
            setattr(instance, 'press_text_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
            if not instance.description_locked:
                setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
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
        instance.tags = form_step_data['basic']['tags']
        instance.suitable_for_children = form_step_data['basic']['suitable_for_children']
        
        if not instance.status:
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
        
        instance.organizer_set.all().delete()
        for organizer_dict in form_step_data['basic']['sets']['organizers']:
            organizer = Organizer(event=instance)
            organizer.organizing_museum = organizer_dict['organizing_museum'] 
            organizer.organizer_title = organizer_dict['organizer_title']
            organizer.organizer_url_link = organizer_dict['organizer_url_link']
            organizer.save()
        
        form_step_data['_pk'] = instance.pk
    
    if current_step == "times":
        if "_pk" in form_step_data:
            instance = Event.objects.get(pk=form_step_data['_pk'])

            instance.eventtime_set.all().delete()
            for event_time_dict in form_step_data['times']['sets']['event_times']:
                event_time = EventTime(event=instance)
                event_time.event_date = event_time_dict['event_date'] 
                event_time.start = event_time_dict['start']
                event_time.end = event_time_dict['end']
                event_time.save()
                
            instance.update_closest_event_time()

    if current_step == "prices":
        if "_pk" in form_step_data:
            instance = Event.objects.get(pk=form_step_data['_pk'])
        
            fields = ['free_admission', 'admission_price', 'reduced_price']
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
            instance.save()

    return form_step_data

def set_extra_context(current_step, form_steps, form_step_data, instance=None):
    extra_context = {}
    if "_pk" in form_step_data:
        extra_context['event'] = Event.objects.get(pk=form_step_data['_pk'])
    if current_step == "times":
        extra_context['batch_event_time_form'] = BatchEventTimeForm()
    return extra_context

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
        setattr(instance, 'press_text_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
        setattr(instance, 'website_%s' % lang_code, form_step_data['basic']['website_%s' % lang_code])
        setattr(instance, 'press_text_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        if not instance.description_locked:
            setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['press_text_%s' % lang_code])
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
    instance.tags = form_step_data['basic']['tags']
    instance.suitable_for_children = form_step_data['basic']['suitable_for_children']

    fields = ['free_admission', 'admission_price', 'reduced_price']
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
    
    instance.organizer_set.all().delete()
    for organizer_dict in form_step_data['basic']['sets']['organizers']:
        organizer = Organizer(event=instance)
        organizer.organizing_museum = organizer_dict['organizing_museum'] 
        organizer.organizer_title = organizer_dict['organizer_title']
        organizer.organizer_url_link = organizer_dict['organizer_url_link']
        organizer.save()

    instance.eventtime_set.all().delete()
    for event_time_dict in form_step_data['times']['sets']['event_times']:
        event_time = EventTime(event=instance)
        event_time.event_date = event_time_dict['event_date'] 
        event_time.start = event_time_dict['start']
        event_time.end = event_time_dict['end']
        event_time.save()

    instance.update_closest_event_time()

    form_steps['success_url'] = reverse("dashboard") #instance.get_url_path()
    
    return form_step_data

def cancel_editing(request):
    return redirect("dashboard")

EVENT_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "events/forms/basic_info_form.html",
        'form': BasicInfoForm,
        'formsets': {
            'organizers': OrganizerFormset,
        }
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
    'onreset': cancel_editing,
    'general_error_message': _("There are errors in this form. Please correct them and try to save again."),
    'name': 'event_registration',
    'default_path': ["basic", "times", "prices", "gallery"],
}

