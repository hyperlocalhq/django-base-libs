# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import autocomplete_light


class AutocompleteModelBase(autocomplete_light.AutocompleteModelBase):
    def choices_for_values(self):
        """
        Return ordered choices which pk are in
        :py:attr:`~.base.AutocompleteInterface.values`.
        """
        assert self.choices is not None, 'choices should be a queryset'
        # Note: this mod skips the None value besides empty string
        return self.order_choices(self.choices.filter(
            pk__in=[x for x in self.values if x not in ('', None)]))