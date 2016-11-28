# -*- coding: UTF-8 -*-
import os
import shutil
from datetime import datetime
try:
    from django.utils.timezone import now as tz_now
except:
    tz_now = datetime.now

from django import forms
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.db import models

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.middleware.threadlocals import get_current_user
from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from jetson.apps.image_mods.models import FileManager

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

import autocomplete_light

from berlinbuehnen.utils.forms import PrimarySubmit
from berlinbuehnen.utils.forms import SecondarySubmit
from berlinbuehnen.utils.forms import InlineFormSet

from berlinbuehnen.apps.people.models import Person
from berlinbuehnen.apps.locations.models import Location
from berlinbuehnen.apps.education.models import Department
from berlinbuehnen.apps.education.models import SocialMediaChannel
from berlinbuehnen.apps.education.models import DepartmentMember


# translatable strings to collect
_(u"leave blank if you want to use the data from the location")

class BasicInfoForm(autocomplete_light.ModelForm):

    class Meta:
        model = Department
        autocomplete_fields = ('location',)
        fields = [
            'location',
            'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
            'contact_name',
            'phone_country', 'phone_area', 'phone_number',
            'fax_country', 'fax_area', 'fax_number',
            'email', 'website',
            'districts',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)
        
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget = forms.HiddenInput()

        self.fields['districts'].widget = forms.CheckboxSelectMultiple()
        self.fields['districts'].help_text = ""
        self.fields['districts'].empty_label = None

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
            layout.Div(
                layout.Field('location'),
                css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12",
            ),
            css_class="row-md"
        ))

        layout_blocks.append(layout.Fieldset(
            _("Basic Info"),
            css_class="fieldset-basic-info",
            *fieldset_content  # ... then pass them to a fieldset
        ))

        layout_blocks.append(layout.Fieldset(
            _("Educational Department Address"),
            layout.HTML("""{% load i18n %}<div class="subtitle">{% trans "leave blank if you want to use the data from the location" %}</div>"""),
            layout.Row(
                layout.Div(
                    "street_address",
                    "street_address2",
                    "postal_code",
                    "city",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.HTML("""{% load i18n %}
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
                    """),
                    "latitude",
                    "longitude",
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md",
            ),
            css_class="fieldset-where",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Districts"),
            "districts",
            css_class="fieldset-services",
        ))

        layout_blocks.append(layout.Fieldset(
            _("Contact"),

            layout.Row(
                layout.Div(
                    'contact_name', css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
            ),
            layout.Row(
                layout.Div(
                    'email', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.Field('website', placeholder="http://"), css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md"
            ),

            layout.Row(
                layout.Div(
                    layout.HTML('{% load i18n %}<div><label class="with">{% trans "Phone" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'phone_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'phone_area',  css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'phone_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                     css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                layout.Div(
                    layout.HTML('{% load i18n %}<div><label class="with">{% trans "Fax" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'fax_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'fax_area', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'fax_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                    css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                ),
                css_class="row-md"
            ),

            css_class="fieldset-other-contact-info"
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


class DescriptionForm(autocomplete_light.ModelForm):
    class Meta:
        model = Department
        fields = [
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(DescriptionForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []

        layout_blocks.append(layout.Fieldset(
            _("Members"),
            layout.HTML("""{% load crispy_forms_tags i18n %}
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
            """),
            css_id="members_fieldset",
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
        layout_blocks.append(layout.Fieldset(
            _("Description"),
            css_class="fieldset-basic-info",
            *fieldset_content  # ... then pass them to a fieldset
        ))

        layout_blocks.append(layout.Fieldset(
            _("Social media"),
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


class DepartmentMemberForm(autocomplete_light.ModelForm):
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
        model = DepartmentMember
        autocomplete_fields = ('person',)

    def __init__(self, *args, **kwargs):
        super(DepartmentMemberForm, self).__init__(*args, **kwargs)

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'function_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.fields['sort_order'].widget = forms.HiddenInput()
        self.fields['person'].required = False
        self.fields['person'].label = ugettext('Choose person') + ' (' + ugettext('or') + ' <a href="" class="enter_person">' + ugettext('click here to enter a new person') + '</a>)'
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
        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('function_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        layout_blocks.append(layout.Fieldset(
            _("Function"),
            css_class="fieldset-basic-info",
            *fieldset_content  # ... then pass them to a fieldset
        ))
        layout_blocks.append(layout.Fieldset(
            _("Contact"),
            layout.Row(
                layout.Div(
                    'email', css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-md"
            ),

            layout.Row(
                layout.Div(
                    layout.HTML('{% load i18n %}<div><label class="with">{% trans "Phone" %}</label></div>'),
                    layout.Row(
                        layout.Div(
                            'phone_country', css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'phone_area',  css_class="col-xs-3 col-sm-3 col-md-3 col-lg-3"
                        ),
                        layout.Div(
                            'phone_number', css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6"
                        ),
                        css_class="row-xs"
                    ),
                     css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12"
                ),
                css_class="row-md"
            ),
            css_class="fieldset-contact-info"
        ))
        layout_blocks.append(
            layout.Div(
                "sort_order",
                "id",
                "DELETE",
                css_class="hidden"
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def clean(self):
        cleaned = super(DepartmentMemberForm, self).clean()
        if not cleaned.get('last_name') and not cleaned.get('person'):
            msg = _("Choose a person from the database or enter his name.")
            self._errors["person"] = self.error_class([msg])
            self._errors["last_name"] = self.error_class([_('This field is required.')])
            if not cleaned.get('first_name'):
                self._errors["first_name"] = self.error_class([_('This field is required.')])
            del cleaned['last_name']
            del cleaned['person']
        return cleaned


DepartmentMemberFormset = inlineformset_factory(Department, DepartmentMember, form=DepartmentMemberForm, formset=InlineFormSet, extra=0)


class SocialMediaChannelForm(forms.ModelForm):
    class Meta:
        model = SocialMediaChannel

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

SocialMediaChannelFormset = inlineformset_factory(Department, SocialMediaChannel, form=SocialMediaChannelForm, formset=InlineFormSet, extra=0)


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = []

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('save_and_close', _('Save and close')),
                SecondarySubmit('reset', _('Cancel')),
            ))
        else:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('submit', _('Save')),
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
            'description': {'_filled': True, 'sets': {
                'social': [],
                'members': [],
            }},
            'gallery': {'_filled': True},
            '_pk': instance.pk,
        }

        ### The "basic" step ###

        fields = [
            'location',
            'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
            'contact_name',
            'phone_country', 'phone_area', 'phone_number',
            'fax_country', 'fax_area', 'fax_number',
            'email', 'website',
            'districts',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
            ]
        for fname in fields:
            form_step_data['basic'][fname] = getattr(instance, fname)

        form_step_data['basic']['districts'] = instance.districts.all()

        ### The "description" step ###

        fields = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
            ]
        for fname in fields:
            form_step_data['description'][fname] = getattr(instance, fname)

        for member in instance.departmentmember_set.all():
            member_dict = {}
            fields = ['id', 'person', 'phone_country', 'phone_area', 'phone_number', 'email', 'sort_order']
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                fields += [
                    'function_%s' % lang_code,
                ]
            for fname in fields:
                member_dict[fname] = getattr(member, fname)
            form_step_data['description']['sets']['members'].append(member_dict)

        for social_media_channel in instance.socialmediachannel_set.all():
            social_media_channel_dict = {}
            social_media_channel_dict['channel_type'] = social_media_channel.channel_type
            social_media_channel_dict['url'] = social_media_channel.url
            form_step_data['description']['sets']['social'].append(social_media_channel_dict)
    else:
        form_step_data = {
            'basic': {'_filled': False, 'sets': {}},
        }
        own_locations = Location.objects.owned_by(get_current_user())
        if own_locations:
            form_step_data['basic']['location'] = own_locations[0]

    return form_step_data


def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Department.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Department()

        fields = [
            'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
            'contact_name',
            'phone_country', 'phone_area', 'phone_number',
            'fax_country', 'fax_area', 'fax_number',
            'email', 'website',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
            ]
        for fname in fields:
            setattr(instance, fname, form_step_data[current_step][fname])
            
        if form_step_data[current_step]['location']:
            instance.location = Location.objects.get(pk=form_step_data[current_step]['location'])

        if not instance.slug:
            instance.slug = get_unique_value(Department, better_slugify(instance.title_de), instance_pk=instance.pk)

        instance.save()

        instance.districts.clear()
        for cat in form_step_data['basic']['districts']:
            instance.districts.add(cat)

        current_user = get_current_user()
        if not current_user.is_superuser and not instance.get_owners():
            instance.set_owner(current_user)

        form_step_data['_pk'] = instance.pk

    if current_step == "description":
        if "_pk" in form_step_data:
            instance = Department.objects.get(pk=form_step_data['_pk'])
        else:
            return
            
        fields = []
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'description_%s' % lang_code,
                'teaser_%s' % lang_code,
            ]
        for fname in fields:
            setattr(instance, fname, form_step_data[current_step][fname])

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            setattr(instance, 'description_%s_markup_type' % lang_code, 'pt')
            setattr(instance, 'teaser_%s_markup_type' % lang_code, 'pt')

        instance.save()

        # save members
        fields = ['phone_country', 'phone_area', 'phone_number', 'email', 'sort_order']
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
                    member = DepartmentMember.objects.get(
                        pk=member_dict['id'],
                        department=instance,
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                member = DepartmentMember(department=instance)
            for fname in fields:
                setattr(member, fname, member_dict[fname])
            member.person = person
            member.save()
            member_ids_to_keep.append(member.pk)
        instance.departmentmember_set.exclude(pk__in=member_ids_to_keep).delete()

        # save social media channels
        instance.socialmediachannel_set.all().delete()
        for social_dict in form_step_data['description']['sets']['social']:
            social = SocialMediaChannel(department=instance)
            social.channel_type = social_dict['channel_type']
            social.url = social_dict['url']
            social.save()

    return form_step_data


def set_extra_context(current_step, form_steps, form_step_data, instance=None):
    if "_pk" in form_step_data:
        return {'department': Department.objects.get(pk=form_step_data['_pk'])}
    return {}


def save_data(form_steps, form_step_data, instance=None):
    # probably a dummy callback, because the data is already saved after each step
    is_new = not instance
    if not instance:
        if '_pk' in form_step_data:
            instance = Department.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Department()

    return form_step_data


def cancel_editing(request):
    return redirect("dashboard")


DEPARTMENT_FORM_STEPS = {
    'basic': {
        'title': _("Educational Department"),
        'template': "education/departments/forms/basic_info_form.html",
        'form': BasicInfoForm,
    },
    'description': {
        'title': _("Description"),
        'template': "education/departments/forms/description_form.html",
        'form': DescriptionForm,
        'formsets': {
            'members': DepartmentMemberFormset,
            'social': SocialMediaChannelFormset,
        }
    },
    'gallery': {
        'title': _("Media"),
        'template': "education/departments/forms/gallery_form.html",
        'form': GalleryForm,  # dummy form
    },
    'oninit': load_data,
    'on_set_extra_context': set_extra_context,
    'onsubmit': submit_step,
    'onsave': save_data,
    'onreset': cancel_editing,
    'success_url': "/dashboard/",
    'general_error_message': _("There are errors in this form. Please correct them and try to save again."),
    'name': 'department_editing',
    'default_path': ["basic", "description", "gallery"],
}
