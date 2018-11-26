# -*- coding: UTF-8 -*-
from datetime import datetime
from optparse import make_option
import requests

from django.db import models
from django.apps import apps
from django.utils.encoding import force_unicode
from django.core.management.base import NoArgsCommand

from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from ruhrbuehnen.apps.productions.models import (
    Production,
    ProductionImage,
    Event,
)

from ._import_base import ImportCommandMixin


class ImportFromEventimBase(NoArgsCommand, ImportCommandMixin):
    """ 
    Base command to extend for importing productions and events from different websites based on Eventim structure
    """
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--skip_images', action='store_true', help='Skips image downloads'
        ),
        make_option(
            '--update_images',
            action='store_true',
            help='Forces image-download updates'
        ),
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
        r = requests.get(self.service.url)
        if r.status_code != requests.codes.ok:
            self.all_feeds_alright = False
            self.stderr.write(
                u"Error status {} when trying to access {}\n".format(
                    r.status_code, self.service.url
                )
            )
            return
        try:
            event_dict_list = r.json()
        except ValueError as err:
            self.stderr.write(u"Parsing error: %s" % force_unicode(err))
            return
        self._production_counter = 0
        self.save_page(event_dict_list)

    def get_location_and_stage(self, event_dict):
        """
        Creates or gets and updates location and stage
        :param event_dict:
        :return: named tuple LocationAndStage(location, stage)
        """
        from collections import namedtuple
        LocationAndStage = namedtuple('LocationAndStage', ['location', 'stage'])
        stage_external_id = event_dict.get('LocationID')
        stage = self.STAGES_BY_EXTERNAL_ID.get(stage_external_id)
        location = stage and stage.location
        return LocationAndStage(location, stage)

    def cleanup_text(self, text):
        from BeautifulSoup import BeautifulStoneSoup
        from django.utils.html import strip_tags
        text = text.replace('<![CDATA[', '')
        text = text.replace(']]>', '')
        text = text.replace('</div>', '\n')
        text = strip_tags(text).strip()
        # convert HTML entities to Unicode
        text = BeautifulStoneSoup(
            text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES
        ).text
        return text

    def parse_and_use_texts(self, event_dict, instance):
        desc = event_dict.get('Description')
        if desc:
            desc = self.cleanup_text(desc)
            instance.description_de = desc
            instance.description_en = desc
        instance.description_de_markup_type = 'pt'
        instance.description_en_markup_type = 'pt'

    def save_page(self, event_dict_list):
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")
        image_mods = apps.get_app("image_mods")

        event_count = len(event_dict_list)

        for event_index, event_dict in enumerate(event_dict_list, 1):
            external_prod_id = event_dict.get('PlayID') or ""
            external_event_id = event_dict.get('EventID') or ""

            title_de = event_dict.get('Title').strip() or ""
            title_en = title_de

            if self.verbosity >= self.NORMAL:
                self.stdout.write(
                    u"%d/%d %s" % (event_index, event_count, title_de)
                )
                self.stdout.flush()

            location, stage = self.get_location_and_stage(event_dict)
            if not location or not stage:
                continue

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

            self.parse_and_use_texts(event_dict, prod)

            prod.save()
            self.production_ids_to_keep.add(prod.pk)

            for owner in self.owners:
                prod.set_owner(owner)

            start_datetime = datetime.utcfromtimestamp(
                int(event_dict.get("StartTimestamp"))
            )
            event.start_date = start_datetime.date()
            event.start_time = start_datetime.time()

            if self.in_program_of:
                prod.in_program_of.clear()
                prod.in_program_of.add(self.in_program_of)

            event.production = prod
            event.save()

            if location:
                event.play_locations.clear()
                event.play_locations.add(location)
            if stage:
                event.play_stages.clear()
                event.play_stages.add(stage)

            self.event_ids_to_keep.add(event.pk)

            if not self.skip_images:
                image_ids_to_keep = []
                # images can be of one of these formats:
                # [{...}, {...}] - this is a preferred one
                # {0: {...}, 1: {...}}
                images = event_dict.get('Images', [])
                for image_url in images:
                    if not image_url:
                        continue

                    image_external_id = "production-%s-%s" % (
                        prod.pk, image_url
                    )
                    image_mapper = None
                    try:
                        # get image model instance from saved mapper
                        image_mapper = self.service.objectmapper_set.get(
                            external_id=image_external_id,
                            content_type__app_label="productions",
                            content_type__model="productionimage",
                        )
                    except models.ObjectDoesNotExist:
                        # or create a new production and then create a mapper
                        mf = ProductionImage(production=prod)
                    else:
                        mf = image_mapper.content_object
                        if mf:
                            image_ids_to_keep.append(mf.pk)
                        else:
                            if self.update_images:
                                # restore image
                                mf = ProductionImage(production=prod)
                            else:
                                # skip deleted images
                                continue
                        if not self.update_images:
                            continue

                    filename = image_url.split("/")[-1]
                    if "?" in filename:
                        # clear the query parameters
                        filename = filename.split("?")[0]
                    image_response = requests.get(image_url)
                    if image_response.status_code in (
                        requests.codes.ok, requests.codes.not_modified
                    ):
                        image_mods.FileManager.delete_file_for_object(
                            mf,
                            field_name="path",
                        )
                        image_mods.FileManager.save_file_for_object(
                            mf,
                            filename,
                            image_response.content,
                            field_name="path",
                            subpath="productions/{}/events/gallery/".format(
                                event.production.slug
                            ),
                        )
                        mf.copyright_restrictions = "general_use"
                        mf.save()
                        image_ids_to_keep.append(mf.pk)

                        if not image_mapper:
                            image_mapper = ObjectMapper(
                                service=self.service,
                                external_id=image_external_id,
                            )
                        image_mapper.content_object = mf
                        image_mapper.save()

                for mf in prod.productionimage_set.exclude(
                    id__in=image_ids_to_keep
                ):
                    if mf.path:
                        # remove the file from the file system
                        image_mods.FileManager.delete_file(mf.path.name)
                    # delete image mapper
                    self.service.objectmapper_set.filter(
                        object_id=mf.pk,
                        content_type__app_label="productions",
                        content_type__model="productionimage",
                    ).delete()
                    # delete image model instance
                    mf.delete()

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
