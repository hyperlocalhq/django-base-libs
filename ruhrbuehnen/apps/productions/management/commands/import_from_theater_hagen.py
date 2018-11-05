# -*- coding: UTF-8 -*-
from ._import_from_eventim_base_json import ImportFromEventimBase


class Command(ImportFromEventimBase):
    help = "Imports productions and events from Theater Hagen"

    IMPORT_URL = "https://www.theaterhagen.de/?id=449&h=da39a3ee5e6b4b0d3255bfef95601890afd80709"

    def prepare(self):
        from django.apps import apps
        from ruhrbuehnen.apps.locations.models import Location, Stage

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Theater Hagen",
            defaults={
                'title_en': u"Theater Hagen",
                'slug': 'theater-hagen',
                'street_address': u'Elberfelder Straße 65',
                'postal_code': u'58095',
                'city': u'Hagen',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="theater_hagen",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Theater Hagen Productions",
            },
        )
        if self.service.url != self.IMPORT_URL:
            self.service.url = self.IMPORT_URL
            self.service.save()

        self.LOCATIONS_BY_EXTERNAL_ID = {
            '*': Location.objects.get(pk=233),  # Theater Hagen
        }

        self.STAGES_BY_EXTERNAL_ID = {
            11: Stage.objects.get(pk=254),  # Lutz
            12: Stage.objects.get(pk=245),  # Großes Haus
            # 25: Stage.objects.get(pk=0),  # Stadthalle Hagen
            # 31: Stage.objects.get(pk=0),  # Kolpinghaus
            32: Stage.objects.get(pk=255),  # opus
            # 35: Stage.objects.get(pk=0),  # Sparkassen-Karree | Sparkasse Hagen
            # 47: Stage.objects.get(pk=0),  # Kunstquartier Hagen
            # 55: Stage.objects.get(pk=0),  # Kirche am Widey
            # 81: Stage.objects.get(pk=0),  # Kleiner Saal | Stadthalle Hagen
            83: Stage.objects.get(pk=253),  # Theatercafè
            # 105: Stage.objects.get(pk=0),  # Kulturhaus Lüdenscheid
            # 135: Stage.objects.get(pk=0),  # Ev.-Luth. Matthäus-Kirchengemeinde
            # 136: Stage.objects.get(pk=0),  # Markuskirche
            # 137: Stage.objects.get(pk=0),  # St. Mariae Himmelfahrt
        }
