# -*- coding: UTF-8 -*-
from ._import_from_culturebase_base_xml import ImportFromCulturebaseBase


class Command(ImportFromCulturebaseBase):
    help = "Imports productions and events from Culturebase / Deutsche Oper Berlin"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location
        from berlinbuehnen.apps.people.models import AuthorshipType
        self.load_and_parse_locations()

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Deutsche Oper Berlin",
            defaults={
                'title_en': u"Deutsche Oper Berlin",
                'slug': 'deutsche-oper-berlin',
                'street_address': u'Bismarckstraße 35',
                'postal_code': u'10627',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="culturebase_dob_prods",
            defaults={
                'url': "https://export.culturebase.org/studio_38/event/dob.xml",
                'title': "Culturebase DOB Productions",
            },
        )

        self.authorship_types_de = AuthorshipType.objects.all().values_list("title_de", flat="True")

        self.helper_dict = {
            'prefix': '{http://export.culturebase.org/schema/event/CultureBaseExport}'
        }
