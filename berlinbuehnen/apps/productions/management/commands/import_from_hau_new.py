# -*- coding: UTF-8 -*-
from ._import_to_berlinbuehnen_base_json import ImportToBerlinBuehnenBaseJSON


class Command(ImportToBerlinBuehnenBaseJSON):
    help = "Imports productions and events from HAU"

    IMPORT_URL = "https://www.tanzimaugust.de/typo3conf/ext/tbsproductions/Classes/Hook/json_result/berlinbuehne.json"
    DEFAULT_PUBLISHING_STATUS = "published"
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = 13

    def prepare(self):
        from django.db import models
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"HAU Hebbel am Ufer",
            defaults={
                'title_en': u"HAU Hebbel am Ufer",
                'slug': 'hau-hebbel-am-ufer',
                'street_address': u'Stresemannstr. 29',
                'postal_code': u'10963',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="hau_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "HAU Productions",
            },
        )

        if self.service.url != self.IMPORT_URL:
            self.service.url = self.IMPORT_URL
            self.service.save()
