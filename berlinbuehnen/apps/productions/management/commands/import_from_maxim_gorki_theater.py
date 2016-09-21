# -*- coding: UTF-8 -*-
from django.db import models
from ._import_to_berlinbuehnen_base_json import ImportToBerlinBuehnenBaseJSON


class Command(ImportToBerlinBuehnenBaseJSON):
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 12

    def define_service(self):
        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_gorki_theater_prods",
            defaults={
                'url': "http://gorki.de/gorki/export?token=DSIFHSDFIEWJSDF9734adadsd342342sdf23432esd9uejdvnpaodhefghdsnhdffgasncvqw3dsf3fsdf",
                'title': u"BB Gorki Theater Productions",
            },
        )
