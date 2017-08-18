# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Volksbühne am Rosa-Luxemburg-Platz"

    IMPORT_URL = "http://dev.volksbuehne-berlin.de/api/export/berlinbuehnen.xml"

    def prepare(self):
        from django.db import models
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Volksbühne am Rosa-Luxemburg-Platz",
            defaults={
                'title_en': u"Volksbühne am Rosa-Luxemburg-Platz",
                'slug': 'volksbuehne-rosa-luxemburg-platz',
                'street_address': u'Rosa-Luxemburg-Platz',
                'postal_code': u'10178',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="volksbuehne_berlin_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Volksbühne am Rosa-Luxemburg-Platz Productions",
            },
        )
