# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms.models import ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

Museum = models.get_model("museums", "Museum")
Season = models.get_model("museums", "Season")
SpecialOpeningTime = models.get_model("museums", "SpecialOpeningTime")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES) 

class BasicInfoForm(ModelForm):
    class Meta:
        model = Museum
        
        fields = ['tags', 'categories']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Basic Info (%s)") % lang_name,
                "title_%s" % lang_code,
                "subtitle_%s" % lang_code,
                "description_%s" % lang_code,
                css_class="multilingual",
                ))
        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),
            "categories",
            "tags",
            ))
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('reset', _('Reset'), css_class="btn-warning"),
            layout.Submit('submit', _('Next')),
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


class OpeningForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('reset', _('Reset'), css_class="btn-warning"),
            layout.Submit('submit', _('Next')),
            ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        

class SeasonForm(ModelForm):
    class Meta:
        model = Season
        exclude = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            exclude.append("exceptions_%s_markup_type" % lang_code)
        
    def __init__(self, *args, **kwargs):
        super(SeasonForm, self).__init__(*args, **kwargs)
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
            ))
        layout_blocks.extend([layout.HTML(
            """{% load i18n %}<table><thead><tr>
                <th>&nbsp;</th>
                <th>{% trans "Monday" %}</th>
                <th>{% trans "Tuesday" %}</th>
                <th>{% trans "Wednesday" %}</th>
                <th>{% trans "Thursday" %}</th>
                <th>{% trans "Friday" %}</th>
                <th>{% trans "Saturday" %}</th>
                <th>{% trans "Sunday" %}</th>
            </tr></thead><tbody>
            <tr>
                <th>{% trans "Opens" %}</th>
                <td>"""), "mon_open", layout.HTML("""</td>
                <td>"""), "tue_open", layout.HTML("""</td>
                <td>"""), "wed_open", layout.HTML("""</td>
                <td>"""), "thu_open", layout.HTML("""</td>
                <td>"""), "fri_open", layout.HTML("""</td>
                <td>"""), "sat_open", layout.HTML("""</td>
                <td>"""), "sun_open", layout.HTML("""</td>
            </tr>
            <tr>
                <th>{% load i18n %}{% trans "Break starts" %}</th>
                <td>"""), "mon_break_close", layout.HTML("""</td>
                <td>"""), "tue_break_close", layout.HTML("""</td>
                <td>"""), "wed_break_close", layout.HTML("""</td>
                <td>"""), "thu_break_close", layout.HTML("""</td>
                <td>"""), "fri_break_close", layout.HTML("""</td>
                <td>"""), "sat_break_close", layout.HTML("""</td>
                <td>"""), "sun_break_close", layout.HTML("""</td>
            </tr>
            <tr>
                <th>{% load i18n %}{% trans "Break ends" %}</th>
                <td>"""), "mon_break_open", layout.HTML("""</td>
                <td>"""), "tue_break_open", layout.HTML("""</td>
                <td>"""), "wed_break_open", layout.HTML("""</td>
                <td>"""), "thu_break_open", layout.HTML("""</td>
                <td>"""), "fri_break_open", layout.HTML("""</td>
                <td>"""), "sat_break_open", layout.HTML("""</td>
                <td>"""), "sun_break_open", layout.HTML("""</td>
            </tr>
            <tr>
                <th>{% load i18n %}{% trans "Closes" %}</th>
                <td>"""), "mon_close", layout.HTML("""</td>
                <td>"""), "tue_close", layout.HTML("""</td>
                <td>"""), "wed_close", layout.HTML("""</td>
                <td>"""), "thu_close", layout.HTML("""</td>
                <td>"""), "fri_close", layout.HTML("""</td>
                <td>"""), "sat_close", layout.HTML("""</td>
                <td>"""), "sun_close", layout.HTML("""</td>
            </tr>
            </tbody></table>
            """
            )])
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Additional info (%s)") % lang_name,
                "last_entry_%s" % lang_code,
                "exceptions_%s" % lang_code,
                ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )     

SeasonFormset = inlineformset_factory(Museum, Season, form=SeasonForm, formset=InlineFormSet, extra=1)

