# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

import autocomplete_light
from .models import Department

# This will generate a PersonAutocomplete class
autocomplete_light.register(Department,
    # Just like in ModelAdmin.search_fields
    search_fields=['title_de', 'title_en',],
    attrs={
        # This will set the input placeholder attribute:
        'placeholder': _('Start typing to choose an educational department'),
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 1,
    },
    # This will set the data-widget-maximum-values attribute on the
    # widget container element, and will be set to
    # yourlabs.Widget.maximumValues (jQuery handles the naming
    # conversion).
    widget_attrs={
        'data-widget-maximum-values': 5,
        # Enable modern-style widget !
        'class': 'modern-style',
    },
)
