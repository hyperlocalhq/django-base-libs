# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Theater an der Parkaue"

    IMPORT_URL = "http://www.parkaue.de/redaktion/spielplan/cbstage.xml"

    def prepare(self):
        from django.db import models
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Theater an der Parkaue",
            defaults={
                'title_en': u"Theater an der Parkaue",
                'slug': 'theater-parkaue',
                'street_address': u'Parkaue 29',
                'postal_code': u'10367',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="parkaue_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Theater an der Parkaue Productions",
            },
        )
