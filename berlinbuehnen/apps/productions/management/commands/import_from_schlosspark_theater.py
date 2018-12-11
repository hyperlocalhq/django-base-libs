# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Schlosspark Theater"

    IMPORT_URL = "http://www.schlosspark-theater.de/index.php?do=export"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Schlosspark Theater",
            defaults={
                'title_en': u"Schlosspark Theater",
                'slug': 'schlosspark-theater',
                'street_address': u'Schloßstraße 48',
                'postal_code': u'12165',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="schlosspark_theater_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Schlosspark Theater Productions",
            },
        )
