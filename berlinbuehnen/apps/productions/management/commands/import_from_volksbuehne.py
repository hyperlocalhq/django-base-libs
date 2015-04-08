# -*- coding: UTF-8 -*-

import requests
from xml.etree import ElementTree
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db import models

from import_base import ImportFromHeimatBase

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand, ImportFromHeimatBase):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells Django to NOT download images.'),
    )
    help = "Imports productions and events from Volksbühne am Rosa-Luxemburg-Platz"

    def handle_noargs(self, *args, **options):
        from berlinbuehnen.apps.locations.models import Location
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Volksbühne am Rosa-Luxemburg-Platz",
            defaults={
                'title_en': u"Volksbühne am Rosa-Luxemburg-Platz",
                'slug': 'volksbuehne-rosa-luxemburg-platz',
                'street_address': u'Rosa-Luxemburg-Platz',
                'postal_code': u'10178',
                'city': u'Berlin',
            },
        )

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="volksbuehne_berlin_prods",
            defaults={
                'url': "http://www.volksbuehne-berlin.de/redaktion/spielplan/cbstage.xml",
                'title': "Volksbühne am Rosa-Luxemburg-Platz Productions",
            },
        )

        r = requests.get(self.service.url, params={})

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
