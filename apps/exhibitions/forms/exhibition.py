# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.models import ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms.fields import AutocompleteModelChoiceField
from base_libs.models.settings import MARKUP_HTML_WYSIWYG

Exhibition = models.get_model("exhibitions", "Exhibition")
Season = models.get_model("exhibitions", "Season")
SpecialOpeningTime = models.get_model("exhibitions", "SpecialOpeningTime")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

class SecondarySubmit(layout.Submit):
    field_classes = "btn"

class BasicInfoForm(ModelForm):
    museum = AutocompleteModelChoiceField(
        required=False,
        label=u"Name",
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
        label=u"Name",
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
    class Meta:
        model = Exhibition
        
        fields = ['start', 'end', 'permanent', 'exhibition_extended',
            'museum', 'location_name', 'street_address', 'street_address2', 'postal_code', 'district',
            'city', 'latitude', 'longitude', 
            'organizing_museum', 'organizer_title', 'organizer_url_link', 'vernissage', 'finissage', 'tags', 'categories']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                'catalog_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                'catalog_%s' % lang_code,
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
                css_class="div-accessibility-details",
                *('title_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-accessibility-details",
                *('subtitle_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-accessibility-details",
                *('description_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            layout.Row(
                css_class="div-accessibility-details",
                *('catalog_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-basic-info",
                ))

        layout_blocks.append(layout.Fieldset(
            _("When?"),
            "start",
            "end",
            "permanent",
            "exhibition_extended",
            "vernissage",
            "finissage",
            css_class="fieldset-when",
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
            css_class="fieldset-where",
            ))
        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),
            "categories",
            "tags",
            css_class="fieldset-categories-tags",
            ))
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('submit', _('Next')),
            SecondarySubmit('reset', _('Reset'), css_class="btn-warning"),
            ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )

class InlineFormSet(BaseInlineFormSet):
    """ Inline formset which accepts initial values for unsaved models """
    def __init__(self, data=None, files=None, instance=None, save_as_new=False, prefix=None, queryset=None, initial=[]):
        self._initial = initial
        super(InlineFormSet, self).__init__(data, files, instance, save_as_new, prefix, queryset)
        
    def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {'auto_id': self.auto_id, 'prefix': self.add_prefix(i)}
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self._initial:
            try:
                defaults['initial'] = self._initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty.
        if i >= self.initial_form_count():
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form

    def initial_form_count(self):
        """Returns the number of forms that are required in this FormSet."""
        if not (self.data or self.files):
            return len(self._initial)
        return super(InlineFormSet, self).initial_form_count()


class OpeningForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('submit', _('Next')),
            SecondarySubmit('reset', _('Reset'), css_class="btn-warning"),
            ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        

