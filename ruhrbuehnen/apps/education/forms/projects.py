# -*- coding: UTF-8 -*-
import os
import shutil
from datetime import datetime, time, timedelta
try:
    from django.utils.timezone import now as tz_now
except:
    tz_now = datetime.now

from django import forms
from django.forms.models import inlineformset_factory, formset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.db import models
from django.utils import timezone

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.middleware.threadlocals import get_current_user
from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from ruhrbuehnen.apps.locations.models import Location
from ruhrbuehnen.apps.education.models import Department
from ruhrbuehnen.apps.education.models import Project
from ruhrbuehnen.apps.education.models import ProjectTime
from ruhrbuehnen.apps.education.models import ProjectMember
from ruhrbuehnen.apps.education.models import ProjectImage
from ruhrbuehnen.apps.education.models import ProjectSocialMediaChannel
from ruhrbuehnen.apps.education.models import ProjectPDF
from ruhrbuehnen.apps.education.models import ProjectVideo
from ruhrbuehnen.apps.education.models import ProjectSponsor
from ruhrbuehnen.apps.people.models import Person

from jetson.apps.image_mods.models import FileManager

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()
                        ) - set(dict(FRONTEND_LANGUAGES).keys())

from ruhrbuehnen.utils.forms import PrimarySubmit
from ruhrbuehnen.utils.forms import SecondarySubmit
from ruhrbuehnen.utils.forms import InlineFormSet
from ruhrbuehnen.utils.forms import timestamp_str

import autocomplete_light

# translatable strings to collect
_(u"leave blank if you want to use the data from the department")


