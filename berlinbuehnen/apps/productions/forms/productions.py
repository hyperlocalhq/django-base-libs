# -*- coding: UTF-8 -*-
import os
import shutil
from datetime import datetime

from django import forms
from django.forms.models import inlineformset_factory, formset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.db import models

from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.middleware.threadlocals import get_current_user

from jetson.apps.image_mods.models import FileManager

from berlinbuehnen.apps.productions.models import Production, ProductionCategory, ProductionLeadership, ProductionAuthorship, ProductionInvolvement, LanguageAndSubtitles, ProductionSocialMediaChannel, ProductionSponsor
from berlinbuehnen.apps.people.models import Person, InvolvementType, AuthorshipType
from berlinbuehnen.apps.locations.models import Location

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from berlinbuehnen.utils.forms import PrimarySubmit
from berlinbuehnen.utils.forms import SecondarySubmit
from berlinbuehnen.utils.forms import InlineFormSet
from berlinbuehnen.utils.forms import ModelMultipleChoiceTreeField
from berlinbuehnen.utils.forms import timestamp_str

import autocomplete_light

# translatable strings to collect
_(u"Minimal size is 100 × 100 px.")

class BasicInfoForm(autocomplete_light.ModelForm):
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        required=True,
        queryset=ProductionCategory.objects.all(),
    )

    class Meta:
        model = Production
        autocomplete_fields = ('in_program_of', 'play_locations', 'play_stages', 'festivals', )
        fields = [
            'festivals', 'in_program_of', 'ensembles', 'play_locations', 'play_stages', 'organizers', 'in_cooperation_with',
            'location_title', 'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
            'categories', 'classiccard', 'show_among_others', 'no_overwriting',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'prefix_%s' % lang_code,
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'original_%s' % lang_code,
                'website_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'prefix_%s' % lang_code,
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'original_%s' % lang_code,
                'website_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['festivals'].label = _("Belongs to festival")

        self.fields['play_locations'].help_text = _('Choose only when differs from the "In the programm of".')

        self.fields['in_program_of'].label += ' (' + ugettext('or') + ' <a href="" class="enter_location">' + ugettext('enter a new location below') + '</a>)'
        self.fields['play_locations'].label = ugettext('Theaters') + ' (' + ugettext('or') + ' <a href="" class="enter_location">' + ugettext('enter a new location below') + '</a>)'
        self.fields['play_stages'].label = ugettext('Stages')

        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()

        if self.instance and not self.instance.import_source:
            self.fields['no_overwriting'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []
        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('title_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('prefix_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('subtitle_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('original_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('website_%s' % lang_code, placeholder="http://"),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        layout_blocks.append(layout.Fieldset(
            _("Title"),
            css_class="fieldset-basic-info",
            *fieldset_content  # ... then pass them to a fieldset
        ))

        layout_blocks.append(layout.Fieldset(
            _("Venue"),
            layout.Row(
                layout.Div(
                    "in_program_of",
                    "play_locations",
                    "play_stages",
                    "ensembles",
                    "organizers",
                    "in_cooperation_with",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-venue",
        ))
        layout_blocks.append(layout.Fieldset(
            _("Performance location"),
            layout.HTML("""{% load i18n %}
            <p class="help-block">{% trans 'Enter the address when the location differs from the "In the programme of" and is not found under "Performance location".' %}</p>
            """),
            layout.Row(
                layout.Div(
                    "location_title",
                    "street_address",
                    "street_address2",
                    "postal_code",
                    "city",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.HTML("""{% load i18n %}
                        <div class="dyn_set_map">
                            <label>{% trans "Location" %}</label>
                            <div class="map_canvas">
                            </div>
                            <div class="form-actions">
                                <input type="button" class="locate_address btn btn-primary" value="{% trans "Relocate on map" %}" />&zwnj;
                                <!--<input type="button" class="remove_geo btn btn-primary" value="{% trans "Remove from map" %}"/>&zwnj;-->
                            </div>
                            <div class="map_locations">
                            </div>
                        </div>
                    """),
                    "latitude",
                    "longitude",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md",
            ),
            css_class="fieldset-where hidden",
        ))
        
        layout_blocks.append(layout.Fieldset(
            _('Festivals'),
            layout.Row(
                layout.Div(
                    "festivals",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-categories",
        ))

        layout_blocks.append(layout.Fieldset(
            _('Categories<span class="asteriskField">*</span>'),
            layout.HTML("""{% load i18n %}<p class="help-block">{% trans "Select one or more categories." %}</p>"""),
            layout.Row(
                layout.Div(
                    layout.Div(layout.Field("categories", template="utils/checkboxselectmultipletree.html")),
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12 tree"
                ),
            ),
            css_class="fieldset-categories",
        ))

        layout_blocks.append(layout.Fieldset(
            _('ClassicCard'),
            layout.Row(
                layout.Div(
                    "classiccard",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-classiccard",
        ))
        layout_blocks.append(layout.Fieldset(
            _('Visibility'),
            layout.Row(
                layout.Div(
                    "show_among_others",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-categories",
        ))
        if self.instance and self.instance.import_source:
            layout_blocks.append(layout.Fieldset(
                _('Import settings'),
                layout.Row(
                    layout.Div(
                        "no_overwriting",
                        css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                    ),
                ),
                css_class="fieldset-categories",
            ))
        else:
            layout_blocks.append("no_overwriting")


        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
            ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def clean(self):
        cleaned = super(BasicInfoForm, self).clean()
        if not cleaned.get('in_program_of') and not cleaned.get('location_title'):
            msg = _("Choose a location from the database or enter another location's title and address below.")
            self._errors["in_program_of"] = self.error_class([msg])
            del cleaned['in_program_of']
            del cleaned['location_title']
        return cleaned


class DescriptionForm(autocomplete_light.ModelForm):
    class Meta:
        model = Production
        #autocomplete_fields = ('related_productions',)
        fields = [
            'language_and_subtitles',
            #'related_productions',
            'free_entrance', 'price_from', 'price_till', 'tickets_website',
            'characteristics', 'age_from', 'age_till', 'edu_offer_website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
                'work_info_%s' % lang_code,
                'contents_%s' % lang_code,
                'press_text_%s' % lang_code,
                'credits_%s' % lang_code,
                'concert_program_%s' % lang_code,
                'supporting_program_%s' % lang_code,
                'remarks_%s' % lang_code,
                'price_information_%s' % lang_code,
                'other_characteristics_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(DescriptionForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
                'work_info_%s' % lang_code,
                'contents_%s' % lang_code,
                'press_text_%s' % lang_code,
                'credits_%s' % lang_code,
                'concert_program_%s' % lang_code,
                'supporting_program_%s' % lang_code,
                'remarks_%s' % lang_code,
                'price_information_%s' % lang_code,
                'other_characteristics_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['characteristics'].widget = forms.CheckboxSelectMultiple()
        self.fields['characteristics'].help_text = u""

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Staff"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            <p class="help-block">{% trans "The staff will be shown in the repertoire of the production." %}</p>
            {{ formsets.leaderships.management_form }}
            <div id="leaderships">
                {% for form in formsets.leaderships.forms %}
                    <div class="leadership formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="leaderships_empty_form" class="leadership formset-form" style="display: none">
                {% with formsets.leaderships.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="leaderships_fieldset",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Authors/Composers"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.authorships.management_form }}
            <div id="authorships">
                {% for form in formsets.authorships.forms %}
                    <div class="authorship formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="authorships_empty_form" class="authorship formset-form" style="display: none">
                {% with formsets.authorships.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="authorships_fieldset",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Cast"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.involvements.management_form }}
            <div id="involvements">
                {% for form in formsets.involvements.forms %}
                    <div class="involvement formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="involvements_empty_form" class="involvement formset-form" style="display: none">
                {% with formsets.involvements.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="involvements_fieldset",
        ))

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('description_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('teaser_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('work_info_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('contents_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('press_text_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('credits_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('concert_program_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('supporting_program_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('remarks_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            layout.Div(
                'language_and_subtitles',
                #'related_productions',
                css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12",
            ),
            css_class="row-md",
        ))
        layout_blocks.append(layout.Fieldset(
            _("Description"),
            css_class="fieldset-basic-info",
            *fieldset_content  # ... then pass them to a fieldset
        ))

        fieldset_content = []
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('price_information_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))

        layout_blocks.append(layout.Fieldset(
            _("Tickets"),
            layout.Row(
                layout.Div(
                    layout.Field('price_from', lang="en-150"),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                layout.Div(
                    layout.Field('price_till', lang="en-150"),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                css_class="row-md",
            ),
            layout.Row(
                layout.Div(
                    "free_entrance",
                    layout.Field("tickets_website", placeholder="http://"),
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-tickets",
            *fieldset_content
        ))

        layout_blocks.append(layout.Fieldset(
            _("Other Characteristics"),
            layout.Row(
                layout.Div(
                    "characteristics",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            layout.Row(
                css_class="row-md",
                *[layout.Div(
                    layout.Field('other_characteristics_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            ),
            layout.Row(
                layout.Div(
                    layout.Field('age_from'),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                layout.Div(
                    layout.Field('age_till'),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                css_class="row-md",
            ),
            layout.Row(
                layout.Div(
                    layout.Field("edu_offer_website", placeholder="http://"),
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-characteristics",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Social media for this production"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.social.management_form }}
            <div id="social">
                {% for form in formsets.social.forms %}
                    <div class="social formset-form tabular-inline">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="social_empty_form" class="social formset-form tabular-inline" style="display: none">
                {% with formsets.social.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="social_channels_fieldset",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Sponsors"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
            {{ formsets.sponsors.management_form }}
            <div id="sponsors">
                {% for form in formsets.sponsors.forms %}
                    <div class="sponsor formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="sponsors_empty_form" class="sponsor formset-form" style="display: none">
                {% with formsets.sponsors.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """),
            css_id="sponsors_fieldset",
        ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('reset', _('Cancel')),
            ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )


class ProductionLeadershipForm(autocomplete_light.ModelForm):
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        max_length=255,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        max_length=255,
    )

    class Meta:
        model = ProductionLeadership
        autocomplete_fields = ('person',)
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductionLeadershipForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'function_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['imported_sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label = ugettext('Choose person') + ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('click here to enter a new person') + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext('or') + ' <a href="" class="choose_person">' + ugettext('choose a person from the database') + '</a>)'

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "person",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm choosing_person"
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "first_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "last_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm entering_person hidden"
            )
        )
        layout_blocks.append(
            layout.Div(
                "sort_order",
                "imported_sort_order",
                "id",
                "DELETE",
                css_class="hidden"
            )
        )
        layout_blocks.append(
            layout.Row(
                css_class="row-sm",
                *[layout.Div(
                    layout.Field('function_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def clean(self):
        cleaned = super(ProductionLeadershipForm, self).clean()
        if not cleaned.get('last_name') and not cleaned.get('person'):
            msg = _("Choose a person from the database or enter his name.")
            self._errors["person"] = self.error_class([msg])
            self._errors["last_name"] = self.error_class([_('This field is required.')])
            if not cleaned.get('first_name'):
                self._errors["first_name"] = self.error_class([_('This field is required.')])
            del cleaned['last_name']
            del cleaned['person']
        return cleaned


ProductionLeadershipFormset = inlineformset_factory(Production, ProductionLeadership, form=ProductionLeadershipForm, formset=InlineFormSet, extra=0)


class ProductionAuthorshipForm(autocomplete_light.ModelForm):
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        max_length=255,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        max_length=255,
    )

    class Meta:
        model = ProductionAuthorship
        autocomplete_fields = ('person',)
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductionAuthorshipForm, self).__init__(*args, **kwargs)

        self.fields['authorship_type'].label = _("Function")
        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['imported_sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label = ugettext('Choose person') + ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('click here to enter a new person') + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext('or') + ' <a href="" class="choose_person">' + ugettext('choose a person from the database') + '</a>)'
        self.fields['work_title'].help_text = _("When differs from the title of the production.")

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "person", css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm choosing_person"
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "first_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "last_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm entering_person hidden"
            )
        )
        layout_blocks.append(
            layout.Div(
                "sort_order",
                "imported_sort_order",
                "id",
                "DELETE",
                css_class="hidden"
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "authorship_type",
                    "work_title",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm"
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def clean(self):
        cleaned = super(ProductionAuthorshipForm, self).clean()
        if not cleaned.get('last_name') and not cleaned.get('person'):
            msg = _("Choose a person from the database or enter his name.")
            self._errors["person"] = self.error_class([msg])
            self._errors["last_name"] = self.error_class([_('This field is required.')])
            if not cleaned.get('first_name'):
                self._errors["first_name"] = self.error_class([_('This field is required.')])
            del cleaned['last_name']
            del cleaned['person']
        return cleaned


ProductionAuthorshipFormset = inlineformset_factory(Production, ProductionAuthorship, form=ProductionAuthorshipForm, formset=InlineFormSet, extra=0)


class ProductionInvolvementForm(autocomplete_light.ModelForm):
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        max_length=255,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        max_length=255,
    )
    selection = forms.ChoiceField(
        label=_("Select one option"),
        required=True,
        choices=(
            ('type', _("Choose function")),
            ('role', _("Enter role")),
            ('instrument', _("Enter instrument")),
        ),
        widget=forms.RadioSelect(),
    )

    class Meta:
        model = ProductionInvolvement
        autocomplete_fields = ('person',)
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductionInvolvementForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'involvement_role_%s' % lang_code,
                'involvement_instrument_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'another_type_%s' % lang_code,
            ]:
                self.fields[f].label = ugettext("Function") + (""" <span class="lang">%s</span>""" % lang_code.upper()) + ' (' + ugettext('or') + ' <a href="" class="choose_type">' + ugettext('choose a function from the database') + '</a>)'

        self.fields['involvement_type'].label = ugettext("Function") + ' (' + ugettext('or') + ' <a href="" class="enter_type">' + ugettext('enter a new function') + '</a>)'
        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['imported_sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label = ugettext('Choose person') + ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('click here to enter a new person') + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext('or') + ' <a href="" class="choose_person">' + ugettext('choose a person from the database') + '</a>)'

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "person",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm choosing_person"
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "first_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "last_name",
                    css_class="col-xs-12 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-sm entering_person hidden"
            )
        )
        layout_blocks.append(
            layout.Div(
                "sort_order",
                "imported_sort_order",
                "id",
                "DELETE",
                css_class="hidden",
            )
        )
        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "selection",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm"
            )
        )
        layout_blocks.append(
            layout.Div(
                layout.Row(
                    layout.Div(
                        "involvement_type",
                        css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                    ),
                    css_class="row-sm choosing_type"
                ),
                layout.Row(
                    css_class="row-sm hidden entering_type",
                    *[layout.Div(
                        layout.Field('another_type_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES]
                ),
                css_class="type_selection hidden",
            )
        )
        layout_blocks.append(
            layout.Row(
                css_class="row-sm hidden",
                *[layout.Div(
                    layout.Field('involvement_role_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            )
        )
        layout_blocks.append(
            layout.Row(
                css_class="row-sm hidden",
                *[layout.Div(
                    layout.Field('involvement_instrument_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def clean(self):
        cleaned = super(ProductionInvolvementForm, self).clean()
        if not cleaned.get('last_name') and not cleaned.get('person'):
            msg = _("Choose a person from the database or enter his name.")
            self._errors["person"] = self.error_class([msg])
            self._errors["last_name"] = self.error_class([_('This field is required.')])
            if not cleaned.get('first_name'):
                self._errors["first_name"] = self.error_class([_('This field is required.')])
            del cleaned['last_name']
            del cleaned['person']
        return cleaned


ProductionInvolvementFormset = inlineformset_factory(Production, ProductionInvolvement, form=ProductionInvolvementForm, formset=InlineFormSet, extra=0)


class SocialMediaChannelForm(forms.ModelForm):
    class Meta:
        model = ProductionSocialMediaChannel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SocialMediaChannelForm, self).__init__(*args, **kwargs)

        self.fields['channel_type'].help_text = ""

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "channel_type", css_class="col-xs-12 col-sm-4 col-md-4 col-lg-4"
                ),
                layout.Div(
                    layout.Field("url", placeholder="http://"),
                    "DELETE",
                    css_class="input-group col-xs-12 col-sm-8 col-md-8 col-lg-8"
                ),
                css_class="row-sm"
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

SocialMediaChannelFormset = inlineformset_factory(Production, ProductionSocialMediaChannel, form=SocialMediaChannelForm, formset=InlineFormSet, extra=0)


class ProductionSponsorForm(autocomplete_light.ModelForm):
    media_file_path = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = ProductionSponsor
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductionSponsorForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_tag = False

        fieldset_content = []  # collect multilingual divs into one list...

        fieldset_content.append(
            layout.HTML(u"""{% load i18n base_tags image_modifications %}
            <div class="row row-md">
                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                    <div class="image_preview">
                        {% if form.instance.image %}
                            <img class="img-responsive" src="{{ MEDIA_URL }}{{ form.instance.image|modified_path:"medium" }}?now={% now "YmdHis" %}" alt="" />
                        {% endif %}
                    </div>
                    <div class="image_uploader">
                        <noscript>
                            <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                        </noscript>
                    </div>
                    <p class="image_help_text help-block">{% trans "Available formats are JPG, GIF, and PNG." %}<br/>{% trans "Minimal size is 100 × 100 px." %}<br/><br/></p>
                </div>
            </div>
            """)
        )

        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('title_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            layout.Div(
                "media_file_path",
                layout.Field("website", placeholder="http://"),
                "id",
                "DELETE",
                css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
            ),
            css_class="row-sm"
        ))

        self.helper.layout = layout.Layout(
            *fieldset_content
        )

    def clean_media_file_path(self):
        data = self.cleaned_data['media_file_path']
        if ".." in data:
            raise forms.ValidationError(_("Double dots are not allowed in the file name."))
        return data

ProductionSponsorFormset = inlineformset_factory(Production, ProductionSponsor, form=ProductionSponsorForm, formset=InlineFormSet, extra=0)


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = []

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        layout_blocks.append(bootstrap.FormActions(
            PrimarySubmit('submit', _('Next')),
            SecondarySubmit('save_and_close', _('Save and close')),
            SecondarySubmit('reset', _('Cancel')),
        ))
        self.helper.layout = layout.Layout(
            *layout_blocks
        )


class EventsForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = []

    def __init__(self, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(bootstrap.FormActions(
            PrimarySubmit('save_and_close', _('Save and close')),
            SecondarySubmit('reset', _('Cancel')),
        ))


def load_data(instance=None, request=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True, 'sets': {}},
            'description': {'_filled': True, 'sets': {'leaderships': [], 'authorships': [], 'involvements': [], 'social': [], 'sponsors': []}},
            'gallery': {'_filled': True},
            'events': {'_filled': True},
            '_pk': instance.pk,
        }

        ### The "basic" step ###

        fields = [
            'ensembles', 'organizers', 'in_cooperation_with',
            'location_title', 'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
            'classiccard', 'show_among_others', 'no_overwriting',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'prefix_%s' % lang_code,
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'original_%s' % lang_code,
                'website_%s' % lang_code,
            ]
        for fname in fields:
            form_step_data['basic'][fname] = getattr(instance, fname)

        form_step_data['basic']['festivals'] = instance.festivals.all()
        form_step_data['basic']['in_program_of'] = instance.in_program_of.all()
        form_step_data['basic']['play_locations'] = instance.play_locations.all()
        form_step_data['basic']['play_stages'] = instance.play_stages.all()
        form_step_data['basic']['categories'] = instance.categories.all()

        ### The "description" step ###

        fields = [
            'language_and_subtitles',
            'free_entrance', 'price_from', 'price_till', 'tickets_website',
            'age_from', 'age_till', 'edu_offer_website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
                'work_info_%s' % lang_code,
                'contents_%s' % lang_code,
                'press_text_%s' % lang_code,
                'credits_%s' % lang_code,
                'concert_program_%s' % lang_code,
                'supporting_program_%s' % lang_code,
                'remarks_%s' % lang_code,
                'price_information_%s' % lang_code,
                'other_characteristics_%s' % lang_code,
            ]
        for fname in fields:
            form_step_data['description'][fname] = getattr(instance, fname)

        #form_step_data['description']['related_productions'] = instance.related_productions.all()
        form_step_data['description']['characteristics'] = instance.characteristics.all()

        for leadership in instance.productionleadership_set.order_by('sort_order'):
            leadership_dict = {}
            leadership_dict['id'] = leadership.pk
            leadership_dict['person'] = leadership.person
            leadership_dict['sort_order'] = leadership.sort_order
            leadership_dict['imported_sort_order'] = leadership.imported_sort_order
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                leadership_dict['function_%s' % lang_code] = getattr(leadership, 'function_%s' % lang_code)
            form_step_data['description']['sets']['leaderships'].append(leadership_dict)

        for authorship in instance.productionauthorship_set.order_by('sort_order'):
            authorship_dict = {}
            authorship_dict['id'] = authorship.pk
            authorship_dict['person'] = authorship.person
            authorship_dict['sort_order'] = authorship.sort_order
            authorship_dict['imported_sort_order'] = authorship.imported_sort_order
            authorship_dict['authorship_type'] = authorship.authorship_type
            form_step_data['description']['sets']['authorships'].append(authorship_dict)

        for involvement in instance.productioninvolvement_set.order_by('sort_order'):
            involvement_dict = {}
            involvement_dict['id'] = involvement.pk
            involvement_dict['person'] = involvement.person
            involvement_dict['sort_order'] = involvement.sort_order
            involvement_dict['imported_sort_order'] = involvement.imported_sort_order
            involvement_dict['involvement_type'] = involvement.involvement_type
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                involvement_dict['another_type_%s' % lang_code] = getattr(involvement, 'another_type_%s' % lang_code)
                involvement_dict['involvement_role_%s' % lang_code] = getattr(involvement, 'involvement_role_%s' % lang_code)
                involvement_dict['involvement_instrument_%s' % lang_code] = getattr(involvement, 'involvement_instrument_%s' % lang_code)
            form_step_data['description']['sets']['involvements'].append(involvement_dict)

        for social_media_channel in instance.productionsocialmediachannel_set.all():
            social_media_channel_dict = {}
            social_media_channel_dict['channel_type'] = social_media_channel.channel_type
            social_media_channel_dict['url'] = social_media_channel.url
            form_step_data['description']['sets']['social'].append(social_media_channel_dict)

        for sponsor in instance.productionsponsor_set.all():
            sponsor_dict = {}
            sponsor_dict['id'] = sponsor.pk
            sponsor_dict['website'] = sponsor.website
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                sponsor_dict['title_%s' % lang_code] = getattr(sponsor, 'title_%s' % lang_code)
            form_step_data['description']['sets']['sponsors'].append(sponsor_dict)

    else:
        form_step_data = {
            'basic': {'_filled': False, 'sets': {}},
        }
        own_locations = Location.objects.owned_by(get_current_user())
        if own_locations:
            form_step_data['basic']['in_program_of'] = own_locations

    return form_step_data


def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Production.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Production()

        fields = [
            'ensembles', 'organizers', 'in_cooperation_with',
            'location_title', 'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
            'classiccard', 'show_among_others', 'no_overwriting'
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'prefix_%s' % lang_code,
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'original_%s' % lang_code,
                'website_%s' % lang_code,
            ]
        for fname in fields:
            setattr(instance, fname, form_step_data[current_step][fname])

        if not instance.slug:
            instance.slug = get_unique_value(Production, better_slugify(instance.title_de) or u"production", instance_pk=instance.pk)

        # Don't trigger saving of the search document for the instance and each m2m relationship. We'll do that later.
        instance._skip_search_document_update = True

        instance.save()

        instance.festivals.clear()
        for cat in form_step_data['basic']['festivals']:
            instance.festivals.add(cat)

        instance.in_program_of.clear()
        for cat in form_step_data['basic']['in_program_of']:
            instance.in_program_of.add(cat)

        instance.play_locations.clear()
        for cat in form_step_data['basic']['play_locations']:
            instance.play_locations.add(cat)

        instance.play_stages.clear()
        for cat in form_step_data['basic']['play_stages']:
            instance.play_stages.add(cat)

        instance.categories.clear()
        for cat in form_step_data['basic']['categories']:
            instance.categories.add(cat)
        instance.fix_categories()

        if not instance.get_owners():
            current_user = get_current_user()
            if not current_user.is_superuser:
                instance.set_owner(get_current_user())
            # add other owners from the in_program_of relationship
            for in_program_of in instance.in_program_of.all():
                for owner in in_program_of.get_owners():
                    instance.set_owner(owner)

        # Now the time has come! Trigger saving of the search document.
        instance._skip_search_document_update = False
        models.signals.post_save.send(type(instance), instance=instance, created=False)

        form_step_data['_pk'] = instance.pk

    if current_step == "description":
        if "_pk" in form_step_data:
            instance = Production.objects.get(pk=form_step_data['_pk'])
        else:
            return

        fields = [
            'free_entrance', 'price_from', 'price_till', 'tickets_website',
            'age_from', 'age_till', 'edu_offer_website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
                'work_info_%s' % lang_code,
                'contents_%s' % lang_code,
                'press_text_%s' % lang_code,
                'credits_%s' % lang_code,
                'concert_program_%s' % lang_code,
                'supporting_program_%s' % lang_code,
                'remarks_%s' % lang_code,
                'price_information_%s' % lang_code,
                'other_characteristics_%s' % lang_code,
            ]
        for fname in fields:
            setattr(instance, fname, form_step_data[current_step][fname])

        language_and_subtitles = form_step_data[current_step]['language_and_subtitles']
        instance.language_and_subtitles = None
        if language_and_subtitles:
            if isinstance(language_and_subtitles, LanguageAndSubtitles):
                instance.language_and_subtitles = language_and_subtitles
            elif isinstance(language_and_subtitles, int):
                # TODO: find if this case occurs with the new jetson for Django 1.8 at all
                instance.language_and_subtitles = LanguageAndSubtitles.objects.get(pk=language_and_subtitles)

        # set markup types to plain text
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(instance, 'description_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'teaser_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'work_info_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'contents_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'press_text_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'credits_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'concert_program_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'supporting_program_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'remarks_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'price_information_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'other_characteristics_%s_markup_type' % lang_code, 'pt')

        instance.save()

        #instance.related_productions.clear()
        #for cat in form_step_data['description']['related_productions']:
        #    instance.related_productions.add(cat)

        instance.characteristics.clear()
        for cat in form_step_data['description']['characteristics']:
            instance.characteristics.add(cat)

        # save leaderships
        fields = [
            'sort_order',
            'imported_sort_order',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'function_%s' % lang_code,
            ]
        leadership_ids_to_keep = []
        for leadership_dict in form_step_data['description']['sets']['leaderships']:
            if leadership_dict['person']:
                person = Person.objects.get(pk=leadership_dict['person'])
            else:
                person = Person()
                person.first_name = leadership_dict['first_name']
                person.last_name = leadership_dict['last_name']
                person.save()

                leadership_dict['person'] = person.pk
                del leadership_dict['first_name']
                del leadership_dict['last_name']
            if leadership_dict['id']:
                try:
                    leadership = ProductionLeadership.objects.get(
                        pk=leadership_dict['id'],
                        production=instance,
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                leadership = ProductionLeadership(production=instance)
            for fname in fields:
                setattr(leadership, fname, leadership_dict[fname])
            leadership.person = person
            leadership.save()
            leadership_ids_to_keep.append(leadership.pk)
        instance.productionleadership_set.exclude(pk__in=leadership_ids_to_keep).delete()

        # save authorships
        fields = [
            'sort_order',
            'imported_sort_order',
        ]
        authorship_ids_to_keep = []
        for authorship_dict in form_step_data['description']['sets']['authorships']:
            authorship_type = None
            if authorship_dict['authorship_type']:
                authorship_type = AuthorshipType.objects.get(pk=authorship_dict['authorship_type'])
            if authorship_dict['person']:
                person = Person.objects.get(pk=authorship_dict['person'])
            else:
                person = Person()
                person.first_name = authorship_dict['first_name']
                person.last_name = authorship_dict['last_name']
                person.save()

                authorship_dict['person'] = person.pk
                del authorship_dict['first_name']
                del authorship_dict['last_name']
            if authorship_dict['id']:
                try:
                    authorship = ProductionAuthorship.objects.get(
                        pk=authorship_dict['id'],
                        production=instance,
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                authorship = ProductionAuthorship(production=instance)
            for fname in fields:
                setattr(authorship, fname, authorship_dict[fname])
            authorship.person = person
            authorship.authorship_type = authorship_type
            authorship.save()
            authorship_ids_to_keep.append(authorship.pk)
        instance.productionauthorship_set.exclude(pk__in=authorship_ids_to_keep).delete()

        # save involvements
        fields = [
            'sort_order',
            'imported_sort_order',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'another_type_%s' % lang_code,
                'involvement_role_%s' % lang_code,
                'involvement_instrument_%s' % lang_code,
            ]
        involvement_ids_to_keep = []
        for involvement_dict in form_step_data['description']['sets']['involvements']:
            involvement_type = None
            if involvement_dict['involvement_type']:
                involvement_type = InvolvementType.objects.get(pk=involvement_dict['involvement_type'])
            if involvement_dict['person']:
                person = Person.objects.get(pk=involvement_dict['person'])
            else:
                person = Person()
                person.first_name = involvement_dict['first_name']
                person.last_name = involvement_dict['last_name']
                person.save()

                involvement_dict['person'] = person.pk
                del involvement_dict['first_name']
                del involvement_dict['last_name']
            if involvement_dict['id']:
                try:
                    involvement = ProductionInvolvement.objects.get(
                        pk=involvement_dict['id'],
                        production=instance,
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                involvement = ProductionInvolvement(production=instance)
            for fname in fields:
                setattr(involvement, fname, involvement_dict[fname])
            involvement.person = person
            involvement.involvement_type = involvement_type
            involvement.save()
            involvement_ids_to_keep.append(involvement.pk)
        instance.productioninvolvement_set.exclude(pk__in=involvement_ids_to_keep).delete()

        # save social media channels
        instance.productionsocialmediachannel_set.all().delete()
        for social_dict in form_step_data['description']['sets']['social']:
            social = ProductionSocialMediaChannel(production=instance)
            social.channel_type = social_dict['channel_type']
            social.url = social_dict['url']
            social.save()

        # save sponsors
        fields = [
            'website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
            ]

        sponsor_ids_to_keep = []
        for sponsor_dict in form_step_data['description']['sets']['sponsors']:
            if sponsor_dict['id']:
                try:
                    sponsor = ProductionSponsor.objects.get(
                        pk=sponsor_dict['id'],
                        production=instance,
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                sponsor = ProductionSponsor(production=instance)
            if sponsor_dict['media_file_path'] and sponsor.image:
                # delete the old file
                try:
                    FileManager.delete_file(sponsor.image.path)
                except OSError:
                    pass
            rel_dir = "productions/{}/sponsors/".format(instance.slug)
            if sponsor_dict['media_file_path']:
                tmp_path = sponsor_dict['media_file_path']
                abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

                fname, fext = os.path.splitext(tmp_path)
                filename = timestamp_str() + fext
                dest_path = "".join((rel_dir, filename))
                FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
                abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)

                shutil.copy2(abs_tmp_path, abs_dest_path)

                os.remove(abs_tmp_path)
                sponsor.image = dest_path
                sponsor_dict['media_file_path'] = u""

            for fname in fields:
                setattr(sponsor, fname, sponsor_dict[fname])
            sponsor.save()
            sponsor_dict['id'] = sponsor.pk
            sponsor_ids_to_keep.append(sponsor.pk)
        instance.productionsponsor_set.exclude(pk__in=sponsor_ids_to_keep).delete()
    if current_step == "gallery":
        if "_pk" in form_step_data:
            instance = Production.objects.get(pk=form_step_data['_pk'])
        else:
            return
        # trigger saving to the Elasticsearch index
        models.signals.post_save.send(type(instance), instance=instance, created=False)
    return form_step_data


def set_extra_context(current_step, form_steps, form_step_data, instance=None, request=None):
    if "_pk" in form_step_data:
        production = Production.objects.get(pk=form_step_data['_pk'])
        return {
            'production': production,
            'events': production.event_set.exclude(event_status="trashed").order_by("-start_date", "-start_time"),
        }
    return {}


def save_data(form_steps, form_step_data, instance=None):
    # probably a dummy callback, because the data is already saved after each step
    is_new = not instance
    if not instance:
        if '_pk' in form_step_data:
            instance = Production.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Production()

    return form_step_data


def cancel_editing(request, instance=None):
    return redirect("dashboard")


PRODUCTION_FORM_STEPS = {
    'basic': {
        'title': _("Production"),
        'template': "productions/forms/basic_info_form.html",
        'form': BasicInfoForm,
    },
    'description': {
        'title': _("Description"),
        'template': "productions/forms/description_form.html",
        'form': DescriptionForm,
        'formsets': {
            'leaderships': ProductionLeadershipFormset,
            'authorships': ProductionAuthorshipFormset,
            'involvements': ProductionInvolvementFormset,
            'social': SocialMediaChannelFormset,
            'sponsors': ProductionSponsorFormset,
        }
    },
    'gallery': {
        'title': _("Media"),
        'template': "productions/forms/gallery_form.html",
        'form': GalleryForm,  # dummy form
    },
    'events': {
        'title': _("Events"),
        'template': "productions/forms/events_form.html",
        'form': EventsForm,  # dummy form
    },
    'oninit': load_data,
    'on_set_extra_context': set_extra_context,
    'onsubmit': submit_step,
    'onsave': save_data,
    'onreset': cancel_editing,
    'success_url': "/dashboard/",
    'general_error_message': _("There are errors in this form. Please correct them and try to save again."),
    'name': 'production_editing',
    'default_path': ["basic", "description", "gallery", "events"],
}


class ProductionDuplicateForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['title_%s' % lang_code for lang_code, lang_name in FRONTEND_LANGUAGES]

    def __init__(self, *args, **kwargs):
        super(ProductionDuplicateForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = "."
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("New Production Title"),
                layout.Row(
                    css_class="row-md",
                    *[layout.Div(
                        layout.Field('title_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES]
                ),
                css_class="fieldset-basic-info",
            ),
            bootstrap.FormActions(
                PrimarySubmit('submit', _('Duplicate')),
                css_class="hidden",
            ),
        )
