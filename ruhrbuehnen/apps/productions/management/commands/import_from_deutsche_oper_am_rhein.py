# -*- coding: UTF-8 -*-
from ._import_from_culturebase_base_xml import ImportFromCulturebaseBase


class Command(ImportFromCulturebaseBase):
    help = "Imports productions and events from Culturebase / Deutsche Oper am Rhein"

    def prepare(self):
        from django.apps import apps
        from ruhrbuehnen.apps.locations.models import Location

        self.load_and_parse_locations()

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Deutsche Oper am Rhein im Theater Duisburg",
            defaults={
                'title_en': u"Deutsche Oper am Rhein im Theater Duisburg",
                'slug': 'deutsche-oper-am-rhein-im-theater-duisburg',
                'street_address': u'Opernplatz',
                'postal_code': u'47051',
                'city': u'Duisburg',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        URL = "https://export.culturebase.org/studio_38/event/dor.xml"
        self.service, created = Service.objects.get_or_create(
            sysname="culturebase_deutsche_oper_am_rhein_prods",
            defaults={
                'url': URL,
                'title': "Culturebase Radialsystem Productions",
            },
        )
        if self.service.url != URL:
            self.service.url = URL
            self.service.save()

        self.helper_dict = {
            'prefix':
                '{http://export.culturebase.org/schema/event/CultureBaseExport}'
        }
