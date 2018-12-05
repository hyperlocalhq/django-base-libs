# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Theater an der Ruhr"

    IMPORT_URL = "http://theater-an-der-ruhr.de/xml/"

    def prepare(self):
        from django.apps import apps
        from ruhrbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Theater an der Ruhr",
            defaults={
                'title_en': u"Theater an der Ruhr",
                'slug': 'theater-an-der-ruhr',
                'street_address': u'Akazienallee 61',
                'postal_code': u'45478',
                'city': u'Mülheim an der Ruhr',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="theater_an_der_ruhr_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Theater an der Ruhr Productions",
            },
        )
