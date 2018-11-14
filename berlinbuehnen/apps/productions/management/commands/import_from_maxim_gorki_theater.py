# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_json import ImportToBerlinBuehnenBaseJSON


class Command(ImportToBerlinBuehnenBaseJSON):
    help = "Imports productions and events from a Maxim Gorki Theater"

    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 12
    AUTH = ('gorki', '2016')

    def prepare(self):
        from django.apps import apps
        Service = apps.get_model("external_services", "Service")

        URL = "http://gorki.de/de/gorki/export?token=DSIFHSDFIEWJSDF9734adadsd342342sdf23432esd9uejdvnpaodhefghdsnhdffgasncvqw3dsf3fsdf"
        self.service, created = Service.objects.get_or_create(
            sysname="bb_gorki_theater_prods",
            defaults={
                'url': URL,
                'title': u"BB Gorki Theater Productions",
            },
        )
        # update the URL
        if self.service.url != URL:
            self.service.url = URL
            self.service.save()
