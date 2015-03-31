# -*- coding: UTF-8 -*-

import requests
from xml.etree import ElementTree
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db import models
from django.utils.encoding import smart_str

from import_base import ImportFromHeimatBase

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand, ImportFromHeimatBase):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells Django to NOT download images.'),
    )
    help = "Imports productions and events from Berliner Philharmonie"

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="berliner_philharmonie_prods",
            defaults={
                'url': "http://www.berliner-philharmoniker.de/api/kulturserver/",
                'title': "Berliner Philharmonie Productions",
            },
        )

        r = requests.get(self.service.url, params={})

        if self.verbosity >= NORMAL:
            print u"=== Productions imported ==="

        self.stats = {
            'prods_added': 0,
            'prods_updated': 0,
            'prods_skipped': 0,
            'events_added': 0,
            'events_updated': 0,
            'events_skipped': 0,
        }

        content = r.content
        content = content.replace('&Auml;', smart_str(u'Ä'))
        content = content.replace('&Ouml;', smart_str(u'Ö'))
        content = content.replace('&Uuml;', smart_str(u'Ü'))
        content = content.replace('&auml;', smart_str(u'ä'))
        content = content.replace('&ouml;', smart_str(u'ö'))
        content = content.replace('&uuml;', smart_str(u'ü'))
        content = content.replace('&szlig;', smart_str(u'ß'))
        root_node = ElementTree.fromstring(content)
        self.save_page(root_node)

        if self.verbosity >= NORMAL:
            print u"Productions added: %d" % self.stats['prods_added']
            print u"Productions updated: %d" % self.stats['prods_updated']
            print u"Productions skipped: %d" % self.stats['prods_skipped']
            print u"Events added: %d" % self.stats['events_added']
            print u"Events updated: %d" % self.stats['events_updated']
            print u"Events skipped: %d" % self.stats['events_skipped']
            print
