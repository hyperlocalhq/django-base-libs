# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

import autocomplete_light
from models import Location, Stage

# This will generate a PersonAutocomplete class
autocomplete_light.register(Location,
    # Just like in ModelAdmin.search_fields
    search_fields=['title_de', 'title_en', 'subtitle_de', 'subtitle_en'],
    attrs={
        # This will set the input placeholder attribute:
        'placeholder': _('Start typing to choose a stage'),
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


class AutocompleteStage(autocomplete_light.AutocompleteModelBase):
    autocomplete_js_attributes = attrs = {
        'placeholder': _('Start typing to choose a venue'),
        'data-autocomplete-minimum-characters': 0,
    }
    widget_attrs = {
        'data-widget-maximum-values': 5,
        # Enable modern-style widget !
        'class': 'modern-style',
    }

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        try:
            location_ids = [int(location_id) for location_id in self.request.GET.get('location_ids', "").split(',')]
        except ValueError:
            location_ids = []

        choices = self.choices.all()
        if q:
            choices = choices.filter(title__icontains=q)
        choices = choices.filter(location__pk__in=location_ids)

        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Stage, AutocompleteStage)