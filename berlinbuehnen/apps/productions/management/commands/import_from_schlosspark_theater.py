# -*- coding: UTF-8 -*-

import requests
from xml.etree import ElementTree
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db import models

from _import_from_heimat_base_xml import ImportFromHeimatBase

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand, ImportFromHeimatBase):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells Django to NOT download images.'),
    )
    help = "Imports productions and events from Schlosspark Theater"

    IMPORT_URL = "http://www.schlosspark-theater.de/index.php?do=export"

    def handle_noargs(self, *args, **options):
        from berlinbuehnen.apps.locations.models import Location
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Schlosspark Theater",
            defaults={
                'title_en': u"Schlosspark Theater",
                'slug': 'schlosspark-theater',
                'street_address': u'Schloßstraße 48',
                'postal_code': u'12165',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="schlosspark_theater_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Schlosspark Theater Productions",
            },
        )

        r = requests.get(self.service.url, params={})
        if r.status_code != 200:
            print(u"Error status: %s" % r.status_code)
            return

        if self.verbosity >= NORMAL:
            print u"=== Importing Productions ==="

        self.stats = {
            'prods_added': 0,
            'prods_updated': 0,
            'prods_skipped': 0,
            'events_added': 0,
            'events_updated': 0,
            'events_skipped': 0,
        }

        root_node = ElementTree.fromstring(r.content)
        self.save_page(root_node)

        if self.verbosity >= NORMAL:
            print u"Productions added: %d" % self.stats['prods_added']
            print u"Productions updated: %d" % self.stats['prods_updated']
            print u"Productions skipped: %d" % self.stats['prods_skipped']
            print u"Events added: %d" % self.stats['events_added']
            print u"Events updated: %d" % self.stats['events_updated']
            print u"Events skipped: %d" % self.stats['events_skipped']
            print
