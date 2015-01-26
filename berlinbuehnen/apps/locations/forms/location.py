# -*- coding: UTF-8 -*-

from django import forms
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import redirect

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from berlinbuehnen.apps.locations.models import Location, Stage, Image, SocialMediaChannel

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from berlinbuehnen.utils.forms import PrimarySubmit
from berlinbuehnen.utils.forms import SecondarySubmit
from berlinbuehnen.utils.forms import InlineFormSet


class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
            'phone_country', 'phone_area', 'phone_number',
            'fax_country', 'fax_area', 'fax_number',
            'email', 'website',
            'tickets_street_address', 'tickets_street_address2', 'tickets_postal_code', 'tickets_city',
            'tickets_email', 'tickets_website',
            'services', 'accessibility_options',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
            ]


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
                    layout.Field("url", placeholder="http://"), css_class="col-xs-12 col-sm-8 col-md-8 col-lg-8"
                ),
                css_class="row-sm"
            )
        )

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

SocialMediaChannelFormset = inlineformset_factory(Location, SocialMediaChannel, form=SocialMediaChannelForm, formset=InlineFormSet, extra=0)


class StagesForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ()


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = [
            'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'description_%s' % lang_code,
            ]

StageFormset = inlineformset_factory(Location, Stage, form=StageForm, formset=InlineFormSet, extra=0)


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = []

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        layout_blocks = []
        if self.instance and self.instance.pk:
            layout_blocks.append(bootstrap.FormActions(
                PrimarySubmit('save_and_close', _('Close')),
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
            'basic': {'_filled': True, 'sets': {'social': []}},
            'stages': {'_filled': True, 'sets': {'stages': []}},
            'gallery': {'_filled': True},
            '_pk': instance.pk,
        }
        # TODO: do the loading
    return form_step_data


def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Location.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Location()

        # TODO: do the saving

        form_step_data['_pk'] = instance.pk

    if current_step == "stages":
        if "_pk" in form_step_data:
            instance = Location.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Location()

    return form_step_data


def set_extra_context(current_step, form_steps, form_step_data, instance=None):
    if "_pk" in form_step_data:
        return {'location': Location.objects.get(pk=form_step_data['_pk'])}
    return {}


def save_data(form_steps, form_step_data, instance=None):
    # probably a dummy callback, because the data is already saved after each step
    is_new = not instance
    if not instance:
        if '_pk' in form_step_data:
            instance = Location.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Location()

    return form_step_data


def cancel_editing(request):
    return redirect("dashboard")


LOCATION_FORM_STEPS = {
    'basic': {
        'title': _("Basic Information"),
        'template': "locations/forms/basic_info_form.html",
        'form': BasicInfoForm,
        'formsets': {
            'social': SocialMediaChannelFormset,
        }
    },
    'stages': {
        'title': _("Stages"),
        'template': "locations/forms/stages_form.html",
        'form': StagesForm,  # dummy form
        'formsets': {
            'stages': StageFormset,
        }
    },
    'gallery': {
        'title': _("Images"),
        'template': "locations/forms/gallery_form.html",
        'form': GalleryForm,  # dummy form
    },
    'oninit': load_data,
    'on_set_extra_context': set_extra_context,
    'onsubmit': submit_step,
    'onsave': save_data,
    'onreset': cancel_editing,
    'general_error_message': _("There are errors in this form. Please correct them and try to save again."),
    'name': 'location_editing',
    'default_path': ["basic", "stages", "gallery"],
}
