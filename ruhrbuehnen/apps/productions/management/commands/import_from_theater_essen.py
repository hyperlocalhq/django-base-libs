# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Theater und Philharmonie Essen"

    IMPORT_URL = "https://www.theater-essen.de/cbstage/export.xml"

    def prepare(self):
        from django.apps import apps
        from ruhrbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Theater und Philharmonie Essen",
            defaults={
                'title_en': u"Theater und Philharmonie Essen",
                'slug': 'theater-und-philharmonie-essen',
                'street_address': u'Opernplatz 10',
                'postal_code': u'45128',
                'city': u'Essen',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="theater_essen_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Theater an der Ruhr Productions",
            },
        )
