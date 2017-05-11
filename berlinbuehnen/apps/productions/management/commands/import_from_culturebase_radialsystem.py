# -*- coding: UTF-8 -*-
from ._import_from_culturebase_base_xml import ImportFromCulturebaseBase


class Command(ImportFromCulturebaseBase):
    help = "Imports productions and events from Culturebase / RADIALSYSTEM V"

    def prepare(self):
        from django.db import models
        from berlinbuehnen.apps.locations.models import Location
        from berlinbuehnen.apps.people.models import AuthorshipType

        self.load_and_parse_locations()

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"RADIALSYSTEM V",
            defaults={
                'title_en': u"RADIALSYSTEM V",
                'slug': 'radialsystem-v',
                'street_address': u'Holzmarktstrasse 33',
                'postal_code': u'10243',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="culturebase_radialsystem_prods",
            defaults={
                'url': "https://export.culturebase.org/studio_38/event/radialsystem.xml",
                'title': "Culturebase Radialsystem Productions",
            },
        )

        self.authorship_types_de = AuthorshipType.objects.all().values_list("title_de", flat="True")

        self.helper_dict = {
            'prefix': '{http://export.culturebase.org/schema/event/CultureBaseExport}'
        }
