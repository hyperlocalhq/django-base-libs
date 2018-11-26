# -*- coding: UTF-8 -*-
from ._import_from_eventim_base_xml import ImportFromEventimBase


class Command(ImportFromEventimBase):
    help = "Imports productions and events from Theater Oberhausen"

    IMPORT_URL = "https://theater-oberhausen.eventim-inhouse.de/webshop/export/export"

    def prepare(self):
        from django.apps import apps
        from ruhrbuehnen.apps.locations.models import Location, Stage

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Theater Oberhausen",
            defaults={
                'title_en': u"Theater Oberhausen",
                'slug': 'theater-oberhausen',
                'street_address': u'Will-Quadflieg-Platz 1',
                'postal_code': u'46045',
                'city': u'Oberhausen',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="theater_oberhausen",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Theater Oberhausen Productions",
            },
        )
        if self.service.url != self.IMPORT_URL:
            self.service.url = self.IMPORT_URL
            self.service.save()

        self.LOCATIONS_BY_EXTERNAL_ID = {
            1: Location.objects.get(pk=236),  # Theater Oberhausen
            # 26: Location.objects.get(pk=0),  # CongressCentrumOberhausen-Luise Albertz
            # 27: Location.objects.get(pk=0),  # Kantine Rathaus Oberhausen
            # 29: Location.objects.get(pk=0),  # Essener Str. 2-24, 46047 Oberhausen
        }

        self.STAGES_BY_EXTERNAL_ID = {
            # 79: Stage.objects.get(pk=0),  # Großes Haus
            # 87: Stage.objects.get(pk=0),  # Pool
            89: Stage.objects.get(pk=250),  # Saal 2
            # 90: Stage.objects.get(pk=0),  # CCO-Luise Albertz Halle
            # 97: Stage.objects.get(pk=0),  # Kantine Rathaus Oberhausen
            # 100: Stage.objects.get(pk=0),  # The Mirai,Essener Str.2-41 OB
        }
