# -*- coding: UTF-8 -*-
from ._import_to_ruhrbuehnen_base_json import ImportToRuhrbuehnenBaseJSON


class Command(ImportToRuhrbuehnenBaseJSON):
    help = "Imports productions and events from Musiktheater im Revier Gelsenkirchen"

    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 232
    AUTH = ('rbfetch', 'wJsMB6cR3fyrauO8Elhq')

    def prepare(self):
        from django.apps import apps
        Service = apps.get_model("external_services", "Service")

        URL = "https://rbfetch.mir.ruhr/"
        self.service, created = Service.objects.get_or_create(
            sysname="musiktheater_im_revier_gelsenkirchen_prods",
            defaults={
                'url': URL,
                'title': u"Musiktheater im Revier Gelsenkirchen Productions",
            },
        )
        # update the URL
        if self.service.url != URL:
            self.service.url = URL
            self.service.save()
