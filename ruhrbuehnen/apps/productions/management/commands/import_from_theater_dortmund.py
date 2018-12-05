# -*- coding: UTF-8 -*-
from django.utils.encoding import force_unicode

from ._import_from_eventim_base_xml import ImportFromEventimBase


class Command(ImportFromEventimBase):
    help = "Imports productions and events from Theater Dortmund"

    IMPORT_URL = "https://www.theaterdo.de/fileadmin/eventim/data.xml"
    IMPORT_URL_PAGE_2 = "https://www.theaterdo.de/fileadmin/eventim/data2.xml"

    def prepare(self):
        from django.apps import apps
        from ruhrbuehnen.apps.locations.models import Location, Stage

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Theater Dortmund",
            defaults={
                'title_en': u"Theater Dortmund",
                'slug': 'theater-dortmund',
                'street_address': u'Theaterkarree 1-3',
                'postal_code': u'44137',
                'city': u'Dortmund',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="theater_dortmund",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Theater Dortmund Productions",
            },
        )
        if self.service.url != self.IMPORT_URL:
            self.service.url = self.IMPORT_URL
            self.service.save()

        self.LOCATIONS_BY_EXTERNAL_ID = {
            # 1: Location.objects.get(pk=0),  # Konzerthaus Dortmund
            # 2: Location.objects.get(pk=0),  # Opernhaus Dortmund
            # 3: Location.objects.get(pk=0),  # Schauspielhaus Dortmund
            # 4: Location.objects.get(pk=0),  # Junge Oper Dortmund
            # 7: Location.objects.get(pk=0),  # Kinder und Jugendtheater
            # 11: Location.objects.get(pk=0),  # Ballettzentrum Dortmund
            # 13: Location.objects.get(pk=0),  # Orchesterzentrum NRW Dortmund
            # 14: Location.objects.get(pk=0),  # Lensing-Carree Conference Center
        }

        self.STAGES_BY_EXTERNAL_ID = {
            # 1: Stage.objects.get(pk=0),  # Opernhaus Dortmund
            # 2: Stage.objects.get(pk=0),  # Schauspielhaus Dortmund
            3: Stage.objects.get(pk=236),  # Konzerthaus Dortmund
            4: Stage.objects.get(
                pk=238
            ),  # KJT Dortmund in der Sckellstraße (Theatercafe)
            6: Stage.objects.get(pk=234),  # Schauspielhaus Dortmund (Studio)
            9: Stage.objects.get(pk=235),  # Opernhaus Dortmund (Matinee)
            37: Stage.objects.get(pk=235),  # Opernhaus Dortmund (Opernfoyer)
            # 38: Stage.objects.get(pk=0),  # Ballettzentrum Dortmund
            # 42: Stage.objects.get(pk=0),  # Orchesterzentrum NRW
            48: Stage.objects.get(pk=237),  # Junge Oper Dortmund
            # 62: Stage.objects.get(pk=0),  # Lensing Carree Conference Center
        }

    def main(self):
        import requests
        from xml.etree import ElementTree

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Importing Productions ===\n")

        for page_url in (self.IMPORT_URL, self.IMPORT_URL_PAGE_2):
            r = requests.get(
                page_url, params={}, headers={
                    'User-Agent': 'RuhrBuehnen',
                }
            )
            if r.status_code != 200:
                self.all_feeds_alright = False
                self.stderr.write(u"Error status: %s\n" % r.status_code)
                continue

            try:
                root_node = ElementTree.fromstring(r.content)
            except ElementTree.ParseError as err:
                self.all_feeds_alright = False
                self.stderr.write(u"Parsing error: %s\n" % force_unicode(err))
                continue

            self.save_page(root_node)
