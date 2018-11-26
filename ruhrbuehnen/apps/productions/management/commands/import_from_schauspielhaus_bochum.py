# -*- coding: UTF-8 -*-
from ._import_to_ruhrbuehnen_base_xml import ImportToRuhrbuehnenBaseXML


class Command(ImportToRuhrbuehnenBaseXML):
    help = "Imports productions and events from Schauspielhaus Bochum"
    DEFAULT_PUBLISHING_STATUS = "published"
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 227  # Schauspielhaus Bochum

    def prepare(self):
        from django.apps import apps
        Service = apps.get_model("external_services", "Service")

        URL = "https://www.schauspielhausbochum.de/api/export/ruhrbuehnen.xml"
        self.service, created = Service.objects.get_or_create(
            sysname="rb_schauspielhaus_bochum_prods",
            defaults={
                'url': URL,
                'title': u"RB Schauspielhaus Bochum Productions",
            },
        )
        if not created and self.service.url != URL:
            # make sure that the URL is actual
            self.service.url = URL
            self.service.save()
