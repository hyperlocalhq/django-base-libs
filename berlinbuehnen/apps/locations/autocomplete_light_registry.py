# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

import autocomplete_light

from berlinbuehnen.apps.utils import autocomplete_light_bb

from .models import Location, Stage


class AutocompleteLocation(autocomplete_light_bb.AutocompleteModelBase):
    autocomplete_js_attributes = attrs = {
        'placeholder': _('Start typing to choose a theater'),
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        'data-widget-maximum-values': 5,
        # Enable modern-style widget !
        'class': 'modern-style',
    }
    search_fields = ['title_de', 'title_en', 'subtitle_de', 'subtitle_en']


autocomplete_light.register(Location, AutocompleteLocation)


class AutocompleteStage(autocomplete_light_bb.AutocompleteModelBase):
    autocomplete_js_attributes = attrs = {
        'placeholder': _('Start typing to choose a stage'),
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