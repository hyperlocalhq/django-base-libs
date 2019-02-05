# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from GRIPS Theater"

    IMPORT_URL = "http://www.grips-theater.de/assets/bb-upload.xml"
    DEFAULT_PUBLISHING_STATUS = "published"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location
        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="grips_theater_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "GRIPS Theater Productions",
            },
        )
        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"GRIPS Theater",
            defaults={
                'title_en': u"GRIPS Theater",
                'slug': 'grips-theater',
                'street_address': u'Altonaer Straße 22',
                'postal_code': u'10557',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

    def main(self):
        import requests
        from xml.etree import ElementTree
        if not self.should_reimport():
            if self.verbosity >= self.NORMAL:
                self.stdout.write(u"=== Nothing to update ===\n")
            return

        r = requests.get(self.service.url, params={})
        if r.status_code != 200:
            self.all_feeds_alright = False
            self.stdout.write(u"Error status: %s" % r.status_code)
            return

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Importing Productions ===\n")

        try:
            root_node = ElementTree.fromstring(r.content)
        except ElementTree.ParseError as err:
            self.all_feeds_alright = False
            self.stderr.write(u"Parsing error: %s" % unicode(err))
            return
        self.save_page(root_node)
