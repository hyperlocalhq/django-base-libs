# -*- coding: UTF-8 -*-
import autocomplete_light
from models import Workshop


class WorkshopAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']
    model = Workshop

    def choices_for_request(self):
        if not self.request.user.is_staff:
            self.choices = self.choices.filter(status="published")

        return super(WorkshopAutocomplete, self).choices_for_request()


class OwnWorkshopAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']
    model = Workshop

    def choices_for_request(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Shop Admins"):
            self.choices = Workshop.objects.exclude(status="trashed")
        else:
            self.choices = Workshop.objects.owned_by(self.request.user)
        return super(OwnWorkshopAutocomplete, self).choices_for_request()


autocomplete_light.register(Workshop, WorkshopAutocomplete, name="WorkshopAutocomplete")
autocomplete_light.register(Workshop, OwnWorkshopAutocomplete, name="OwnWorkshopAutocomplete")
