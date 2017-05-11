# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    help = "Imports productions and events from a local example file"

    def prepare(self):
        from django.db import models
        from django.conf import settings
        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_example",
            defaults={
                'url': "file://{}/production_import_specs/example.xml".format(settings.PROJECT_PATH),
                'title': u"Berlin Bühnen Import API Example",
            },
        )
