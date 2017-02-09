# -*- coding: UTF-8 -*-
from django.db import models
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    DEFAULT_PUBLISHING_STATUS = "published"
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 197

    def define_service(self):
        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_staatskapelle_prods",
            defaults={
                'url': "https://www.staatskapelle-berlin.de/export.xml",
                'title': u"BB Staatskapelle Productions",
            },
        )
