# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

import autocomplete_light

from ruhrbuehnen.apps.utils import autocomplete_light_bb

from .models import Production


class AutocompleteProduction(autocomplete_light_bb.AutocompleteModelBase):
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
        from jetson.apps.permissions.models import PerObjectGroup
        q = self.request.GET.get('q', '')
        try:
            self_id = int(self.request.GET.get('self_id', ""))
        except ValueError:
            self_id = None

        if self.request.user.has_perm("productions.change_production"):
            choices = self.choices.exclude(status="trashed")
        else:
            ids = map(
                int,
                PerObjectGroup.objects.filter(
                    content_type__app_label="productions",
                    content_type__model="production",
                    sysname__startswith="owners",
                    users=self.request.user,
                ).values_list("object_id", flat=True)
            )
            choices = self.choices.filter(pk__in=ids).exclude(status="trashed")

        if q:
            choices = choices.filter(title__icontains=q)
        choices = choices.exclude(pk=self_id)

        return self.order_choices(choices)[0:self.limit_choices]


autocomplete_light.register(Production, AutocompleteProduction)
