# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    help = "Imports productions and events from Berliner Ensemble"
    DEFAULT_PUBLISHING_STATUS = "published"
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 24

    def prepare(self):
        from django.db import models
        Service = models.get_model("external_services", "Service")

        URL = "https://neu.berliner-ensemble.de/api/v1/productions?_format=bbuehnen"
        self.service, created = Service.objects.get_or_create(
            sysname="bb_berliner_ensemble_prods",
            defaults={
                'url': URL,
                'title': u"BB Berliner Ensemble Productions",
            },
        )
        if not created and self.service.url != URL:
            # make sure that the URL is actual
            self.service.url = URL
            self.service.save()
