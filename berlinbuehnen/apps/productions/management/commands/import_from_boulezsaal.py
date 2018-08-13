# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 193

    def prepare(self):
        from django.db import models
        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_boulezsaal_prods",
            defaults={
                'url': "https://boulezsaal.de/export/events-page-1.xml",
                'title': u"BB Boulezsaal Productions",
            },
        )
