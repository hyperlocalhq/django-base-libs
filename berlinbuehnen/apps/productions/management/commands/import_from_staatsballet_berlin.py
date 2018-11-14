# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Staatsballett Berlin"

    IMPORT_URL = "https://www.staatsballett-berlin.de/xml/cb_staging.xml"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Staatsballett Berlin",
            defaults={
                'title_en': u"Staatsballett Berlin",
                'slug': 'staatsballett-berlin',
                'street_address': u'Richard-Wagner-Str. 10',
                'postal_code': u'10585',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="staatsballett_berlin_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Staatsballett Berlin Productions",
            },
        )
        if self.service.url != self.IMPORT_URL:
            self.service.url = self.IMPORT_URL
            self.service.save()