class SeasonForm(ModelForm):
    mon_is_open = forms.BooleanField(label=_("Mon"), required=False)
    tue_is_open = forms.BooleanField(label=_("Tue"), required=False)
    wed_is_open = forms.BooleanField(label=_("Wed"), required=False)
    thu_is_open = forms.BooleanField(label=_("Thu"), required=False)
    fri_is_open = forms.BooleanField(label=_("Fri"), required=False)
    sat_is_open = forms.BooleanField(label=_("Sat"), required=False)
    sun_is_open = forms.BooleanField(label=_("Sun"), required=False)
    
    class Meta:
        model = Season
        exclude = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            exclude.append("exceptions_%s_markup_type" % lang_code)
        
    def __init__(self, *args, **kwargs):
        super(SeasonForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'last_entry_%s' % lang_code,
                'exceptions_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        # remove labels from opening and closing times 
        for weekday in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
            self.fields['%s_open' % weekday].label = ""
            self.fields['%s_break_close' % weekday].label = ""
            self.fields['%s_break_open' % weekday].label = ""
            self.fields['%s_close' % weekday].label = ""
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Season"),
            "start",
            "end",
            "is_appointment_based",

            layout.HTML(
            """{% load i18n %}
            <table>
                <thead>
                    <tr>
                        <th>&nbsp;</th>
                        <th>{% trans "From" %}</th>
                        <th>{% trans "Break from" %}</th>
                        <th>{% trans "Break bis" %}</th>
                        <th>{% trans "Till" %}</th>
                    </tr>
                </thead>

                <tbody>
                    <tr>
                        <th>"""), "mon_is_open", layout.HTML("""</th>
                        <td>"""), "mon_open", layout.HTML("""</td>
                        <td>"""), "mon_break_close", layout.HTML("""</td>
                        <td>"""), "mon_break_open", layout.HTML("""</td>
                        <td>"""), "mon_close", layout.HTML("""</td>
                    </tr>
                    <tr>
                        <th>"""), "tue_is_open", layout.HTML("""</th>
                        <td>"""), "tue_open", layout.HTML("""</td>
                        <td>"""), "tue_break_close", layout.HTML("""</td>
                        <td>"""), "tue_break_open", layout.HTML("""</td>
                        <td>"""), "tue_close", layout.HTML("""</td>
                    </tr>
                    <tr>
                        <th>"""), "wed_is_open", layout.HTML("""</th>
                        <td>"""), "wed_open", layout.HTML("""</td>
                        <td>"""), "wed_break_close", layout.HTML("""</td>
                        <td>"""), "wed_break_open", layout.HTML("""</td>
                        <td>"""), "wed_close", layout.HTML("""</td>
                    </tr>
                    <tr>
                        <th>"""), "thu_is_open", layout.HTML("""</th>
                        <td>"""), "thu_open", layout.HTML("""</td>
                        <td>"""), "thu_break_close", layout.HTML("""</td>
                        <td>"""), "thu_break_open", layout.HTML("""</td>
                        <td>"""), "thu_close", layout.HTML("""</td>
                    </tr>
                    <tr>
                        <th>"""), "fri_is_open", layout.HTML("""</th>
                        <td>"""), "fri_open", layout.HTML("""</td>
                        <td>"""), "fri_break_close", layout.HTML("""</td>
                        <td>"""), "fri_break_open", layout.HTML("""</td>
                        <td>"""), "fri_close", layout.HTML("""</td>
                    </tr>
                    <tr>
                        <th>"""), "sat_is_open", layout.HTML("""</th>
                        <td>"""), "sat_open", layout.HTML("""</td>
                        <td>"""), "sat_break_close", layout.HTML("""</td>
                        <td>"""), "sat_break_open", layout.HTML("""</td>
                        <td>"""), "sat_close", layout.HTML("""</td>
                    </tr>
                    <tr>
                        <th>"""), "sun_is_open", layout.HTML("""</th>
                        <td>"""), "sun_open", layout.HTML("""</td>
                        <td>"""), "sun_break_close", layout.HTML("""</td>
                        <td>"""), "sun_break_open", layout.HTML("""</td>
                        <td>"""), "sun_close", layout.HTML("""</td>
                    </tr>
                </tbody>
            </table>
            """
            ),

            css_class="fieldset-season",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Additional info"),
            layout.Row(
                css_class="div-accessibility-details",
                *('last_entry_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('exceptions_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-additional-info",
                ))

        self.helper.layout = layout.Layout(
            *layout_blocks
            )

SeasonFormset = inlineformset_factory(Exhibition, Season, form=SeasonForm, formset=InlineFormSet, extra=0)

class SpecialOpeningTimeForm(ModelForm):
    class Meta:
        model = SpecialOpeningTime
        exclude = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            exclude.append("exceptions_%s_markup_type" % lang_code)
    def __init__(self, *args, **kwargs):
        super(SpecialOpeningTimeForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'day_label_%s' % lang_code,
                'exceptions_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Occasion"),
            layout.Row(
                css_class="div-accessibility-details",
                *('day_label_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-additional-info",
                ))

        layout_blocks.append(layout.Fieldset(
            _("Special date"),

            layout.Row("yyyy", "mm", "dd"),
            
            css_class="fieldset-special-date",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Opening times"),
            "is_closed",
            "is_regular",
            "opening",
            "break_close",
            "break_open",
            "closing",
            css_class="fieldset-opening-times",
            ))

        layout_blocks.append(layout.Fieldset(
            _("Additional info"),
            layout.Row(
                css_class="div-accessibility-details",
                *('exceptions_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-additional-info",
                ))

        self.helper.layout = layout.Layout(
            *layout_blocks
            )

SpecialOpeningTimeFormset = inlineformset_factory(Exhibition, SpecialOpeningTime, form=SpecialOpeningTimeForm, formset=InlineFormSet, extra=0)

class PricesForm(ModelForm):
    class Meta:
        model = Exhibition
        fields = ['free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass']
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
            layout.Row(
                css_class="div-accessibility-details",
                *('admission_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('reduced_price_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('arrangements_for_children_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('free_entrance_for_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('family_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('group_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('free_entrance_times_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('yearly_ticket_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

            layout.Row(
                css_class="div-accessibility-details",
                *('other_tickets_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),

                css_class="fieldset-basic-info",
                ))

        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('submit', _('Next')),
            SecondarySubmit('reset', _('Reset'), css_class="btn-warning"),
            ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        

class AccessibilityForm(ModelForm):
    class Meta:
        model = Exhibition
        fields = ['suitable_for_disabled',]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'suitable_for_disabled_info_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(AccessibilityForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'suitable_for_disabled_info_%s' % lang_code,
                ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Accessibility"),
            'suitable_for_disabled',

            layout.Row(
                css_class="div-accessibility-details",
                *('suitable_for_disabled_info_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES)
                ),
            
            css_class="fieldset-accessibility",
            ))

        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('submit', _('Save')),
            SecondarySubmit('reset', _('Reset'), css_class="btn-warning"),
            ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )

def load_data(instance=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True},
            'opening': {'_filled': True, 'sets': {'seasons': [], 'special_openings': []}},
            'prices': {'_filled': True},
            'accessibility': {'_filled': True},
            }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
            form_step_data['basic']['catalog_%s' % lang_code] = getattr(instance, 'catalog_%s' % lang_code)
        form_step_data['basic']['start'] = instance.start
        form_step_data['basic']['end'] = instance.end
        form_step_data['basic']['permanent'] = instance.permanent
        form_step_data['basic']['exhibition_extended'] = instance.exhibition_extended
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
        form_step_data['basic']['vernissage'] = instance.vernissage
        form_step_data['basic']['finissage'] = instance.finissage
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
            season_dict['mon_is_open'] = bool(season.mon_open)
            season_dict['tue_open'] = season.tue_open
            season_dict['tue_break_close'] = season.tue_break_close
            season_dict['tue_break_open'] = season.tue_break_open
            season_dict['tue_close'] = season.tue_close
            season_dict['tue_is_open'] = bool(season.tue_open)
            season_dict['wed_open'] = season.wed_open
            season_dict['wed_break_close'] = season.wed_break_close
            season_dict['wed_break_open'] = season.wed_break_open
            season_dict['wed_close'] = season.wed_close
            season_dict['wed_is_open'] = bool(season.wed_open)
            season_dict['thu_open'] = season.thu_open
            season_dict['thu_break_close'] = season.thu_break_close
            season_dict['thu_break_open'] = season.thu_break_open
            season_dict['thu_close'] = season.thu_close
            season_dict['thu_is_open'] = bool(season.thu_open)
            season_dict['fri_open'] = season.fri_open
            season_dict['fri_break_close'] = season.fri_break_close
            season_dict['fri_break_open'] = season.fri_break_open
            season_dict['fri_close'] = season.fri_close
            season_dict['fri_is_open'] = bool(season.fri_open)
            season_dict['sat_open'] = season.sat_open
            season_dict['sat_break_close'] = season.sat_break_close
            season_dict['sat_break_open'] = season.sat_break_open
            season_dict['sat_close'] = season.sat_close
            season_dict['sat_is_open'] = bool(season.sat_open)
            season_dict['sun_open'] = season.sun_open
            season_dict['sun_break_close'] = season.sun_break_close
            season_dict['sun_break_open'] = season.sun_break_open
            season_dict['sun_close'] = season.sun_close
            season_dict['sun_is_open'] = bool(season.sun_open)
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
    
        fields = ['free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass']
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
        # fill in opening times from museum
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
                season_dict['mon_is_open'] = bool(season.mon_open)
                season_dict['tue_open'] = season.tue_open
                season_dict['tue_break_close'] = season.tue_break_close
                season_dict['tue_break_open'] = season.tue_break_open
                season_dict['tue_close'] = season.tue_close
                season_dict['tue_is_open'] = bool(season.tue_open)
                season_dict['wed_open'] = season.wed_open
                season_dict['wed_break_close'] = season.wed_break_close
                season_dict['wed_break_open'] = season.wed_break_open
                season_dict['wed_close'] = season.wed_close
                season_dict['wed_is_open'] = bool(season.wed_open)
                season_dict['thu_open'] = season.thu_open
                season_dict['thu_break_close'] = season.thu_break_close
                season_dict['thu_break_open'] = season.thu_break_open
                season_dict['thu_close'] = season.thu_close
                season_dict['thu_is_open'] = bool(season.thu_open)
                season_dict['fri_open'] = season.fri_open
                season_dict['fri_break_close'] = season.fri_break_close
                season_dict['fri_break_open'] = season.fri_break_open
                season_dict['fri_close'] = season.fri_close
                season_dict['fri_is_open'] = bool(season.fri_open)
                season_dict['sat_open'] = season.sat_open
                season_dict['sat_break_close'] = season.sat_break_close
                season_dict['sat_break_open'] = season.sat_break_open
                season_dict['sat_close'] = season.sat_close
                season_dict['sat_is_open'] = bool(season.sat_open)
                season_dict['sun_open'] = season.sun_open
                season_dict['sun_break_close'] = season.sun_break_close
                season_dict['sun_break_open'] = season.sun_break_open
                season_dict['sun_close'] = season.sun_close
                season_dict['sun_is_open'] = bool(season.sun_open)
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
            fields = ['free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass']
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
    if not instance:
        instance = Exhibition()
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code]) 
        setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
        setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
        getattr(instance, 'catalog_%s' % lang_code, form_step_data['basic']['catalog_%s' % lang_code])
        setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        getattr(instance, 'catalog_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
    instance.start = form_step_data['basic']['start'] 
    instance.end = form_step_data['basic']['end']
    instance.permanent = form_step_data['basic']['permanent'] 
    instance.exhibition_extended = form_step_data['basic']['exhibition_extended'] 
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
    instance.vernissage = form_step_data['basic']['vernissage']
    instance.finissage = form_step_data['basic']['finissage']
    instance.tags = form_step_data['basic']['tags']

    fields = ['free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass']
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
            setattr(instance, f + "_markup_type", MARKUP_HTML_WYSIWYG)

    instance.suitable_for_disabled = form_step_data['accessibility']['suitable_for_disabled']
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'suitable_for_disabled_info_%s' % lang_code, form_step_data['accessibility']['suitable_for_disabled_info_%s' % lang_code])
    
    instance.status = "published"
    instance.save()
    
    for cat in form_step_data['basic']['categories']:
        instance.categories.add(cat)
    
    instance.season_set.all().delete()
    for season_dict in form_step_data['opening']['sets']['seasons']:
        season = Season(exhibition=instance)
        season.start = season_dict['start'] 
        season.end = season_dict['end'] 
        season.is_appointment_based = season_dict['is_appointment_based'] 
        season.mon_open = season_dict['mon_open'] 
        season.mon_break_close = season_dict['mon_break_close'] 
        season.mon_break_open = season_dict['mon_break_open']
        season.mon_close = season_dict['mon_close']
        season.tue_open = season_dict['tue_open'] 
        season.tue_break_close = season_dict['tue_break_close'] 
        season.tue_break_open = season_dict['tue_break_open'] 
        season.tue_close = season_dict['tue_close'] 
        season.wed_open = season_dict['wed_open']
        season.wed_break_close = season_dict['wed_break_close'] 
        season.wed_break_open = season_dict['wed_break_open'] 
        season.wed_close = season_dict['wed_close'] 
        season.thu_open = season_dict['thu_open'] 
        season.thu_break_close = season_dict['thu_break_close'] 
        season.thu_break_open = season_dict['thu_break_open'] 
        season.thu_close = season_dict['thu_close'] 
        season.fri_open = season_dict['fri_open'] 
        season.fri_break_close = season_dict['fri_break_close'] 
        season.fri_break_open = season_dict['fri_break_open'] 
        season.fri_close = season_dict['fri_close'] 
        season.sat_open = season_dict['sat_open']
        season.sat_break_close = season_dict['sat_break_close'] 
        season.sat_break_open = season_dict['sat_break_open']
        season.sat_close = season_dict['sat_close']
        season.sun_open = season_dict['sun_open'] 
        season.sun_break_close = season_dict['sun_break_close'] 
        season.sun_break_open = season_dict['sun_break_open'] 
        season.sun_close = season_dict['sun_close']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(season, 'last_entry_%s' % lang_code, season_dict['last_entry_%s' % lang_code])
            setattr(season, 'exceptions_%s' % lang_code, season_dict['exceptions_%s' % lang_code])
            setattr(season, 'exceptions_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        season.save()
        
    instance.specialopeningtime_set.all().delete()
    for special_opening_dict in form_step_data['opening']['sets']['special_openings']:
        special_opening = SpecialOpeningTime(exhibition=instance)
        special_opening.yyyy = special_opening_dict['yyyy'] 
        special_opening.mm = special_opening_dict['mm']
        special_opening.dd = special_opening_dict['dd']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(special_opening, 'day_label_%s' % lang_code, special_opening_dict['day_label_%s' % lang_code])
            setattr(special_opening, 'exceptions_%s' % lang_code, special_opening_dict['exceptions_%s' % lang_code])
            setattr(special_opening, 'exceptions_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
        special_opening.is_closed = special_opening_dict['is_closed'] 
        special_opening.is_regular = special_opening_dict['is_regular'] 
        special_opening.opening = special_opening_dict['opening'] 
        special_opening.break_close = special_opening_dict['break_close'] 
        special_opening.break_open = special_opening_dict['break_open'] 
        special_opening.closing = special_opening_dict['closing']
        special_opening.save()

    form_steps['success_url'] = instance.get_url_path()
    
    return form_step_data

EXHIBITION_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "exhibitions/forms/basic_info_form.html",
        'form': BasicInfoForm,
    },
    'opening': {
        'title': _("Opening times"),
        'template': "exhibitions/forms/opening_form.html",
        'form': OpeningForm, # dummy form
        'formsets': {
            'seasons': SeasonFormset,
            'special_openings': SpecialOpeningTimeFormset,
        }
    },
    'prices': {
        'title': _("Prices"),
        'template': "exhibitions/forms/prices_form.html",
        'form': PricesForm,
    },
    'accessibility': {
        'title': _("Accessibility"),
        'template': "exhibitions/forms/accessibility_form.html",
        'form': AccessibilityForm,
    },
    'oninit': load_data,
    'onsubmit': submit_step,
    'onsave': save_data,
    'name': 'exhibition_registration',
    'default_path': ["basic", "opening", "prices", "accessibility"],
}

