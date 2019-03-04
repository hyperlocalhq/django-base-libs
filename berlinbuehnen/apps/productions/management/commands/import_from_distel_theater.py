# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    help = "Imports productions and events from Distel Theater"
    DEFAULT_PUBLISHING_STATUS = "published"
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 31  # DISTEL Kabarett-Theater

    def prepare(self):
        from django.apps import apps
        Service = apps.get_model("external_services", "Service")

        URL = "https://distel-berlin.de/distel_events.xml"
        self.service, created = Service.objects.get_or_create(
            sysname="bb_distel_theater_prods",
            defaults={
                'url': URL,
                'title': u"BB Distel Theater Productions",
            },
        )
        if not created and self.service.url != URL:
            # make sure that the URL is actual
            self.service.url = URL
            self.service.save()
