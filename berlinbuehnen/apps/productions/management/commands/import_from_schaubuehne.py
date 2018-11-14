# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = u"Imports productions and events from Schaubühne am Lehniner Platz"

    IMPORT_URL = "http://schaubuehne.de/export/kulturserver.php"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Schaubühne am Lehniner Platz",
            defaults={
                'title_en': u"Schaubühne am Lehniner Platz",
                'slug': 'schaubuehne-am-lehniner-platz',
                'street_address': u'Kurfürstendamm 153',
                'postal_code': u'10709',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="schaubuehne_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': u"Schaubühne am Lehniner Platz Productions",
            },
        )
