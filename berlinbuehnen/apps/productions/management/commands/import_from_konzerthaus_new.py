# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    help = "Imports productions and events from Konzerthaus"

    IMPORT_URL = "https://www.konzerthaus.de/berlin_buehnen.xml"

    def prepare(self):
        from django.db import models
        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_konzerthaus_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': u"BB Konzerthaus Productions",
            },
        )

        if self.service.url != self.IMPORT_URL:
            self.service.url = self.IMPORT_URL
            self.service.save()