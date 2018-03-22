# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models

import autocomplete_light

from berlinbuehnen.apps.utils import autocomplete_light_bb

from .models import Person


class AutocompletePerson(autocomplete_light_bb.AutocompleteModelBase):
    search_fields = ['^first_name', '^last_name']
    split_words = True

    autocomplete_js_attributes = attrs = {
        'placeholder': _('Start typing to choose a person'),
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        'data-widget-maximum-values': 5,
        # Enable modern-style widget !
        'class': 'modern-style',
    }

    def choice_label(self, choice):
        return unicode(choice)

autocomplete_light.register(Person, AutocompletePerson)
