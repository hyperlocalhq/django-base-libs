# -*- coding: UTF-8 -*-
from django.db import models
from ._import_to_berlinbuehnen_base_json import ImportToBerlinBuehnenBaseJSON


class Command(ImportToBerlinBuehnenBaseJSON):
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 12
    AUTH = ('gorki', '2016')

    def define_service(self):
        Service = models.get_model("external_services", "Service")

        #url = "http://staging.gorki.de/de/gorki/export?token=DSIFHSDFIEWJSDF9734adadsd342342sdf23432esd9uejdvnpaodhefghdsnhdffgasncvqw3dsf3fsdf"
        url = "http://gorki.de/de/gorki/export?token=DSIFHSDFIEWJSDF9734adadsd342342sdf23432esd9uejdvnpaodhefghdsnhdffgasncvqw3dsf3fsdf"
        self.service, created = Service.objects.get_or_create(
            sysname="bb_gorki_theater_prods",
            defaults={
                'url': url,
                'title': u"BB Gorki Theater Productions",
            },
        )
        # update the URL
        if self.service.url != url:
            self.service.url = url
            self.service.save()
