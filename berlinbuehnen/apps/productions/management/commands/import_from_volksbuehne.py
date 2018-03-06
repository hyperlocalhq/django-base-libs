# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    help = u"Imports productions and events from Volksbühne Berlin"
    DEFAULT_PUBLISHING_STATUS = "published"
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 6

    def prepare(self):
        from django.db import models
        Service = models.get_model("external_services", "Service")

        URL = "https://www.volksbuehne.berlin/api/export/berlinbuehnen.xml"
        self.service, created = Service.objects.get_or_create(
            sysname="volksbuehne_berlin_prods",
            defaults={
                'url': URL,
                'title': u"BB Volksbühne Productions",
            },
        )
        if not created and self.service.url != URL:
            # make sure that the URL is actual
            self.service.url = URL
            self.service.save()
