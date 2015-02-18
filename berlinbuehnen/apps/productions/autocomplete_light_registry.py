# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

import autocomplete_light
from models import Production


class AutocompleteProduction(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title_de', 'title_en', 'subtitle_de', 'subtitle_en']
    autocomplete_js_attributes = attrs = {
        'placeholder': _('Start typing to choose a production'),
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        'data-widget-maximum-values': 5,
        # Enable modern-style widget !
        'class': 'modern-style',
    }

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        try:
            self_id = int(self.request.GET.get('self_id', ""))
        except ValueError:
            self_id = None

        choices = self.choices.all()
        if q:
            choices = choices.filter(title__icontains=q)
        choices = choices.exclude(pk=self_id)

        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Production, AutocompleteProduction)