# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from Berliner Philharmonie"

    IMPORT_URL = "https://www.berliner-philharmoniker.de/api/kulturserver/"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="berliner_philharmonie_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Berliner Philharmonie Productions",
            },
        )

        self.delete_existing_productions_and_events()

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Berliner Philharmonie",
            defaults={
                'title_en': u"Berliner Philharmonie",
                'slug': 'berliner-philharmonie',
                'street_address': u'Herbert-von-Karajan-Str. 1',
                'postal_code': u'10785',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

    def main(self):
        import requests
        from xml.etree import ElementTree
        from django.utils.encoding import smart_str
        r = requests.get(self.service.url, params={})
        if r.status_code != 200:
            self.all_feeds_alright = False
            self.stderr.write(u"Error status: %s" % r.status_code)
            return

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Importing Productions ===\n")

        content = r.content
        content = content.replace('&Auml;', smart_str(u'Ä'))
        content = content.replace('&Ouml;', smart_str(u'Ö'))
        content = content.replace('&Uuml;', smart_str(u'Ü'))
        content = content.replace('&auml;', smart_str(u'ä'))
        content = content.replace('&ouml;', smart_str(u'ö'))
        content = content.replace('&uuml;', smart_str(u'ü'))
        content = content.replace('&szlig;', smart_str(u'ß'))
        try:
            root_node = ElementTree.fromstring(content)
        except ElementTree.ParseError as err:
            self.all_feeds_alright = False
            self.stderr.write(u"Parsing error: %s" % unicode(err))
            return

        self.save_page(root_node)
