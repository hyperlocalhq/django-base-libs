# -*- coding: UTF-8 -*-
from ._import_from_heimat_base_xml import ImportFromHeimatBase


class Command(ImportFromHeimatBase):
    help = "Imports productions and events from BKA Theater"

    IMPORT_URL = "https://shb01.de.inter.net:8443/login_up.php3"

    def prepare(self):
        from django.apps import apps
        from berlinbuehnen.apps.locations.models import Location

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"BKA Theater",
            defaults={
                'title_en': u"BKA Theater",
                'slug': 'bka-theater',
                'street_address': u'Mehringdamm 34',
                'postal_code': u'10961',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bka_theater_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "BKA Theater Productions",
                'user': '24729',
                'password': 'Ameisenbaer12',
            },
        )

    def main(self):
        import requests
        from xml.etree import ElementTree

        r = requests.get(self.service.url, params={})
        if r.status_code != 200:
            self.all_feeds_alright = False
            print(u"Error status: %s" % r.status_code)
            return

        if self.verbosity >= self.NORMAL:
            print u"=== Importing Productions ==="

        try:
            root_node = ElementTree.fromstring(r.content)
        except ElementTree.ParseError as err:
            self.all_feeds_alright = False
            self.stderr.write(u"Parsing error: %s" % unicode(err))
            return
        self.save_page(root_node)
