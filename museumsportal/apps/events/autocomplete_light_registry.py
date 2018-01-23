# -*- coding: UTF-8 -*-
import autocomplete_light
from models import Event


class EventAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']
    model = Event

    def choices_for_request(self):
        if not self.request.user.is_staff:
            self.choices = self.choices.filter(status="published")

        return super(EventAutocomplete, self).choices_for_request()


class OwnEventAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['title']
    model = Event

    def choices_for_request(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name="Shop Admins"):
            self.choices = Event.objects.exclude(status="trashed")
        else:
            self.choices = Event.objects.owned_by(self.request.user)
        return super(OwnEventAutocomplete, self).choices_for_request()


autocomplete_light.register(Event, EventAutocomplete, name="EventAutocomplete")
autocomplete_light.register(Event, OwnEventAutocomplete, name="OwnEventAutocomplete")
