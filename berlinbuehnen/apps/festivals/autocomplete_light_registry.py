# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _

import autocomplete_light

from berlinbuehnen.apps.utils import autocomplete_light_bb

from .models import Festival


class AutocompleteFestival(autocomplete_light_bb.AutocompleteModelBase):
    search_fields=['title_de', 'title_en', 'subtitle_de', 'subtitle_en']
    autocomplete_js_attributes = attrs = {
        'placeholder': _('Start typing to choose a festival'),
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        'data-widget-maximum-values': 5,
        # Enable modern-style widget !
        'class': 'modern-style',
    }

autocomplete_light.register(Festival, AutocompleteFestival)
