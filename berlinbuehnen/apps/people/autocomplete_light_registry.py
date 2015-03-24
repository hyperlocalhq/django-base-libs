# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models

import autocomplete_light
from models import Person


class AutocompletePerson(autocomplete_light.AutocompleteModelBase):
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
        label = unicode(choice)
        if choice.leadership_function:
            return label + u' - ' + unicode(choice.leadership_function)
        if choice.involvement_type:
            return label + u' - ' + unicode(choice.involvement_type)
        if choice.involvement_role:
            return label + u'  - ' + unicode(choice.involvement_role)
        if choice.involvement_instrument:
            return label + u'  - ' + unicode(choice.involvement_instrument)
        if choice.authorship_type:
            return label + u' - ' + unicode(choice.authorship_type)
        return label

autocomplete_light.register(Person, AutocompletePerson)
