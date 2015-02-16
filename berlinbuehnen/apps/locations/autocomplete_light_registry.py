# -*- coding: UTF-8 -*-

import autocomplete_light
from models import Location

# This will generate a PersonAutocomplete class
autocomplete_light.register(Location,
    # Just like in ModelAdmin.search_fields
    search_fields=['title_de', 'title_en', 'subtitle_de', 'subtitle_en'],
    attrs={
        # This will set the input placeholder attribute:
        'placeholder': 'Start typing to enter location title?',
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