class SpecialOpeningTimeForm(ModelForm):
    class Meta:
        model = SpecialOpeningTime
    def __init__(self, *args, **kwargs):
        super(SpecialOpeningTimeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Special date"),
            "yyyy",
            "mm",
            "dd",
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Occasion (%s)") % lang_name,
                "day_label_%s" % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Opening times"),
            "is_closed",
            "is_regular",
            "opening",
            "break_close",
            "break_open",
            "closing",
            ))
        self.helper.layout = layout.Layout(
            *layout_blocks
            )     

SpecialOpeningTimeFormset = inlineformset_factory(Museum, SpecialOpeningTime, form=SpecialOpeningTimeForm, formset=InlineFormSet, extra=1)

class PricesForm(ModelForm):
    class Meta:
        model = Museum
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
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Prices"),
            'free_entrance', 'admission_price', 'reduced_price', 'member_of_museumspass',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Details (%s)") % lang_name,
                'admission_price_info_%s' % lang_code,
                'reduced_price_info_%s' % lang_code,
                'arrangements_for_children_%s' % lang_code,
                'free_entrance_for_%s' % lang_code,
                'family_ticket_%s' % lang_code,
                'group_ticket_%s' % lang_code,
                'free_entrance_times_%s' % lang_code,
                'yearly_ticket_%s' % lang_code,
                'other_tickets_%s' % lang_code,
                ))
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('reset', _('Reset'), css_class="btn-warning"),
            layout.Submit('submit', _('Next')),
            ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        
                
        
class AddressForm(ModelForm):
    class Meta:
        model = Museum
        fields = ['street_address', 'street_address2', 'postal_code', 'district',
            'city', 'latitude', 'longitude',
            'phone', 'fax', 'email', 'website', 'twitter', 'facebook',
            'contact_name', 'contact_phone_country', 'contact_phone_area', 'contact_phone_number', 'contact_email',
            'post_street_address', 'post_street_address2', 'post_postal_code', 'post_city',
            ]
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Location"),
            'street_address', 'street_address2', 'postal_code', 'district',
            'city', 'country',
            'latitude', 'longitude',
            ))
        layout_blocks.append(layout.Fieldset(
            _("Postal address (if differs from museum's address)"),
            'post_street_address', 'post_street_address2', 'post_postal_code', 'post_city',
            ))
        layout_blocks.append(layout.Fieldset(
            _("Contact person"),
            'contact_name', 
            layout.Row('contact_phone_country', 'contact_phone_area', 'contact_phone_number', css_class="phone"),
            'contact_email',
            ))
        layout_blocks.append(layout.Fieldset(
            _("Other contact info"),
            'phone', 'fax', 'email', 'website',
            ))
        layout_blocks.append(layout.Fieldset(
            _("Social media"),
            'twitter', 'facebook',
            ))
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('reset', _('Reset'), css_class="btn-warning"),
            layout.Submit('submit', _('Next')),
            ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        
            
class ServicesAccessibilityForm(ModelForm):
    class Meta:
        model = Museum
        fields = ['accessibility_options', 'service_shop', 'service_books', 'service_restaurant',
        'service_cafe', 'service_library', 'service_archive', 'service_studio', 'service_online', 
        'service_diaper_changing_table', 'service_birthdays', 'service_rent', 'service_other']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'accessibility_%s' % lang_code,
                'service_shop_info_%s' % lang_code,
                'service_books_info_%s' % lang_code,
                'service_restaurant_info_%s' % lang_code,
                'service_cafe_info_%s' % lang_code,
                'service_library_info_%s' % lang_code,
                'service_archive_info_%s' % lang_code,
                'service_studio_info_%s' % lang_code,
                'service_online_info_%s' % lang_code,
                'service_birthdays_info_%s' % lang_code,
                'service_rent_info_%s' % lang_code,
                'service_other_info_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(ServicesAccessibilityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        layout_blocks.append(layout.Fieldset(
            _("Accessibility Options"),
            'accessibility_options',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Accessibility (%s)") % lang_name,
                'accessibility_%s' % lang_code,
                #'mediation_offer_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Shop"),
            'service_shop',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Shop Details (%s)") % lang_name,
                'service_shop_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Bookstore"),
            'service_books',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Bookstore Details (%s)") % lang_name,
                'service_books_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Restaurant"),
            'service_restaurant',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Restaurant Details (%s)") % lang_name,
                'service_restaurant_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Cafe"),
            'service_cafe',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Cafe Details (%s)") % lang_name,
                'service_cafe_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Library"),
            'service_library',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Library Details (%s)") % lang_name,
                'service_library_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Archive"),
            'service_archive',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Archive Details (%s)") % lang_name,
                'service_archive_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Studio"),
            'service_studio',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Studio Details (%s)") % lang_name,
                'service_studio_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Online Offers"),
            'service_online',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Online Offers' Details (%s)") % lang_name,
                'service_online_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Diaper changing table"),
            'service_diaper_changing_table',
            ))
        layout_blocks.append(layout.Fieldset(
            _("Children birthdays"),
            'service_birthdays',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Children Birthdays' Details (%s)") % lang_name,
                'service_birthdays_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Rent"),
            'service_rent',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Rent Details (%s)") % lang_name,
                'service_rent_info_%s' % lang_code,
                ))
        layout_blocks.append(layout.Fieldset(
            _("Other services"),
            'service_other',
            ))
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Other Services' Details (%s)") % lang_name,
                'service_other_info_%s' % lang_code,
                ))
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('reset', _('Reset'), css_class="btn-warning"),
            layout.Submit('submit', _('Next')),
            ))
        
        self.helper.layout = layout.Layout(
            *layout_blocks
            )        

