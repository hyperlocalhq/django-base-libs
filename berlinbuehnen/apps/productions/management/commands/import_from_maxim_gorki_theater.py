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
    help = "Imports productions and events from Maxim Gorki Theater"

    IMPORT_URL = "http://www.gorki.de/cbstage/export.xml"

    def handle_noargs(self, *args, **options):
        from berlinbuehnen.apps.locations.models import Location
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Maxim Gorki Theater",
            defaults={
                'title_en': u"Maxim Gorki Theater",
                'slug': 'gorki-theater',
                'street_address': u'Am Festungsgraben 2',
                'postal_code': u'10117',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="gorki_theater_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "Maxim Gorki Theater Productions",
            },
        )

        r = requests.get(self.service.url, params={})
        if r.status_code != 200:
            print (u"Error status: %s" % r.status_code)
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
