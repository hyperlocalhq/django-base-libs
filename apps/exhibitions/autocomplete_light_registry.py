# -*- coding: UTF-8 -*-
import autocomplete_light
from models import Exhibition


class ExhibitionAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']
    model = Exhibition

    def choices_for_request(self):
        if not self.request.user.is_staff:
            self.choices = self.choices.filter(status="published")

        return super(ExhibitionAutocomplete, self).choices_for_request()


class OwnExhibitionAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']
    model = Exhibition

    def choices_for_request(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Shop Admins"):
            self.choices = Exhibition.objects.exclude(status="trashed")
        else:
            self.choices = Exhibition.objects.owned_by(self.request.user)
        return super(OwnExhibitionAutocomplete, self).choices_for_request()


autocomplete_light.register(Exhibition, ExhibitionAutocomplete, name="ExhibitionAutocomplete")
autocomplete_light.register(Exhibition, OwnExhibitionAutocomplete, name="OwnExhibitionAutocomplete")
