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

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from jetson.apps.image_mods.models import FileManager

from berlinbuehnen.apps.sponsors.models import Sponsor
from berlinbuehnen.apps.productions.models import Production, Event, ProductionCategory, ProductionLeadership, ProductionAuthorship, ProductionInvolvement, LanguageAndSubtitles
from berlinbuehnen.apps.people.models import Person, InvolvementType, AuthorshipType

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from berlinbuehnen.utils.forms import PrimarySubmit
from berlinbuehnen.utils.forms import SecondarySubmit
from berlinbuehnen.utils.forms import InlineFormSet
from berlinbuehnen.utils.forms import ModelMultipleChoiceTreeField

import autocomplete_light


class BasicInfoForm(autocomplete_light.ModelForm):
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        required=False,
        queryset=ProductionCategory.objects.all(),
    )

    class Meta:
        model = Production
        autocomplete_fields = ('in_program_of', 'ensembles', 'play_locations', 'play_stages', 'organizers', 'in_cooperation_with')
        fields = [
            'website',
            'in_program_of', 'ensembles', 'play_locations', 'play_stages', 'organizers', 'in_cooperation_with',
            'categories',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'prefix_%s' % lang_code,
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'original_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'prefix_%s' % lang_code,
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'original_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []
        fieldset_content = []  # collect multilingual divs into one list...
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
                layout.Field('title_%s' % lang_code),
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
            layout.Div(
                layout.Field('website'),
                css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12",
            ),
            css_class="row-md",
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
                    "ensembles",
                    "play_locations",
                    "play_stages",
                    "organizers",
                    "in_cooperation_with",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-venue",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Categories"),
            layout.Row(
                layout.Div(
                    layout.Div(layout.Field("categories", template="utils/checkboxselectmultipletree.html")),
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            css_class="fieldset-categories",
        ))

        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Next')),
                SecondarySubmit('save_and_close', _('Close')),
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


