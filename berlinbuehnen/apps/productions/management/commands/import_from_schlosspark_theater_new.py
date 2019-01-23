# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_xml import ImportToBerlinBuehnenBaseXML


class Command(ImportToBerlinBuehnenBaseXML):
    help = "Imports productions and events from Schlosspark Theater"

    def prepare(self):
        from django.apps import apps
        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_schlosspark_theater_prods",
            defaults={
                'url': "http://www.schlossparktheater.de/export/berlinbuehnen.php",
                'title': u"BB Schlosspark Theater Productions",
            },
        )
