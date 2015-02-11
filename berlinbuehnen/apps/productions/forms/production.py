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

from berlinbuehnen.apps.locations.models import Location, Stage, Image, SocialMediaChannel

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)
EXCLUDED_LANGUAGES = set(dict(settings.LANGUAGES).keys()) - set(dict(FRONTEND_LANGUAGES).keys())

from berlinbuehnen.utils.forms import PrimarySubmit
from berlinbuehnen.utils.forms import SecondarySubmit
from berlinbuehnen.utils.forms import InlineFormSet



PRODUCTION_FORM_STEPS = {
    'basic': {
        'title': _("Production"),
        'template': "locations/forms/basic_info_form.html",
        'form': forms.Form,
        #'formsets': {
        #    'social': SocialMediaChannelFormset,
        #}
    },
    'stages': {
        'title': _("Stages"),
        'template': "locations/forms/stages_form.html",
        'form': forms.Form,  # dummy form
        #'formsets': {
        #    'stages': StageFormset,
        #}
    },
    'gallery': {
        'title': _("Images"),
        'template': "locations/forms/gallery_form.html",
        'form': forms.Form,  # dummy form
    },
    #'oninit': load_data,
    #'on_set_extra_context': set_extra_context,
    #'onsubmit': submit_step,
    #'onsave': save_data,
    #'onreset': cancel_editing,
    'success_url': "/dashboard/",
    'general_error_message': _("There are errors in this form. Please correct them and try to save again."),
    'name': 'location_editing',
    'default_path': ["basic", "stages", "gallery"],
}
