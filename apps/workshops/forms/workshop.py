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
        # help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
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
        # help_text=u"Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Museums angezeigt zu bekommen.",
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
        model = Workshop
        
        fields = ['tags', 'languages', 'other_languages',
            'has_group_offer',
            'is_for_preschool',
            'is_for_primary_school',
            'is_for_youth',
            'is_for_families',
            'is_for_disabled',
            'is_for_wheelchaired',
            'is_for_deaf',
            'is_for_blind',
            'is_for_learning_difficulties',
            
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

        self.fields['tags'].widget = forms.TextInput()
        self.fields['tags'].help_text = ""
        
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
            _("Location"),
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
                        <label>{% trans "Location" %}</label>
                        <div class="workshop_map" id="gmap_wrapper">
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

            layout.Row(
                layout.Div("languages", css_class="min"),
                layout.Div("other_languages", css_class="max"),
                css_class="flex merge",
                ),

            layout.Row(
                "tags",
                ),

            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Particularities" %}</label> """),
                'has_group_offer',
                'is_for_preschool',
                'is_for_primary_school',
                'is_for_youth',
                'is_for_families',
                'is_for_disabled',
                'is_for_wheelchaired',
                'is_for_deaf',
                'is_for_blind',
                'is_for_learning_difficulties',
                css_class="inline",
                ),
                
            css_class="fieldset-categories-tags",
            ))
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),                SecondarySubmit('reset', _('Cancel')),
                ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                layout.Submit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
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
        model = Workshop
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

class WorkshopTimeForm(ModelForm):
    class Meta:
        model = WorkshopTime
        
    def __init__(self, *args, **kwargs):
        super(WorkshopTimeForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget = forms.TimeInput(format='%H:%M')
        self.fields['end'].widget = forms.TimeInput(format='%H:%M')
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        layout_blocks.append(
            layout.Row(
                layout.Field("workshop_date", placeholder="yyyy-mm-dd"),
                layout.Field("start", placeholder="00:00"),
                layout.Field("end", placeholder="00:00"),
                css_class="flex",
                ),
            )

        self.helper.layout = layout.Layout(
            *layout_blocks
            )

WorkshopTimeFormset = inlineformset_factory(Workshop, WorkshopTime, form=WorkshopTimeForm, formset=InlineFormSet, extra=0)

class GalleryForm(ModelForm):
    class Meta:
        model = Workshop
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
            'basic': {'_filled': True},
            'times': {'_filled': True, 'sets': {'workshop_times': [],}},
            'prices': {'_filled': True},
            'gallery': {'_filled': True},
            '_pk': instance.pk,
            }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
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
        for f in [            'has_group_offer',
            'is_for_preschool',
            'is_for_primary_school',
            'is_for_youth',
            'is_for_families',
            'is_for_disabled',
            'is_for_wheelchaired',
            'is_for_deaf',
            'is_for_blind',
            'is_for_learning_difficulties',
            ]:
            form_step_data['basic'][f] = getattr(instance, f)
    
        for workshop_time in instance.workshoptime_set.all():
            workshop_time_dict = {}
            workshop_time_dict['workshop_date'] = workshop_time.workshop_date
            workshop_time_dict['start'] = workshop_time.start
            workshop_time_dict['end'] = workshop_time.end
            form_step_data['times']['sets']['workshop_times'].append(workshop_time_dict)
    
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
            instance = Workshop.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Workshop()
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
        for f in [
            'is_for_preschool',
            'is_for_primary_school',
            'is_for_youth',
            'is_for_families',
            'is_for_disabled',
            'is_for_wheelchaired',
            'is_for_deaf',
            'is_for_blind',
            'is_for_learning_difficulties',
            ]:
            setattr(instance, f, form_step_data['basic'][f])
        instance.status = "draft"
        instance.save()
        
        if '_pk' not in form_step_data:
            user = get_current_user()
            instance.set_owner(user)
        
        instance.languages.clear()
        for cat in form_step_data['basic']['languages']:
            instance.languages.add(cat)
        
        form_step_data['_pk'] = instance.pk

    if current_step == "times":
        if "_pk" in form_step_data:
            instance = Workshop.objects.get(pk=form_step_data['_pk'])

            instance.workshoptime_set.all().delete()
            for workshop_time_dict in form_step_data['times']['sets']['workshop_times']:
                workshop_time = WorkshopTime(workshop=instance)
                workshop_time.workshop_date = workshop_time_dict['workshop_date'] 
                workshop_time.start = workshop_time_dict['start']
                workshop_time.end = workshop_time_dict['end']
                workshop_time.save()

    if current_step == "prices":
        if "_pk" in form_step_data:
            instance = Workshop.objects.get(pk=form_step_data['_pk'])
        
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
            instance.save()

    return form_step_data

def set_extra_context(current_step, form_steps, form_step_data, instance=None):
    if "_pk" in form_step_data:
        return {'workshop': Workshop.objects.get(pk=form_step_data['_pk'])}
    return {}


def save_data(form_steps, form_step_data, instance=None):
    is_new = not instance
    if not instance:
        if '_pk' in form_step_data:
            instance = Workshop.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Workshop()
            
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
    for f in [
        'is_for_preschool',
        'is_for_primary_school',
        'is_for_youth',
        'is_for_families',
        'is_for_disabled',
        'is_for_wheelchaired',
        'is_for_deaf',
        'is_for_blind',
        'is_for_learning_difficulties',
        ]:
        setattr(instance, f, form_step_data['basic'][f])
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
    
    instance.languages.clear()
    for cat in form_step_data['basic']['languages']:
        instance.languages.add(cat)
    
    instance.workshoptime_set.all().delete()
    for workshop_time_dict in form_step_data['times']['sets']['workshop_times']:
        workshop_time = WorkshopTime(workshop=instance)
        workshop_time.workshop_date = workshop_time_dict['workshop_date'] 
        workshop_time.start = workshop_time_dict['start']
        workshop_time.end = workshop_time_dict['end']
        workshop_time.save()

    form_steps['success_url'] = reverse("dashboard") #instance.get_url_path()
    
    return form_step_data

def cancel_editing(request):
    return redirect("dashboard")

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
        'formsets': {
            'workshop_times': WorkshopTimeFormset,
        }
    },
    'prices': {
        'title': _("Prices"),
        'template': "workshops/forms/prices_form.html",
        'form': PricesForm,
    },
    'gallery': {
        'title': _("Images"),
        'template': "workshops/forms/gallery_form.html",
        'form': GalleryForm, # dummy form
    },
    'oninit': load_data,
    'on_set_extra_context': set_extra_context,
    'onsubmit': submit_step,
    'onsave': save_data,
    'onreset': cancel_editing,
    'name': 'workshop_registration',
    'default_path': ["basic", "times", "prices", "gallery"],
}

