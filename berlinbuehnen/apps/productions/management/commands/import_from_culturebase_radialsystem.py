# -*- coding: UTF-8 -*-

import re
import requests
from xml.etree import ElementTree
from dateutil.parser import parse as parse_datetime
from optparse import make_option
import csv

from django.core.management.base import NoArgsCommand
from django.utils.encoding import smart_str, force_unicode
from django.utils.text import slugify
from django.db import models

from base_libs.utils.misc import get_unique_value

from berlinbuehnen.apps.productions.models import ProductionCategory
from berlinbuehnen.apps.productions.models import ProductionCharacteristics
from berlinbuehnen.apps.productions.models import Production
from berlinbuehnen.apps.productions.models import ProductionImage
from berlinbuehnen.apps.productions.models import Event
from berlinbuehnen.apps.productions.models import EventCharacteristics
from berlinbuehnen.apps.productions.models import EventImage
from berlinbuehnen.apps.people.models import Person, AuthorshipType
from berlinbuehnen.apps.sponsors.models import Sponsor

from _import_from_heimat_base_xml import LOCATIONS_TO_SKIP, STAGE_TO_LOCATION_MAPPER, PRODUCTION_VENUES, convert_location_title, CultureBaseLocation
from _import_from_culturebase_base_xml import ImportFromCulturebaseBase

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand, ImportFromCulturebaseBase):
    help = "Imports productions and events from Culturebase / RADIALSYSTEM V"

    def handle_noargs(self, *args, **options):
        from berlinbuehnen.apps.locations.models import Location
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        self.load_and_parse_locations()

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"RADIALSYSTEM V",
            defaults={
                'title_en': u"RADIALSYSTEM V",
                'slug': 'radialsystem-v',
                'street_address': u'Holzmarktstrasse 33',
                'postal_code': u'10243',
                'city': u'Berlin',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="culturebase_radialsystem_prods",
            defaults={
                'url': "https://export.culturebase.org/studio_38/event/radialsystem.xml",
                'title': "Culturebase Radialsystem Productions",
            },
        )

        self.authorship_types_de = AuthorshipType.objects.all().values_list("title_de", flat="True")

        r = requests.get(self.service.url, params={})
        if r.status_code != 200:
            print(u"Error status: %s" % r.status_code)
            return
        self.helper_dict = {
            'prefix': '{http://export.culturebase.org/schema/event/CultureBaseExport}'
        }

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
