# -*- coding: UTF-8 -*-

import os
import requests
import shutil
from xml.etree import ElementTree
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db import models
from django.utils.encoding import smart_str, force_unicode
from django.conf import settings

from import_base import ImportFromHeimatBase

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

        self.delete_existing_productions_and_events(self.service)

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

    def should_reimport(self, service):
        from dateutil.parser import parse

        # read the last-modified header from the feed
        response = requests.head(self.IMPORT_URL)
        last_modified_str = response.headers.get('last-modified', '')
        if not last_modified_str:
            return False
        feed_last_modified = parse(last_modified_str)

        # compare feed_last_modified with the last updated production creation date
        mappers = service.objectmapper_set.filter(content_type__model__iexact="production").order_by('-pk')
        if mappers:
            productions_last_modified = mappers[0].content_object.creation_date
            return feed_last_modified > productions_last_modified
        return True

    def delete_existing_productions_and_events(self, service):
        if self.verbosity >= NORMAL:
            print u"=== Deleting existing productions ==="

        # deleting productions and their mappers
        prods_count = service.objectmapper_set.filter(content_type__model__iexact="production").count()
        for prod_index, mapper in enumerate(service.objectmapper_set.filter(content_type__model__iexact="production"), 1):
            if mapper.content_object:
                if self.verbosity >= NORMAL:
                    print "%d/%d %s | %s" % (prod_index, prods_count, smart_str(mapper.content_object.title_de), smart_str(mapper.content_object.title_en))
                if mapper.content_object.no_overwriting:  # don't delete items with no_overwriting == True
                    continue

                # delete media files
                try:
                    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, "productions", mapper.content_object.slug))
                except OSError as err:
                    pass

                mapper.content_object.delete()
            mapper.delete()

        # deleting events and their mappers
        for mapper in service.objectmapper_set.filter(content_type__model__iexact="event"):
            if mapper.content_object:
                if mapper.content_object.production.no_overwriting:  # don't delete items with no_overwriting == True
                    continue

                mapper.content_object.delete()
            mapper.delete()
