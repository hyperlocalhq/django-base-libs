# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Sophiensaele"

    IMPORT_URL = "http://sophiensaele.com/tool/cbstage.php"

    def prepare(self):
        from django.db import models
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Sophiensæle",
            defaults={
                'title_en': u"Sophiensæle",
                'slug': 'sophiensaele',
                'street_address': u'Sophienstrasse 18',
                'postal_code': u'10178',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="sophiensaele_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Sophiensaele Productions",
                'user': 'sophadmin', # not used
                'password': 'I09Z2606', # not used
            },
        )
