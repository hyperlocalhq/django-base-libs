# -*- coding: UTF-8 -*-

from django import forms
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.db import models

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from berlinbuehnen.apps.productions.models import Production, Event

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from berlinbuehnen.utils.forms import PrimarySubmit
from berlinbuehnen.utils.forms import SecondarySubmit
from berlinbuehnen.utils.forms import InlineFormSet


class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = Production


class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Production


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Production


class EventsForm(forms.ModelForm):
    class Meta:
        model = Production


def load_data(instance=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'basic': {'_filled': True, 'sets': {'social': []}},
            'description': {'_filled': True},
            'gallery': {'_filled': True},
            'events': {'_filled': True},
            '_pk': instance.pk,
        }
        fields = [
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
            ]
        for fname in fields:
            form_step_data['basic'][fname] = getattr(instance, fname)

    return form_step_data


def submit_step(current_step, form_steps, form_step_data, instance=None):
    if current_step == "basic":
        # save the entry
        if "_pk" in form_step_data:
            instance = Production.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Production()

        fields = [
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
            ]
        for fname in fields:
            setattr(instance, fname, form_step_data[current_step][fname])

        instance.save()

        form_step_data['_pk'] = instance.pk

    if current_step == "stages":
        if "_pk" in form_step_data:
            instance = Production.objects.get(pk=form_step_data['_pk'])
        else:
            return

        stage_fields = [
            'street_address', 'street_address2', 'postal_code', 'city', 'latitude', 'longitude',
        ]
        for lang_code, lang_name in FRONTEND_LANGUAGES:
            stage_fields += [
                'title_%s' % lang_code,
                'description_%s' % lang_code,
            ]
        stage_ids_to_keep = []
        for stage_dict in form_step_data['stages']['sets']['stages']:
            if stage_dict['id']:
                try:
                    stage = Event.objects.get(
                        pk=stage_dict['id'],
                        location=instance,
                    )
                except models.ObjectDoesNotExist:
                    continue
            else:
                stage = Event(location=instance)
            for fname in stage_fields:
                setattr(stage, fname, stage_dict[fname])
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                setattr(stage, 'description_%s_markup_type' % lang_code, 'pt')
            stage.save()
            stage_ids_to_keep.append(stage.pk)
        instance.stage_set.exclude(pk__in=stage_ids_to_keep).delete()

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
        #'formsets': {
        #    'social': SocialMediaChannelFormset,
        #}
    },
    'description': {
        'title': _("Description"),
        'template': "productions/forms/description_form.html",
        'form': DescriptionForm,
        #'formsets': {
        #    'stages': EventFormset,
        #}
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
