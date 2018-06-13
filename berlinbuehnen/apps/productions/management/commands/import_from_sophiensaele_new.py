# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_json import ImportToBerlinBuehnenBaseJSON


class Command(ImportToBerlinBuehnenBaseJSON):
    help = "Imports productions and events from Sophiensaele"

    IMPORT_URL = "https://sophiensaele.poltmann.com/api/v1/stuecke/berlin-buehnen"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Sophiensæle",
            defaults={
                'title_en': u"Sophiensæle",
                'slug': 'sophiensaele',
                'street_address': u'Sophienstrasse 18',
                'postal_code': u'10178',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="sophiensaele_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Sophiensaele Productions",
            },
        )
        if self.service.url != self.IMPORT_URL:
            self.service.url = self.IMPORT_URL
            self.service.save()
