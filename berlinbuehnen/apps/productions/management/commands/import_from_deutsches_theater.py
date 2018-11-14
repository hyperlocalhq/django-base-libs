# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Deutsches Theater"

    IMPORT_URL = "http://www.deutschestheater.de/cbstage/export.xml"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Deutsches Theater Berlin",
            defaults={
                'title_en': u"Deutsches Theater Berlin",
                'slug': 'deutsches-theater-berlin',
                'street_address': u'Schumannstraße 13a',
                'postal_code': u'10117',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="deutsches_theater_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Deutsches Theater Productions",
            },
        )
