# -*- coding: UTF-8 -*-
from ._import_to_ruhrbuehnen_base_xml import ImportToRuhrbuehnenBaseXML


class Command(ImportToRuhrbuehnenBaseXML):
    help = "Imports productions and events from Theater Dortmund"

    DEFAULT_PUBLISHING_STATUS = "published"
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 228  # Theater Dortmund
    IMPORT_URL = "https://www.theaterdo.de/api-ruhrbuehnen/"

    def prepare(self):
        from django.apps import apps

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="theater_dortmund",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Theater Dortmund Productions",
            },
        )
        if self.service.url != self.IMPORT_URL:
            self.service.url = self.IMPORT_URL
            self.service.save()
