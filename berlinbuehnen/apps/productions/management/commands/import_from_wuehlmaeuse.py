# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = u"Imports productions and events from Wühlmäuse"

    IMPORT_URL = "https://www.wuehlmaeuse.de/export"

    def prepare(self):
        from django.db import models
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Die Wühlmäuse",
            defaults={
                'title_en': u"Die Wühlmäuse",
                'slug': 'die-wuehlmaeuse',
                'street_address': u'Pommernallee 2-4',
                'postal_code': u'14052',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="wuehlmaeuse_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': u"Wühlmäuse Productions",
            },
        )
