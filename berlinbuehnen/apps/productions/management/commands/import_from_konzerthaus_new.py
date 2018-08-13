# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    help = "Imports productions and events from Konzerthaus"

    def prepare(self):
        from django.db import models
        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_konzerthaus_prods",
            defaults={
                'url': "http://www.konzerthaus.de/berlin_buehnen.xml",
                'title': u"BB Konzerthaus Productions",
            },
        )
