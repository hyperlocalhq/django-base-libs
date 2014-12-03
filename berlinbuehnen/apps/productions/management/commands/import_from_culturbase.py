# -*- coding: UTF-8 -*-

import os
import requests
from xml.etree import ElementTree
from StringIO import StringIO

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils.encoding import smart_str, force_unicode
from django.conf import settings
from django.core.files import File
from django.utils.text import slugify

from base_libs.utils.misc import get_unique_value

from berlinbuehnen.apps.productions.models import Production
from berlinbuehnen.apps.productions.models import Event

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3

class Command(BaseCommand):
    help = "Imports productions and events from Culturebase"

    def handle(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))

        r = requests.get(
            "https://export.culturebase.org/cb-event/event/hamburger_staatstheater.xml",
            params={}
        )
        self.helper_dict = {
            'prefix': '{http://export.culturebase.org/schema/event/CultureBaseExport}'
        }

        if self.verbosity >= NORMAL:
            print u"=== Productions imported ==="

        root = ElementTree.fromstring(r.content)
        self.save_page(root)

    def get_child_text(self, node, tag):
        child_node = node.find('%(prefix)s%(tag)s' % dict(tag=tag, **self.helper_dict))
        if child_node is not None:
            return child_node.text

    def save_page(self, root):
        for prod_node in root.findall('%(prefix)sProduction' % self.helper_dict):
            prod = Production()

            title_de = u""
            title_en = u""
            for title_node in prod_node.findall('%(prefix)sTitle' % self.helper_dict):
                if title_node.get('Language') == "de":
                    title_de = title_node.text
                elif title_node.get('Language') == "en":
                    title_en = title_node.text
            prod.title_de = force_unicode(title_de)
            prod.title_en = force_unicode(title_en or title_de)

            print smart_str(title_de) + " | " + smart_str(title_en)

            prod.slug = get_unique_value(Production, slugify(prod.title_de))

            for category_id_node in prod_node.findall('%(prefix)sContentCategory/%(prefix)sCategoryId' % self.helper_dict):
                print int(category_id_node.text)
                # TODO: map category ids to real categories

            venue_node = prod_node.find('%(prefix)sVenue' % self.helper_dict)
            if venue_node:
                print venue_node.get('Id')
                print smart_str(self.get_child_text(venue_node, 'Name'))
                print smart_str(self.get_child_text(venue_node, 'Latitude'))
                print smart_str(self.get_child_text(venue_node, 'Longitude'))
                print smart_str(self.get_child_text(venue_node, 'Street'))
                print smart_str(self.get_child_text(venue_node, 'ZipCode'))
                print smart_str(self.get_child_text(venue_node, 'City'))