class BasicInfoForm(autocomplete_light.ModelForm):
    class Meta:
        model = Project
        autocomplete_fields = ('departments', )
        fields = [
            'departments',
            'location_title',
            'street_address',
            'street_address2',
            'postal_code',
            'city',
            'latitude',
            'longitude',
            'contact_department',
            'contact_name',
            'phone_country',
            'phone_area',
            'phone_number',
            'fax_country',
            'fax_area',
            'fax_number',
            'email',
            'website',
            'age_from',
            'age_till',
            'needs_teachers',
            'free_entrance',
            'tickets_website',
            'target_groups',
            'formats',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'participant_count_%s' % lang_code,
                'prices_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'participant_count_%s' % lang_code,
                'prices_%s' % lang_code,
            ]:
                self.fields[
                    f
                ].label += """ <span class="lang">%s</span>""" % lang_code.upper(
                )

        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()

        self.fields['target_groups'].widget = forms.CheckboxSelectMultiple()
        self.fields['target_groups'].help_text = ""
        self.fields['target_groups'].empty_label = None

        self.fields['formats'].widget = forms.CheckboxSelectMultiple()
        self.fields['formats'].help_text = ""
        self.fields['formats'].empty_label = None

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []

        fieldset_content = [
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('title_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('subtitle_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                layout.Div(
                    layout.Field('departments'),
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12",
                ),
                css_class="row-md"
            )
        ]  # collect multilingual divs into one list...

        layout_blocks.append(
            layout.Fieldset(
                _("Basic Info"),
                css_class="fieldset-basic-info",
                *fieldset_content  # ... then pass them to a fieldset
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Project Office Address"),
                layout.HTML(
                    """{% load i18n %}<div class="subtitle">{% trans "leave blank if you want to use the data from the department" %}</div>"""
                ),
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
                        layout.HTML(
                            """{% load i18n %}
                        <div class="dyn_set_map">
                            <label>{% trans "Project" %}</label>
                            <div class="map_canvas">
                            </div>
                            <div class="form-actions">
                                <input type="button" class="locate_address btn btn-primary" value="{% trans "Relocate on map" %}" />&zwnj;
                                <!--<input type="button" class="remove_geo btn btn-primary" value="{% trans "Remove from map" %}"/>&zwnj;-->
                            </div>
                            <div class="map_projects">
                            </div>
                        </div>
                    """
                        ),
                        "latitude",
                        "longitude",
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-md",
                ),
                css_class="fieldset-where",
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Contact"),
                layout.HTML(
                    """{% load i18n %}<div class="subtitle">{% trans "leave blank if you want to use the data from the department" %}</div>"""
                ),
                layout.Row(
                    layout.Div(
                        'contact_department',
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        'contact_name',
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-md"
                ),
                layout.Row(
                    layout.Div(
                        'email',
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        layout.Field('website', placeholder="http://"),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-md"
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(
                            '{% load i18n %}<div><label class="with">{% trans "Phone" %}</label></div>'
                        ),
                        layout.Row(
                            layout.Div(
                                'phone_country',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'phone_area',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'phone_number',
                                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                            ),
                            css_class="row-xs"
                        ),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    layout.Div(
                        layout.HTML(
                            '{% load i18n %}<div><label class="with">{% trans "Fax" %}</label></div>'
                        ),
                        layout.Row(
                            layout.Div(
                                'fax_country',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'fax_area',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'fax_number',
                                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                            ),
                            css_class="row-xs"
                        ),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                    ),
                    css_class="row-md"
                ),
                css_class="fieldset-other-contact-info"
            )
        )

        fieldset_content = [
            layout.Row(
                layout.Div(
                    layout.Field('age_from'),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                layout.Div(
                    layout.Field('age_till'),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                css_class="row-md"
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('participant_count_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                layout.Div(
                    layout.Field('needs_teachers'),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                layout.Div(
                    layout.Field('free_entrance'),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                ),
                css_class="row-md"
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('prices_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                layout.Div(
                    layout.Field('tickets_website', placeholder="http://"),
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12",
                ),
                css_class="row-md"
            )
        ]  # collect multilingual divs into one list...

        layout_blocks.append(
            layout.Fieldset(
                _("Dates and Times"),
                layout.HTML(
                    """{% load crispy_forms_tags i18n %}
            {{ formsets.times.management_form }}
            <div id="times">
                {% for form in formsets.times.forms %}
                    <div class="time formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="times_empty_form" class="time formset-form" style="display: none">
                {% with formsets.times.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """
                ),
                css_id="times_fieldset",
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Details"),
                css_class="fieldset-basic-info",
                *fieldset_content  # ... then pass them to a fieldset
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Target Groups"),
                "target_groups",
                css_class="fieldset-services",
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Formats"),
                "formats",
                css_class="fieldset-services",
            )
        )

        if self.instance and self.instance.pk:
            layout_blocks.append(
                bootstrap.FormActions(
                    PrimarySubmit('submit', _('Next')),
                    SecondarySubmit('save_and_close', _('Save and close')),
                    SecondarySubmit('reset', _('Cancel')),
                )
            )
        else:
            layout_blocks.append(
                bootstrap.FormActions(
                    PrimarySubmit('submit', _('Next')),
                    SecondarySubmit('reset', _('Cancel')),
                )
            )

        self.helper.layout = layout.Layout(*layout_blocks)


class ProjectTimeForm(forms.ModelForm):
    start_date = forms.DateField(
        label=_("Start date"),
        required=True,
        input_formats=('%Y-%m-%d', ),
        widget=forms.DateInput(format='%Y-%m-%d'),
    )
    start_time = forms.TimeField(
        label=_("Start time"),
        required=True,
    )
    end_date = forms.DateField(
        label=_("End date"),
        required=False,
        input_formats=('%Y-%m-%d', ),
        widget=forms.DateInput(format='%Y-%m-%d'),
    )
    end_time = forms.TimeField(
        label=_("End time"),
        required=False,
    )

    class Meta:
        model = ProjectTime
        fields = ['id']

    def __init__(self, *args, **kwargs):
        super(ProjectTimeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = [
            layout.Row(
                layout.Div(
                    "start_date",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "start_time",
                    "id",
                    "DELETE",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md"
            ),
            layout.Row(
                layout.Div(
                    "end_date", css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    "end_time", css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md"
            )
        ]

        self.helper.layout = layout.Layout(*layout_blocks)


ProjectTimeFormset = inlineformset_factory(
    Project, ProjectTime, form=ProjectTimeForm, formset=InlineFormSet, extra=0
)


class DescriptionForm(autocomplete_light.ModelForm):
    class Meta:
        model = Project
        fields = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'special_conditions_%s' % lang_code,
                'remarks_%s' % lang_code,
                'cooperation_%s' % lang_code,
                'supporters_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(DescriptionForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'description_%s' % lang_code,
                'special_conditions_%s' % lang_code,
                'remarks_%s' % lang_code,
                'cooperation_%s' % lang_code,
                'supporters_%s' % lang_code,
            ]:
                self.fields[
                    f
                ].label += """ <span class="lang">%s</span>""" % lang_code.upper(
                )

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = [
            layout.Fieldset(
                _("Members"),
                layout.HTML(
                    """{% load crispy_forms_tags i18n %}
            {{ formsets.members.management_form }}
            <div id="members">
                {% for form in formsets.members.forms %}
                    <div class="member formset-form">
                        {% crispy form %}
                    </div>
                {% endfor %}
            </div>
            <!-- used by javascript -->
            <div id="members_empty_form" class="member formset-form" style="display: none">
                {% with formsets.members.empty_form as form %}
                    {% crispy form %}
                {% endwith %}
            </div>
            """
                ),
                css_id="members_fieldset",
            )
        ]

        fieldset_content = [
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('description_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('special_conditions_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('remarks_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('cooperation_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('supporters_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            )
        ]  # collect multilingual divs into one list...
        layout_blocks.append(
            layout.Fieldset(
                _("Description"),
                css_class="fieldset-basic-info",
                *fieldset_content  # ... then pass them to a fieldset
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Social media"),
                layout.HTML(
                    """{% load crispy_forms_tags i18n %}
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
            """
                ),
                css_id="social_channels_fieldset",
            )
        )

        layout_blocks.append(
            layout.Fieldset(
                _("Supported by"),
                layout.HTML(
                    """{% load crispy_forms_tags i18n %}
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
            """
                ),
                css_id="sponsors_fieldset",
            )
        )

        if self.instance and self.instance.pk:
            layout_blocks.append(
                bootstrap.FormActions(
                    PrimarySubmit('submit', _('Next')),
                    SecondarySubmit('save_and_close', _('Save and close')),
                    SecondarySubmit('reset', _('Cancel')),
                )
            )
        else:
            layout_blocks.append(
                bootstrap.FormActions(
                    PrimarySubmit('submit', _('Next')),
                    SecondarySubmit('reset', _('Cancel')),
                )
            )

        self.helper.layout = layout.Layout(*layout_blocks)


class ProjectMemberForm(autocomplete_light.ModelForm):
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
        model = ProjectMember
        autocomplete_fields = ('person', )
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProjectMemberForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'function_%s' % lang_code,
            ]:
                self.fields[
                    f
                ].label += """ <span class="lang">%s</span>""" % lang_code.upper(
                )

        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label = ugettext(
            'Choose person'
        ) + ' (' + ugettext('or'
                           ) + ' <a href="" class="enter_person">' + ugettext(
                               'click here to enter a new person'
                           ) + '</a>)'
        self.fields['first_name'].label += ' (' + ugettext(
            'or'
        ) + ' <a href="" class="choose_person">' + ugettext(
            'choose a person from the database'
        ) + '</a>)'

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = [
            layout.Row(
                layout.Div(
                    "person",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm choosing_person"
            ),
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
        ]

        fieldset_content = [
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('function_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            )
        ]  # collect multilingual divs into one list...
        layout_blocks.append(
            layout.Fieldset(
                _("Function"),
                css_class="fieldset-basic-info",
                *fieldset_content  # ... then pass them to a fieldset
            )
        )
        layout_blocks.append(
            layout.Fieldset(
                _("Contact"),
                layout.Row(
                    layout.Div(
                        'email',
                        css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                    ),
                    css_class="row-md"
                ),
                layout.Row(
                    layout.Div(
                        layout.HTML(
                            '{% load i18n %}<div><label class="with">{% trans "Phone" %}</label></div>'
                        ),
                        layout.Row(
                            layout.Div(
                                'phone_country',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'phone_area',
                                css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                            ),
                            layout.Div(
                                'phone_number',
                                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                            ),
                            css_class="row-xs"
                        ),
                        css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                    ),
                    css_class="row-md"
                ),
                css_class="fieldset-contact-info"
            )
        )
        layout_blocks.append(
            layout.Div("sort_order", "id", "DELETE", css_class="hidden")
        )

        self.helper.layout = layout.Layout(*layout_blocks)

    def clean(self):
        cleaned = super(ProjectMemberForm, self).clean()
        if not cleaned.get('last_name') and not cleaned.get('person'):
            msg = _("Choose a person from the database or enter his name.")
            self._errors["person"] = self.error_class([msg])
            self._errors["last_name"] = self.error_class(
                [_('This field is required.')]
            )
            if not cleaned.get('first_name'):
                self._errors["first_name"] = self.error_class(
                    [_('This field is required.')]
                )
            del cleaned['last_name']
            del cleaned['person']
        return cleaned


ProjectMemberFormset = inlineformset_factory(
    Project,
    ProjectMember,
    form=ProjectMemberForm,
    formset=InlineFormSet,
    extra=0
)


class SocialMediaChannelForm(forms.ModelForm):
    class Meta:
        model = ProjectSocialMediaChannel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SocialMediaChannelForm, self).__init__(*args, **kwargs)

        self.fields['channel_type'].help_text = ""

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_blocks = [
            layout.Row(
                layout.Div(
                    "channel_type",
                    css_class="col-xs-12 col-sm-4 col-md-4 col-lg-4"
                ),
                layout.Div(
                    layout.Field("url", placeholder="http://"),
                    "DELETE",
                    css_class="input-group col-xs-12 col-sm-8 col-md-8 col-lg-8"
                ),
                css_class="row-sm"
            )
        ]

        self.helper.layout = layout.Layout(*layout_blocks)


SocialMediaChannelFormset = inlineformset_factory(
    Project,
    ProjectSocialMediaChannel,
    form=SocialMediaChannelForm,
    formset=InlineFormSet,
    extra=0
)


class ProjectSponsorForm(autocomplete_light.ModelForm):
    media_file_path = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = ProjectSponsor
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProjectSponsorForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
            ]:
                self.fields[
                    f
                ].label += """ <span class="lang">%s</span>""" % lang_code.upper(
                )

        self.helper = FormHelper()
        self.helper.form_tag = False

        fieldset_content = [
            layout.HTML(
                u"""{% load i18n base_tags image_modifications %}
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
            """
            ),
            layout.Row(
                css_class="row-md",
                *[
                    layout.Div(
                        layout.Field('title_%s' % lang_code),
                        css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                    ) for lang_code, lang_name in FRONTEND_LANGUAGES
                ]
            ),
            layout.Row(
                layout.Div(
                    "media_file_path",
                    layout.Field("website", placeholder="http://"),
                    "id",
                    "DELETE",
                    css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-sm"
            )
        ]  # collect multilingual divs into one list...

        self.helper.layout = layout.Layout(*fieldset_content)

    def clean_media_file_path(self):
        data = self.cleaned_data['media_file_path']
        if ".." in data:
            raise forms.ValidationError(
                _("Double dots are not allowed in the file name.")
            )
        return data


ProjectSponsorFormset = inlineformset_factory(
    Project,
    ProjectSponsor,
    form=ProjectSponsorForm,
    formset=InlineFormSet,
    extra=0
)


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = []

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        if self.instance and self.instance.pk:
            layout_blocks.append(
                bootstrap.FormActions(
                    PrimarySubmit('save_and_close', _('Save and close')),
                    SecondarySubmit('reset', _('Cancel')),
                )
            )
        else:
            layout_blocks.append(
                bootstrap.FormActions(
                    PrimarySubmit('submit', _('Save')),
                    SecondarySubmit('reset', _('Cancel')),
                )
            )
        self.helper.layout = layout.Layout(*layout_blocks)


def load_data(instance=None, request=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {
                '_filled': True,
                'sets': {
                    'times': [],
                }
            },
            'description':
                {
                    '_filled': True,
                    'sets': {
                        'members': [],
                        'social': [],
                        'sponsors': [],
                    }
                },
            'gallery': {
                '_filled': True
            },
            '_pk': instance.pk,
        }

        ### The "basic" step ###

        fields = [
            'location_title',
            'street_address',
            'street_address2',
            'postal_code',
            'city',
            'latitude',
            'longitude',
            'contact_department',
            'contact_name',
            'phone_country',
            'phone_area',
            'phone_number',
            'fax_country',
            'fax_area',
            'fax_number',
            'email',
            'website',
            'age_from',
            'age_till',
            'needs_teachers',
            'free_entrance',
            'tickets_website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'participant_count_%s' % lang_code,
                'prices_%s' % lang_code,
            ]
        for fname in fields:
            form_step_data['basic'][fname] = getattr(instance, fname)

        form_step_data['basic']['departments'] = instance.departments.all()
        form_step_data['basic']['target_groups'] = instance.target_groups.all()
        form_step_data['basic']['formats'] = instance.formats.all()

        for project_time in instance.projecttime_set.all():
            time_dict = {'id': project_time.id}
            local_start = timezone.localtime(project_time.start)
            time_dict['start_date'] = local_start.date()
            time_dict['start_time'] = local_start.time()
            if project_time.end is not None:
                local_end = timezone.localtime(project_time.end)
                time_dict['end_date'] = local_end.date()
                time_dict['end_time'] = local_end.time()

            form_step_data['basic']['sets']['times'].append(time_dict)

        ### The "description" step ###

        fields = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'special_conditions_%s' % lang_code,
                'remarks_%s' % lang_code,
                'cooperation_%s' % lang_code,
                'supporters_%s' % lang_code,
            ]
        for fname in fields:
            form_step_data['description'][fname] = getattr(instance, fname)

        for member in instance.projectmember_set.all():
            member_dict = {}
            fields = [
                'id', 'person', 'phone_country', 'phone_area', 'phone_number',
                'email', 'sort_order'
            ]
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                fields += [
                    'function_%s' % lang_code,
                ]
            for fname in fields:
                member_dict[fname] = getattr(member, fname)
            form_step_data['description']['sets']['members'].append(member_dict)

        for social_media_channel in instance.projectsocialmediachannel_set.all(
        ):
            social_media_channel_dict = {
                'channel_type': social_media_channel.channel_type,
                'url': social_media_channel.url
            }
            form_step_data['description']['sets']['social'].append(
                social_media_channel_dict
            )

        for sponsor in instance.projectsponsor_set.all():
            sponsor_dict = {'id': sponsor.pk, 'website': sponsor.website}
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                sponsor_dict['title_%s' % lang_code
                            ] = getattr(sponsor, 'title_%s' % lang_code)
            form_step_data['description']['sets']['sponsors'].append(
                sponsor_dict
            )
    else:
        form_step_data = {
            'basic': {
                '_filled': False,
                'sets': {}
            },
        }
        own_locations = Location.objects.owned_by(get_current_user())
        own_departments = Department.objects.filter(location__in=own_locations)
        if own_locations:
            form_step_data['basic']['departments'] = own_departments

    return form_step_data


def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Project.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Project()

        fields = [
            'location_title',
            'street_address',
            'street_address2',
            'postal_code',
            'city',
            'latitude',
            'longitude',
            'contact_department',
            'contact_name',
            'phone_country',
            'phone_area',
            'phone_number',
            'fax_country',
            'fax_area',
            'fax_number',
            'email',
            'website',
            'age_from',
            'age_till',
            'needs_teachers',
            'free_entrance',
            'tickets_website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'participant_count_%s' % lang_code,
                'prices_%s' % lang_code,
            ]
        for fname in fields:
            setattr(instance, fname, form_step_data[current_step][fname])

        if not instance.slug:
            instance.slug = get_unique_value(
                Project,
                better_slugify(instance.title_de),
                instance_pk=instance.pk
            )

        instance.save()

        instance.departments.clear()
        for cat in form_step_data['basic']['departments']:
            instance.departments.add(cat)

        instance.target_groups.clear()
        for cat in form_step_data['basic']['target_groups']:
            instance.target_groups.add(cat)

        instance.formats.clear()
        for cat in form_step_data['basic']['formats']:
            instance.formats.add(cat)

        if not instance.get_owners():
            current_user = get_current_user()
            if not current_user.is_superuser:
                instance.set_owner(current_user)
            # add other owners from the organizers relationship
            for department in instance.departments.all():
                for owner in department.get_owners():
                    instance.set_owner(owner)

        # save times
        time_ids_to_keep = []
        for time_dict in form_step_data['basic']['sets']['times']:
            if time_dict['id']:
                try:
                    project_time = ProjectTime.objects.get(
                        pk=time_dict['id'],
                        project=instance,
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                project_time = ProjectTime(project=instance)
            if time_dict['start_date'] and time_dict['start_time']:
                project_time.start = datetime.combine(
                    time_dict['start_date'], time_dict['start_time']
                )
            if time_dict['end_date']:
                if not time_dict['end_time']:
                    time_dict['end_time'] = time(0, 0)
                project_time.end = datetime.combine(
                    time_dict['end_date'], time_dict['end_time']
                )
            project_time.save()
            time_ids_to_keep.append(project_time.pk)
        instance.projecttime_set.exclude(pk__in=time_ids_to_keep).delete()

        form_step_data['_pk'] = instance.pk

    if current_step == "description":
        if "_pk" in form_step_data:
            instance = Project.objects.get(pk=form_step_data['_pk'])
        else:
            return

        fields = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'special_conditions_%s' % lang_code,
                'remarks_%s' % lang_code,
                'cooperation_%s' % lang_code,
                'supporters_%s' % lang_code,
            ]
        for fname in fields:
            setattr(instance, fname, form_step_data['description'][fname])

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(instance, 'description_%s_markup_type' % lang_code, 'pt')
            setattr(
                instance, 'special_conditions_%s_markup_type' % lang_code, 'pt'
            )
            setattr(instance, 'remarks_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'cooperation_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'supporters_%s_markup_type' % lang_code, 'pt')

        instance.save()

        # save members
        fields = [
            'phone_country', 'phone_area', 'phone_number', 'email', 'sort_order'
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'function_%s' % lang_code,
            ]
        member_ids_to_keep = []
        for member_dict in form_step_data['description']['sets']['members']:
            if member_dict['person']:
                person = Person.objects.get(pk=member_dict['person'])
            else:
                person = Person()
                person.first_name = member_dict['first_name']
                person.last_name = member_dict['last_name']
                person.save()

                member_dict['person'] = person.pk
                del member_dict['first_name']
                del member_dict['last_name']
            if member_dict['id']:
                try:
                    member = ProjectMember.objects.get(
                        pk=member_dict['id'],
                        project=instance,
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                member = ProjectMember(project=instance)
            for fname in fields:
                setattr(member, fname, member_dict[fname])
            member.person = person
            member.save()
            member_ids_to_keep.append(member.pk)
        instance.projectmember_set.exclude(pk__in=member_ids_to_keep).delete()

        # save social media channels
        instance.projectsocialmediachannel_set.all().delete()
        for social_dict in form_step_data['description']['sets']['social']:
            social = ProjectSocialMediaChannel(project=instance)
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
                    sponsor = ProjectSponsor.objects.get(
                        pk=sponsor_dict['id'],
                        project=instance,
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                sponsor = ProjectSponsor(project=instance)
            if sponsor_dict['media_file_path'] and sponsor.image:
                # delete the old file
                try:
                    FileManager.delete_file(sponsor.image.path)
                except OSError:
                    pass
            rel_dir = "education/projects/{}/sponsors/".format(instance.slug)
            if sponsor_dict['media_file_path']:
                tmp_path = sponsor_dict['media_file_path']
                abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

                fname, fext = os.path.splitext(tmp_path)
                filename = timestamp_str() + fext
                dest_path = "".join((rel_dir, filename))
                FileManager.path_exists(
                    os.path.join(settings.MEDIA_ROOT, rel_dir)
                )
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
        instance.projectsponsor_set.exclude(pk__in=sponsor_ids_to_keep).delete()

    return form_step_data


def set_extra_context(
    current_step, form_steps, form_step_data, instance=None, request=None
):
    if "_pk" in form_step_data:
        return {'project': Project.objects.get(pk=form_step_data['_pk'])}
    return {}


def save_data(form_steps, form_step_data, instance=None):
    # probably a dummy callback, because the data is already saved after each step
    is_new = not instance
    if not instance:
        if '_pk' in form_step_data:
            instance = Project.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Project()

    return form_step_data


def cancel_editing(request, instance=None):
    return redirect("dashboard")


PROJECT_FORM_STEPS = {
    'basic':
        {
            'title': _("Educational Project"),
            'template': "education/projects/forms/basic_info_form.html",
            'form': BasicInfoForm,
            'formsets': {
                'times': ProjectTimeFormset,
            }
        },
    'description':
        {
            'title': _("Description"),
            'template': "education/projects/forms/description_form.html",
            'form': DescriptionForm,
            'formsets':
                {
                    'members': ProjectMemberFormset,
                    'social': SocialMediaChannelFormset,
                    'sponsors': ProjectSponsorFormset,
                }
        },
    'gallery':
        {
            'title': _("Media"),
            'template': "education/projects/forms/gallery_form.html",
            'form': GalleryForm,  # dummy form
        },
    'oninit':
        load_data,
    'on_set_extra_context':
        set_extra_context,
    'onsubmit':
        submit_step,
    'onsave':
        save_data,
    'onreset':
        cancel_editing,
    'success_url':
        "/dashboard/",
    'general_error_message':
        _(
            "There are errors in this form. Please correct them and try to save again."
        ),
    'name':
        'project_editing',
    'default_path': ["basic", "description", "gallery"],
}


class ProjectDuplicateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title_%s' % lang_code
            for lang_code, lang_name in FRONTEND_LANGUAGES
        ]

    def __init__(self, *args, **kwargs):
        super(ProjectDuplicateForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
            ]:
                self.fields[
                    f
                ].label += """ <span class="lang">%s</span>""" % lang_code.upper(
                )

        self.helper = FormHelper()
        self.helper.form_action = "."
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("New Project Title"),
                layout.Row(
                    css_class="row-md",
                    *[
                        layout.Div(
                            layout.Field('title_%s' % lang_code),
                            css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
                        ) for lang_code, lang_name in FRONTEND_LANGUAGES
                    ]
                ),
                css_class="fieldset-basic-info",
            ),
            bootstrap.FormActions(
                PrimarySubmit('submit', _('Duplicate')),
                css_class="hidden",
            ),
        )