class DescriptionForm(autocomplete_light.ModelForm):
    class Meta:
        model = Production
        autocomplete_fields = ('festivals', 'related_productions',)
        fields = [
            'festivals', 'language_and_subtitles', 'related_productions',
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
                'concert_programm_%s' % lang_code,
                'supporting_programm_%s' % lang_code,
                'remarks_%s' % lang_code,
                'duration_text_%s' % lang_code,
                'subtitles_text_%s' % lang_code,
                'age_text_%s' % lang_code,
                'price_information_%s' % lang_code,
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
                'concert_programm_%s' % lang_code,
                'supporting_programm_%s' % lang_code,
                'remarks_%s' % lang_code,
                'duration_text_%s' % lang_code,
                'subtitles_text_%s' % lang_code,
                'age_text_%s' % lang_code,
                'price_information_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['characteristics'].widget = forms.CheckboxSelectMultiple()
        self.fields['characteristics'].help_text = u""

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Leaders"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
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
            _("Authors"),
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
            _("Other involved people"),
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
                layout.Field('concert_programm_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('supporting_programm_%s' % lang_code),
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
            css_class="row-md",
            *[layout.Div(
                layout.Field('duration_text_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('subtitles_text_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('age_text_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            layout.Div(
                'festivals',
                'language_and_subtitles',
                'related_productions',
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
                    layout.Field('price_from'),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                layout.Div(
                    layout.Field('price_till'),
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
                SecondarySubmit('save_and_close', _('Close')),
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

    def __init__(self, *args, **kwargs):
        super(ProductionLeadershipForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'function_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label += ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('enter a new person') + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext('or') + ' <a href="" class="choose_person">' + ugettext('choose a person from the database') + '</a>)'

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "person",
                    "sort_order",
                    "id",
                    "DELETE",
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

    def __init__(self, *args, **kwargs):
        super(ProductionAuthorshipForm, self).__init__(*args, **kwargs)

        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label += ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('enter a new person') + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext('or') + ' <a href="" class="choose_person">' + ugettext('choose a person from the database') + '</a>)'

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
            layout.Row(
                layout.Div(
                    "authorship_type",
                    "sort_order",
                    "id",
                    "DELETE",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm"
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

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

    class Meta:
        model = ProductionInvolvement
        autocomplete_fields = ('person',)

    def __init__(self, *args, **kwargs):
        super(ProductionInvolvementForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'involvement_role_%s' % lang_code,
                'involvement_instrument_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label += ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('enter a new person') + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext('or') + ' <a href="" class="choose_person">' + ugettext('choose a person from the database') + '</a>)'

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = []

        layout_blocks.append(
            layout.Row(
                layout.Div(
                    "person",
                    "sort_order",
                    "id",
                    "DELETE",
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
            layout.Row(
                layout.Div(
                    "involvement_type",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm"
            )
        )
        layout_blocks.append(
            layout.Row(
                css_class="row-sm",
                *[layout.Div(
                    layout.Field('involvement_role_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            )
        )
        layout_blocks.append(
            layout.Row(
                css_class="row-sm",
                *[layout.Div(
                    layout.Field('involvement_instrument_%s' % lang_code),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ) for lang_code, lang_name in FRONTEND_LANGUAGES]
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

ProductionInvolvementFormset = inlineformset_factory(Production, ProductionInvolvement, form=ProductionInvolvementForm, formset=InlineFormSet, extra=0)


class SponsorForm(autocomplete_light.ModelForm):
    id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )
    media_file_path = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = Sponsor

    def __init__(self, *args, **kwargs):
        super(SponsorForm, self).__init__(*args, **kwargs)

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
                    <p class="image_help_text help-block">{% trans "Available formats are JPG, GIF, and PNG. Minimal size is 100 × 100 px. Optimal size is 1000 × 350 px (min)." %}</p>
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

SponsorFormset = formset_factory(form=SponsorForm, extra=0, can_delete=True)


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
            SecondarySubmit('save_and_close', _('Close')),
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
            PrimarySubmit('save_and_close', _('Close')),
            SecondarySubmit('reset', _('Cancel')),
        ))


def load_data(instance=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True, 'sets': {'social': []}},
            'description': {'_filled': True, 'sets': {'leaderships': [], 'authorships': [], 'involvements': [], 'sponsors': []}},
            'gallery': {'_filled': True},
            'events': {'_filled': True},
            '_pk': instance.pk,
        }
        fields = [
            'website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'prefix_%s' % lang_code,
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'original_%s' % lang_code,
            ]
        for fname in fields:
            form_step_data['basic'][fname] = getattr(instance, fname)

        form_step_data['basic']['in_program_of'] = instance.in_program_of.all()
        form_step_data['basic']['ensembles'] = instance.ensembles.all()
        form_step_data['basic']['play_locations'] = instance.play_locations.all()
        form_step_data['basic']['play_stages'] = instance.play_stages.all()
        form_step_data['basic']['organizers'] = instance.organizers.all()
        form_step_data['basic']['in_cooperation_with'] = instance.in_cooperation_with.all()
        form_step_data['basic']['categories'] = instance.categories.all()

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
                'concert_programm_%s' % lang_code,
                'supporting_programm_%s' % lang_code,
                'remarks_%s' % lang_code,
                'duration_text_%s' % lang_code,
                'subtitles_text_%s' % lang_code,
                'age_text_%s' % lang_code,
                'price_information_%s' % lang_code,
            ]
        for fname in fields:
            form_step_data['description'][fname] = getattr(instance, fname)

        form_step_data['description']['festivals'] = instance.festivals.all()
        form_step_data['description']['related_productions'] = instance.related_productions.all()
        form_step_data['description']['characteristics'] = instance.characteristics.all()

        for leadership in instance.productionleadership_set.all():
            leadership_dict = {}
            leadership_dict['id'] = leadership.pk
            leadership_dict['person'] = leadership.person
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                leadership_dict['function_%s' % lang_code] = getattr(leadership, 'function_%s' % lang_code)
            form_step_data['description']['sets']['leaderships'].append(leadership_dict)

        for authorship in instance.productionauthorship_set.all():
            authorship_dict = {}
            authorship_dict['id'] = authorship.pk
            authorship_dict['person'] = authorship.person
            authorship_dict['authorship_type'] = authorship.authorship_type
            form_step_data['description']['sets']['authorships'].append(authorship_dict)

        for involvement in instance.productioninvolvement_set.all():
            involvement_dict = {}
            involvement_dict['id'] = involvement.pk
            involvement_dict['person'] = involvement.person
            involvement_dict['involvement_type'] = involvement.involvement_type
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                involvement_dict['involvement_role_%s' % lang_code] = getattr(involvement, 'involvement_role_%s' % lang_code)
                involvement_dict['involvement_instrument_%s' % lang_code] = getattr(involvement, 'involvement_instrument_%s' % lang_code)
            form_step_data['description']['sets']['involvements'].append(involvement_dict)

        for sponsor in instance.sponsors.all():
            sponsor_dict = {}
            sponsor_dict['id'] = sponsor.pk
            sponsor_dict['website'] = sponsor.website
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                sponsor_dict['title_%s' % lang_code] = getattr(sponsor, 'title_%s' % lang_code)
            form_step_data['description']['sets']['sponsors'].append(sponsor_dict)

    return form_step_data

def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Production.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Production()

        fields = [
            'website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'prefix_%s' % lang_code,
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'original_%s' % lang_code,
            ]
        for fname in fields:
            setattr(instance, fname, form_step_data[current_step][fname])

        instance.save()

        instance.in_program_of.clear()
        for cat in form_step_data['basic']['in_program_of']:
            instance.in_program_of.add(cat)

        instance.ensembles.clear()
        for cat in form_step_data['basic']['ensembles']:
            instance.ensembles.add(cat)

        instance.play_locations.clear()
        for cat in form_step_data['basic']['play_locations']:
            instance.play_locations.add(cat)

        instance.play_stages.clear()
        for cat in form_step_data['basic']['play_stages']:
            instance.play_stages.add(cat)

        instance.organizers.clear()
        for cat in form_step_data['basic']['organizers']:
            instance.organizers.add(cat)

        instance.in_cooperation_with.clear()
        for cat in form_step_data['basic']['in_cooperation_with']:
            instance.in_cooperation_with.add(cat)

        instance.categories.clear()
        for cat in form_step_data['basic']['categories']:
            instance.categories.add(cat)

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
                'concert_programm_%s' % lang_code,
                'supporting_programm_%s' % lang_code,
                'remarks_%s' % lang_code,
                'duration_text_%s' % lang_code,
                'subtitles_text_%s' % lang_code,
                'age_text_%s' % lang_code,
                'price_information_%s' % lang_code,
            ]
        for fname in fields:
            setattr(instance, fname, form_step_data[current_step][fname])

        if form_step_data[current_step]['language_and_subtitles']:
            instance.language_and_subtitles = LanguageAndSubtitles.objects.get(pk=form_step_data[current_step]['language_and_subtitles'])

        # set markup types to plain text
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(instance, 'description_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'teaser_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'work_info_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'contents_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'press_text_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'credits_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'concert_programm_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'supporting_programm_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'remarks_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'price_information_%s_markup_type' % lang_code, 'pt')

        instance.save()

        instance.festivals.clear()
        for cat in form_step_data['description']['festivals']:
            instance.festivals.add(cat)

        instance.related_productions.clear()
        for cat in form_step_data['description']['related_productions']:
            instance.related_productions.add(cat)

        instance.characteristics.clear()
        for cat in form_step_data['description']['characteristics']:
            instance.characteristics.add(cat)

        # save leaderships
        fields = [
            'sort_order',
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
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    setattr(person, 'leadership_function_%s' % lang_code, leadership_dict['function_%s' % lang_code])
                person.save()
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
                person.authorship_type = authorship_type
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    setattr(person, 'leadership_function_%s' % lang_code, authorship_dict['function_%s' % lang_code])
                person.save()
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
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
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
                person.involvement_type = involvement_type
                for lang_code, lang_name in FRONTEND_LANGUAGES:
                    setattr(person, 'involvement_role_%s' % lang_code, involvement_dict['involvement_role_%s' % lang_code])
                    setattr(person, 'involvement_instrument_%s' % lang_code, involvement_dict['involvement_instrument_%s' % lang_code])
                person.save()
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

        # save sponsors
        fields = [
            'website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
            ]
        instance.sponsors.clear()
        for sponsor_dict in form_step_data['description']['sets']['sponsors']:
            if sponsor_dict['id']:
                try:
                    sponsor = Sponsor.objects.get(
                        pk=sponsor_dict['id'],
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                sponsor = Sponsor()
            if sponsor_dict['media_file_path'] and sponsor.image:
                # delete the old file
                try:
                    FileManager.delete_file(sponsor.image.path)
                except OSError:
                    pass
            rel_dir = "sponsors/"
            if sponsor_dict['media_file_path']:
                tmp_path = sponsor_dict['media_file_path']
                abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

                fname, fext = os.path.splitext(tmp_path)
                filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
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
            instance.sponsors.add(sponsor)

    return form_step_data


def set_extra_context(current_step, form_steps, form_step_data, instance=None):
    if "_pk" in form_step_data:
        return {'location': Production.objects.get(pk=form_step_data['_pk'])}
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


def cancel_editing(request):
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
            'sponsors': SponsorFormset,
        }
    },
    'gallery': {
        'title': _("Images"),
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