class MediationForm(ModelForm):
    class Meta:
        model = Museum
        fields = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'mediation_offer_%s' % lang_code,
                ]
    def __init__(self, *args, **kwargs):
        super(MediationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        
        layout_blocks = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            layout_blocks.append(layout.Fieldset(
                _("Mediation offer (%s)") % lang_name,
                'mediation_offer_%s' % lang_code,
                ))
        layout_blocks.append(bootstrap.FormActions(
            layout.Submit('reset', _('Reset'), css_class="btn-warning"),
            layout.Submit('submit', _('Save')),
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
            'address': {'_filled': True},
            'services_accessibility': {'_filled': True},
            'mediation': {'_filled': True},
            }
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['basic']['title_%s' % lang_code] = getattr(instance, 'title_%s' % lang_code)
            form_step_data['basic']['subtitle_%s' % lang_code] = getattr(instance, 'subtitle_%s' % lang_code)
            form_step_data['basic']['description_%s' % lang_code] = getattr(instance, 'description_%s' % lang_code)
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
            season_dict['tue_open'] = season.tue_open
            season_dict['tue_break_close'] = season.tue_break_close
            season_dict['tue_break_open'] = season.tue_break_open
            season_dict['tue_close'] = season.tue_close
            season_dict['wed_open'] = season.wed_open
            season_dict['wed_break_close'] = season.wed_break_close
            season_dict['wed_break_open'] = season.wed_break_open
            season_dict['wed_close'] = season.wed_close
            season_dict['thu_open'] = season.thu_open
            season_dict['thu_break_close'] = season.thu_break_close
            season_dict['thu_break_open'] = season.thu_break_open
            season_dict['thu_close'] = season.thu_close
            season_dict['fri_open'] = season.fri_open
            season_dict['fri_break_close'] = season.fri_break_close
            season_dict['fri_break_open'] = season.fri_break_open
            season_dict['fri_close'] = season.fri_close
            season_dict['sat_open'] = season.sat_open
            season_dict['sat_break_close'] = season.sat_break_close
            season_dict['sat_break_open'] = season.sat_break_open
            season_dict['sat_close'] = season.sat_close
            season_dict['sun_open'] = season.sun_open
            season_dict['sun_break_close'] = season.sun_break_close
            season_dict['sun_break_open'] = season.sun_break_open
            season_dict['sun_close'] = season.sun_close
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
        
        fields = ['street_address', 'street_address2', 'postal_code', 'district',
            'city', 'latitude', 'longitude',
            'phone', 'fax', 'email', 'website', 'twitter', 'facebook',
            'contact_name', 'contact_phone_country', 'contact_phone_area', 'contact_phone_number', 'contact_email',
            'post_street_address', 'post_street_address2', 'post_postal_code', 'post_city',
            ]
        for f in fields:
            form_step_data['address'][f] = getattr(instance, f)
        
        form_step_data['services_accessibility']['accessibility_options'] = instance.accessibility_options.all()
        form_step_data['services_accessibility']['service_shop'] = instance.service_shop
        form_step_data['services_accessibility']['service_books'] = instance.service_books
        form_step_data['services_accessibility']['service_restaurant'] = instance.service_restaurant
        form_step_data['services_accessibility']['service_cafe'] = instance.service_cafe
        form_step_data['services_accessibility']['service_library'] = instance.service_library
        form_step_data['services_accessibility']['service_archive'] = instance.service_archive
        form_step_data['services_accessibility']['service_studio'] = instance.service_studio
        form_step_data['services_accessibility']['service_online'] = instance.service_online
        form_step_data['services_accessibility']['service_diaper_changing_table'] = instance.service_diaper_changing_table
        form_step_data['services_accessibility']['service_birthdays'] = instance.service_birthdays
        form_step_data['services_accessibility']['service_rent'] = instance.service_rent
        form_step_data['services_accessibility']['service_other'] = instance.service_other
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['services_accessibility']['accessibility_%s' % lang_code] = getattr(instance, 'accessibility_%s' % lang_code)
            form_step_data['services_accessibility']['service_shop_info_%s' % lang_code] = getattr(instance, 'service_shop_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_books_info_%s' % lang_code] = getattr(instance, 'service_books_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_restaurant_info_%s' % lang_code] = getattr(instance, 'service_restaurant_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_cafe_info_%s' % lang_code] = getattr(instance, 'service_cafe_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_library_info_%s' % lang_code] = getattr(instance, 'service_library_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_archive_info_%s' % lang_code] = getattr(instance, 'service_archive_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_studio_info_%s' % lang_code] = getattr(instance, 'service_studio_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_online_info_%s' % lang_code] = getattr(instance, 'service_online_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_birthdays_info_%s' % lang_code] = getattr(instance, 'service_birthdays_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_rent_info_%s' % lang_code] = getattr(instance, 'service_rent_info_%s' % lang_code)
            form_step_data['services_accessibility']['service_other_info_%s' % lang_code] = getattr(instance, 'service_other_info_%s' % lang_code)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            form_step_data['mediation']['mediation_offer_%s' % lang_code] = getattr(instance, 'mediation_offer_%s' % lang_code)

    return form_step_data
    
def submit_step(current_step, form_steps, form_step_data, instance=None):
    return form_step_data

def save_data(form_steps, form_step_data, instance=None):
    if not instance:
        instance = Museum()

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'title_%s' % lang_code, form_step_data['basic']['title_%s' % lang_code])
        setattr(instance, 'subtitle_%s' % lang_code, form_step_data['basic']['subtitle_%s' % lang_code])
        setattr(instance, 'description_%s' % lang_code, form_step_data['basic']['description_%s' % lang_code])
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
    
    fields = ['street_address', 'street_address2', 'postal_code', 'district',
        'city', 'latitude', 'longitude',
        'phone', 'fax', 'email', 'website', 'twitter', 'facebook',
        'contact_name', 'contact_phone_country', 'contact_phone_area', 'contact_phone_number', 'contact_email',
        'post_street_address', 'post_street_address2', 'post_postal_code', 'post_city',
        ]
    for f in fields:
        setattr(instance, f, form_step_data['address'][f])
    
    
    instance.service_shop = form_step_data['services_accessibility']['service_shop']
    instance.service_books = form_step_data['services_accessibility']['service_books']
    instance.service_restaurant = form_step_data['services_accessibility']['service_restaurant']
    instance.service_cafe = form_step_data['services_accessibility']['service_cafe']
    instance.service_library = form_step_data['services_accessibility']['service_library']
    instance.service_archive = form_step_data['services_accessibility']['service_archive']
    instance.service_studio = form_step_data['services_accessibility']['service_studio']
    instance.service_online = form_step_data['services_accessibility']['service_online']
    instance.service_diaper_changing_table = form_step_data['services_accessibility']['service_diaper_changing_table']
    instance.service_birthdays = form_step_data['services_accessibility']['service_birthdays']
    instance.service_rent = form_step_data['services_accessibility']['service_rent'] 
    instance.service_other = form_step_data['services_accessibility']['service_other']
    
    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'accessibility_%s' % lang_code, form_step_data['services_accessibility']['accessibility_%s' % lang_code])
        setattr(instance, 'accessibility_%s' % lang_code, form_step_data['services_accessibility']['accessibility_%s' % lang_code])
        setattr(instance, 'service_shop_info_%s' % lang_code, form_step_data['services_accessibility']['service_shop_info_%s' % lang_code])
        setattr(instance, 'service_books_info_%s' % lang_code, form_step_data['services_accessibility']['service_books_info_%s' % lang_code]) 
        setattr(instance, 'service_restaurant_info_%s' % lang_code, form_step_data['services_accessibility']['service_restaurant_info_%s' % lang_code])
        setattr(instance, 'service_cafe_info_%s' % lang_code, form_step_data['services_accessibility']['service_cafe_info_%s' % lang_code])
        setattr(instance, 'service_library_info_%s' % lang_code, form_step_data['services_accessibility']['service_library_info_%s' % lang_code])
        setattr(instance, 'service_archive_info_%s' % lang_code, form_step_data['services_accessibility']['service_archive_info_%s' % lang_code])
        setattr(instance, 'service_studio_info_%s' % lang_code, form_step_data['services_accessibility']['service_studio_info_%s' % lang_code])
        setattr(instance, 'service_online_info_%s' % lang_code, form_step_data['services_accessibility']['service_online_info_%s' % lang_code])
        setattr(instance, 'service_birthdays_info_%s' % lang_code, form_step_data['services_accessibility']['service_birthdays_info_%s' % lang_code])
        setattr(instance, 'service_rent_info_%s' % lang_code, form_step_data['services_accessibility']['service_rent_info_%s' % lang_code])
        setattr(instance, 'service_other_info_%s' % lang_code, form_step_data['services_accessibility']['service_other_info_%s' % lang_code])

    for lang_code, lang_name in FRONTEND_LANGUAGES:
        setattr(instance, 'mediation_offer_%s' % lang_code, form_step_data['mediation']['mediation_offer_%s' % lang_code])

    instance.status = "published"
    instance.save()
    for cat in form_step_data['basic']['categories']:
        instance.categories.add(cat)
    for cat in form_step_data['services_accessibility']['accessibility_options']:
        instance.accessibility_options.add(cat)

    for season_dict in form_step_data['opening']['sets']['seasons']:
        season = Season(museum=instance)
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
        season.save()
        
    for special_opening_dict in form_step_data['opening']['sets']['special_openings']:
        special_opening = SpecialOpeningTime(museum=instance)
        special_opening.yyyy = special_opening_dict['yyyy'] 
        special_opening.mm = special_opening_dict['mm']
        special_opening.dd = special_opening_dict['dd']
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(special_opening, 'day_label_%s' % lang_code, special_opening_dict['day_label_%s' % lang_code])
        special_opening.is_closed = special_opening_dict['is_closed'] 
        special_opening.is_regular = special_opening_dict['is_regular'] 
        special_opening.opening = special_opening_dict['opening'] 
        special_opening.break_close = special_opening_dict['break_close'] 
        special_opening.break_open = special_opening_dict['break_open'] 
        special_opening.closing = special_opening_dict['closing']
        special_opening.save()

    form_steps['success_url'] = instance.get_url_path()

    return form_step_data

MUSEUM_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "museums/forms/basic_info_form.html",
        'form': BasicInfoForm,
    },
    'opening': {
        'title': _("Opening times"),
        'template': "museums/forms/opening_form.html",
        'form': OpeningForm, # dummy form
        'formsets': {
            'seasons': SeasonFormset,
            'special_openings': SpecialOpeningTimeFormset,
        }
    },
    'prices': {
        'title': _("Prices"),
        'template': "museums/forms/prices_form.html",
        'form': PricesForm,
    },
    'address': {
        'title': _("Address"),
        'template': "museums/forms/address_form.html",
        'form': AddressForm,
    },
    'services_accessibility': {
        'title': _("Services and Accessibility"),
        'template': "museums/forms/services_accessibility_form.html",
        'form': ServicesAccessibilityForm,
    },
    'mediation': {
        'title': _("Mediation"),
        'template': "museums/forms/mediation_form.html",
        'form': MediationForm,
    },
    'oninit': load_data,
    'onsubmit': submit_step,
    'onsave': save_data,
    'name': 'museum_registration',
    'default_path': ["basic", "opening", "prices", "address", "services_accessibility", "mediation"],
}

