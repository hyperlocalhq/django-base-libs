# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    help = "Imports productions and events from Staatsoper Berlin"
    DEFAULT_PUBLISHING_STATUS = "published"
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 9

    def prepare(self):
        from django.db import models
        Service = models.get_model("external_services", "Service")

        URL = "https://www.staatsoper-berlin.de/export/berlin-buehnen/feed.xml"
        self.service, created = Service.objects.get_or_create(
            sysname="bb_staatsoper_berlin_prods",
            defaults={
                'url': URL,
                'title': u"BB Staatsoper Berlin Productions",
            },
        )
        if not created and self.service.url != URL:
            # make sure that the URL is actual
            self.service.url = URL
            self.service.save()
