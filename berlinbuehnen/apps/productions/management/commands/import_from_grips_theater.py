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
    help = "Imports productions and events from GRIPS Theater"

    IMPORT_URL = "http://www.grips-theater.de/assets/bb-upload.xml"
    DEFAULT_PUBLISHING_STATUS = "published"

    def handle_noargs(self, *args, **options):
        from berlinbuehnen.apps.locations.models import Location
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="grips_theater_prods",
            defaults={
                'url': self.IMPORT_URL,
                'title': "GRIPS Theater Productions",
            },
        )

        if not self.should_reimport(self.service):
            if self.verbosity >= NORMAL:
                print u"=== Nothing to update ==="
            return

        # self.delete_existing_productions_and_events(self.service)

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
            'prods_deleted': 0,
            'events_added': 0,
            'events_updated': 0,
            'events_skipped': 0,
            'events_deleted': 0,
        }

        root_node = ElementTree.fromstring(r.content)
        self.save_page(root_node)

        self.delete_outdated_productions_and_events(self.service)

        if self.verbosity >= NORMAL:
            print u"Productions added: %d" % self.stats['prods_added']
            print u"Productions updated: %d" % self.stats['prods_updated']
            print u"Productions skipped: %d" % self.stats['prods_skipped']
            print u"Productions deleted: %d" % self.stats['prods_deleted']
            print u"Events added: %d" % self.stats['events_added']
            print u"Events updated: %d" % self.stats['events_updated']
            print u"Events skipped: %d" % self.stats['events_skipped']
            print u"Events deleted: %d" % self.stats['events_deleted']
            print
