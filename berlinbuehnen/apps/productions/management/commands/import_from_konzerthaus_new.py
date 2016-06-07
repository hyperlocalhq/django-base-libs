# -*- coding: UTF-8 -*-
from django.db import models
from .import_to_berlinbuehnen_base import ImportToBerlinBuehnenBase


class Command(ImportToBerlinBuehnenBase):

    def define_service(self):
        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_konzerthaus_prods",
            defaults={
                'url': "http://www.konzerthaus.de/berlin_buehnen.xml",
                'title': u"BB Konzerthaus Productions",
            },
        )
