# -*- coding: UTF-8 -*-
import autocomplete_light
from models import Museum


class MuseumAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']
    model = Museum

    def choices_for_request(self):
        if not self.request.user.is_staff:
            self.choices = self.choices.filter(status="published")

        return super(MuseumAutocomplete, self).choices_for_request()


class OwnMuseumAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']
    model = Museum

    def choices_for_request(self):
        self.choices = Museum.objects.owned_by(self.request.user)
        return super(OwnMuseumAutocomplete, self).choices_for_request()


autocomplete_light.register(Museum, MuseumAutocomplete, name="MuseumAutocomplete")
autocomplete_light.register(Museum, OwnMuseumAutocomplete, name="OwnMuseumAutocomplete")
