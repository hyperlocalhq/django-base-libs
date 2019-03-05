# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Komische Oper Berlin"

    IMPORT_URL = "http://www.komische-oper-berlin.de/cbstage/export.xml"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location
        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Komische Oper Berlin",
            defaults={
                'title_en': u"Komische Oper Berlin",
                'slug': 'komische-oper-berlin',
                'street_address': u'Behrenstraße 55-57',
                'postal_code': u'10117',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="komische_oper_berlin_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Komische Oper Berlin Productions",
            },
        )
