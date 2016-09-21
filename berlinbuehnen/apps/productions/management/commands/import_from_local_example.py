# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):

    def define_service(self):
        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_example",
            defaults={
                'url': "file://{}/production_import_specs/example.xml".format(settings.PROJECT_PATH),
                'title': u"Berlin Bühnen Import API Example",
            },
        )
