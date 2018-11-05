# -*- coding: UTF-8 -*-
import re
from dateutil.parser import parse as parse_datetime
from decimal import Decimal
from optparse import make_option

from django.db import models
from django.apps import apps
from django.utils.encoding import force_unicode
from django.core.management.base import NoArgsCommand

from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from ruhrbuehnen.apps.productions.models import Production
from ruhrbuehnen.apps.productions.models import Event

from ._import_base import ImportCommandMixin


class ImportFromEventimBase(NoArgsCommand, ImportCommandMixin):
    """ 
    Base command to extend for importing productions and events from different websites based on Eventim structure
    """
    option_list = NoArgsCommand.option_list + (
        make_option('--skip_images', action='store_true', help='Skips image downloads'),
        make_option('--update_images', action='store_true', help='Forces image-download updates'),
    )
    help = "Imports productions and events from Eventim feeds"

    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3

    LOCATIONS_BY_EXTERNAL_ID = {}
    STAGES_BY_EXTERNAL_ID = {}

    in_program_of = None
    owners = []
    IMPORT_URL = None
    DEFAULT_PUBLISHING_STATUS = "published"  # "import"

    service = None

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", self.NORMAL))
        self.skip_images = options.get("skip_images")
        self.update_images = options.get("update_images")
        self.prepare()
        self.main()
        self.finalize()

    def prepare(self):
        raise NotImplementedError("Implement the prepare() method")

    def main(self):
        import requests
        from xml.etree import ElementTree
        r = requests.get(self.service.url, params={}, headers={
            'User-Agent': 'RuhrBuehnen',
        })
        if r.status_code != 200:
            self.all_feeds_alright = False
            self.stderr.write(u"Error status: %s" % r.status_code)
            return

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Importing Productions ===\n")

        try:
            root_node = ElementTree.fromstring(r.content)
        except ElementTree.ParseError as err:
            self.all_feeds_alright = False
            self.stderr.write(u"Parsing error: %s" % force_unicode(err))
            return

        self.save_page(root_node)

    def get_child_text(self, node, tag, **attrs):
        """
        returns the text from a child node with tag name and attributes

        Example:
        self.get_child_text(production_node, "Title", Language="de") == u"Nathan der  Weise"

        :param node: XML node which children to scan
        :param tag: the tag name of the children to get
        :param attrs: attributes of the children to match
        :return: text value of the selected child or empty string otherwise
        """
        for child_node in node.findall(tag):
            all_attributes_match = True
            for name, val in attrs.items():
                if child_node.get(name) != val:
                    all_attributes_match = False
                    break
            if all_attributes_match:
                # return force_unicode(child_node.text or u''.join([t for t in child_node.itertext()]))
                return force_unicode(u''.join([t for t in child_node.itertext()]))
        return u''

    def get_location_and_stage(self, venue_node):
        """
        Creates or gets and updates location and stage
        :param venue_node: XML node with venue data
        :return: named tuple LocationAndStage(location, stage)
        """
        from collections import namedtuple
        LocationAndStage = namedtuple('LocationAndStage', ['location', 'stage'])
        location_external_id = venue_node.find('spielort').get('id')
        stage_external_id = venue_node.find('spielstaette').get('id')

        location = self.LOCATIONS_BY_EXTERNAL_ID.get(location_external_id)
        stage = self.STAGES_BY_EXTERNAL_ID.get(stage_external_id)
        return LocationAndStage(location, stage)

    def cleanup_text(self, text):
        from BeautifulSoup import BeautifulStoneSoup
        from django.utils.html import strip_tags
        text = text.replace('<![CDATA[', '')
        text = text.replace(']]>', '')
        text = text.replace('</div>', '\n')
        text = strip_tags(text).strip()
        # convert HTML entities to Unicode
        text = BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES).text
        return text

    def parse_and_use_texts(self, xml_node, instance):
        desc = self.get_child_text(xml_node, 'hinweis')
        if desc:
            instance.description_de = desc
            instance.description_en = desc
        instance.description_de_markup_type = 'pt'
        instance.description_en_markup_type = 'pt'

    def save_page(self, root_node):
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")
        # image_mods = apps.get_app("image_mods")

        event_nodes = root_node.findall('veranstaltung')
        event_count = len(event_nodes)

        for event_index, event_node in enumerate(event_nodes, 1):
            external_prod_id = self.get_child_text(event_node, 'produktion')
            external_event_id = event_node.get("id") or event_node.get("index")

            title_de = self.get_child_text(event_node, 'titel').replace('\n', ' ').strip()
            title_en = title_de

            if self.verbosity >= self.NORMAL:
                self.stdout.write(u"%d/%d %s" % (event_index, event_count, title_de))
                self.stdout.flush()

            mapper = None
            try:
                # get production from saved mapper
                mapper = self.service.objectmapper_set.get(
                    external_id=external_prod_id,
                    content_type__app_label="productions",
                    content_type__model="production",
                )
            except models.ObjectDoesNotExist:
                # or create a new production and then create a mapper
                prod = Production(status=self.DEFAULT_PUBLISHING_STATUS)
                prod.import_source = self.service
            else:
                prod = mapper.content_object
                self.production_ids_to_keep.add(prod.pk)
                if not prod:
                    # if production was deleted after import,
                    # don't import it again
                    self.stats['prods_skipped'] += 1
                    continue
                if prod.status == "trashed":
                    self.stats['prods_untrashed'] += 1

            if prod.no_overwriting:
                self.stats['prods_skipped'] += 1
                continue

            event_mapper = None
            try:
                # get production from saved mapper
                event_mapper = self.service.objectmapper_set.get(
                    external_id=external_event_id,
                    content_type__app_label="productions",
                    content_type__model="event",
                )
            except models.ObjectDoesNotExist:
                # or create a new production and then create a mapper
                event = Event(production=prod)
            else:
                event = event_mapper.content_object
                if event:
                    self.event_ids_to_keep.add(event.pk)
                else:
                    # skip deleted events
                    self.stats['events_skipped'] += 1
                    continue

            if not title_de:  # skip productions without title
                self.stats['prods_skipped'] += 1
                continue

            prod.status = self.DEFAULT_PUBLISHING_STATUS
            prod.title_de = title_de
            prod.title_en = title_en or title_de

            prod.slug = get_unique_value(
                Production,
                better_slugify(prod.title_de)[:200] or u"production",
                instance_pk=prod.pk,
            )

            self.parse_and_use_texts(event_node, prod)

            prod.save()
            self.production_ids_to_keep.add(prod.pk)

            for owner in self.owners:
                prod.set_owner(owner)

            if self.in_program_of:
                prod.in_program_of.clear()
                prod.in_program_of.add(self.in_program_of)

            start_datetime_string = self.get_child_text(event_node, 'datum')
            if re.search(r"^\d\d\d\d", start_datetime_string):
                # ISO date format
                start_datetime = parse_datetime(start_datetime_string)
            else:
                # German date format
                start_datetime = parse_datetime(start_datetime_string, dayfirst=True)

            event.start_date = start_datetime.date()
            event.start_time = start_datetime.time()

            min_price = Decimal("999999.99")
            max_price = Decimal("0.00")
            for price_node in event_node.findall('preis'):
                price = Decimal(force_unicode(u''.join([t for t in price_node.itertext()])).replace(',', '.'))
                min_price = min(price, min_price)
                max_price = max(price, max_price)

            event.price_from = None
            if min_price != Decimal("999999.99"):
                event.price_from = min_price

            event.price_till = None
            if max_price != Decimal("0.00"):
                event.price_till = max_price

            event.production = prod
            event.save()

            location, stage = self.get_location_and_stage(event_node)
            if location:
                event.play_locations.clear()
                event.play_locations.add(location)
            if stage:
                event.play_stages.clear()
                event.play_stages.add(stage)

            self.event_ids_to_keep.add(event.pk)

            if not event_mapper:
                event_mapper = ObjectMapper(
                    service=self.service,
                    external_id=external_event_id,
                )
                event_mapper.content_object = event
                event_mapper.save()
                self.stats['events_added'] += 1
            else:
                self.stats['events_updated'] += 1

            if not mapper:
                mapper = ObjectMapper(
                    service=self.service,
                    external_id=external_prod_id,
                )
                mapper.content_object = prod
                mapper.save()
                self.stats['prods_added'] += 1
            else:
                self.stats['prods_updated'] += 1

            prod.update_actual_date_and_time()
