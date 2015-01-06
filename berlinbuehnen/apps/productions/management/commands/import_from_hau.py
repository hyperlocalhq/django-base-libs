# -*- coding: UTF-8 -*-

import re
import requests
from xml.etree import ElementTree
from dateutil.parser import parse as parse_datetime
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.utils.encoding import smart_str, force_unicode
from django.utils.text import slugify
from django.db import models

from base_libs.utils.misc import get_unique_value

from berlinbuehnen.apps.productions.models import ProductionCategory
from berlinbuehnen.apps.productions.models import Production
from berlinbuehnen.apps.productions.models import ProductionImage
from berlinbuehnen.apps.productions.models import Event
from berlinbuehnen.apps.productions.models import EventImage
from berlinbuehnen.apps.people.models import Person

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells Django to NOT download images.'),
    )
    help = "Imports productions and events from HAU"

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        Service = models.get_model("external_services", "Service")

        self.CATEGORY_MAPPER = {
        }

        self.service, created = Service.objects.get_or_create(
            sysname="hau_prods",
            defaults={
                'url': "http://www.hebbel-am-ufer.de/cbstage/export.xml",
                'title': "HAU Productions",
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
        all_attributes_match = True
        for child_node in node.findall(tag):
            for name, val in attrs.items():
                if child_node.get(name) != val:
                    all_attributes_match = False
                    break
            if all_attributes_match:
                return force_unicode(child_node.text)
        return u""

    def create_or_update_location(self, venue_node):
        from berlinbuehnen.apps.locations.models import Location
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        city_suffix = re.compile(r' \[[^\]]+\]')

        return None, False # TODO: finalize
        # TODO: decide whether to leave title handling as external id
        external_id = venue_node.get('Id') or self.get_child_text(venue_node, 'Name')
        mapper = None
        try:
            # get exhibition from saved mapper
            mapper = self.service.objectmapper_set.get(
                external_id=external_id,
                content_type__app_label="locations",
                content_type__model="location",
            )
        except models.ObjectDoesNotExist:
            # or create a new exhibition and then create a mapper
            location = Location()
        else:
            location = mapper.content_object
            if not location:
                # if exhibition was deleted after import,
                # don't import it again
                return None, False

        location.title = self.get_child_text(venue_node, 'Name')
        lat = self.get_child_text(venue_node, 'Latitude')
        if lat:
            location.latitude = float(lat)
        lng = self.get_child_text(venue_node, 'Longitude')
        if lng:
            location.longitude = float(lng)
        location.street_address = self.get_child_text(venue_node, 'Street')
        location.postal_code = self.get_child_text(venue_node, 'ZipCode')
        location.city = city_suffix.sub("", self.get_child_text(venue_node, 'City') or "")
        location.save()

        if not mapper:
            mapper = ObjectMapper(
                service=self.service,
                external_id=external_id,
            )
            mapper.content_object = location
            mapper.save()
            return location, True

        return location, False

    def save_page(self, root_node):
        import time
        from filebrowser.models import FileDescription
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        image_mods = models.get_app("image_mods")

        for prod_node in root_node.findall('production'):
            external_prod_id = prod_node.get('foreignId')

            mapper = None
            try:
                # get exhibition from saved mapper
                mapper = self.service.objectmapper_set.get(
                    external_id=external_prod_id,
                    content_type__app_label="productions",
                    content_type__model="production",
                )
            except models.ObjectDoesNotExist:
                # or create a new exhibition and then create a mapper
                prod = Production()
            else:
                prod = mapper.content_object
                if not prod:
                    # if exhibition was deleted after import,
                    # don't import it again
                    self.stats['prods_skipped'] += 1
                    continue
                # else:
                #     if parse_datetime(exhibition_dict['lastaction'], ignoretz=True) < datetime.now() - timedelta(days=1):
                #         self.stats['prods_skipped'] += 1
                #         continue

            title_de = self.get_child_text(prod_node, 'title', languageId="1")
            title_en = self.get_child_text(prod_node, 'title', languageId="2")
            prod.title_de = title_de
            prod.title_en = title_en or title_de
            prod.website = prod_node.get('url')

            if self.verbosity > NORMAL:
                print smart_str(title_de) + " | " + smart_str(title_en)

            prod.slug = get_unique_value(Production, slugify(prod.title_de))

            for text_node in prod_node.findall('./mediaText'):
                text_cat_id = int(text_node.get('relation'))
                text_de = self.get_child_text(text_node, 'text', languageId="1")
                text_en = self.get_child_text(text_node, 'text', languageId="2")
                if text_cat_id == 14:  # Beschreibungstext kurz
                    prod.teaser_de = text_de
                    prod.teaser_de_markup_type = 'pt'
                    prod.teaser_en = text_en
                    prod.teaser_en_markup_type = 'pt'
                elif text_cat_id == 15:  # Beschreibungstext lang
                    pass

            prod.save()

            venue_node = prod_node.find('location')
            if venue_node:
                location, created = self.create_or_update_location(venue_node)
                if location:
                    prod.play_locations.clear()
                    prod.play_locations.add(location)

            if not self.skip_images and not prod.productionimage_set.count():
                for picture_node in prod_node.findall('picture'):
                    image_url = picture_node.get('url')
                    mf = ProductionImage(production=prod)
                    filename = image_url.split("/")[-1]
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_mods.FileManager.save_file_for_object(
                            mf,
                            filename,
                            image_response.content,
                            field_name="path",
                            subpath="productions/%s/gallery/" % prod.slug,
                        )
                        if picture_node.get('publishType') == "0":  # TODO: clarify publishType statuses for pictures
                            mf.copyright_restrictions = "general_use"
                        else:
                            mf.copyright_restrictions = "protected"
                        mf.save()
                        try:
                            file_description = FileDescription.objects.filter(
                                file_path=mf.path,
                            ).order_by("pk")[0]
                        except:
                            file_description = FileDescription(file_path=mf.path)

                        file_description.title_de = self.get_child_text(picture_node, 'text', languageId="1")
                        file_description.title_en = self.get_child_text(picture_node, 'text', languageId="2")
                        file_description.author = picture_node.get('photographer').replace("Foto: ", "")
                        file_description.copyright_limitations = picture_node.get('copyright')
                        file_description.save()
                        time.sleep(1)

            for category_node in prod_node.findall('category'):
                internal_cat_id = self.CATEGORY_MAPPER.get(int(category_node.text), None)
                if internal_cat_id:
                    prod.categories.add(ProductionCategory.objects.get(pk=internal_cat_id))

            if not prod.productioninvolvement_set.count():
                for person_node in prod_node.findall('person'):
                    role_de = self.get_child_text(person_node, 'mediaText/text', languageId="1")
                    role_en = self.get_child_text(person_node, 'mediaText/text', languageId="2")
                    for person_name in person_node.get('personFreetext').split(", "):
                        first_name, last_name = person_name.rsplit(" ", 1)
                        p, created = Person.objects.get_or_create(
                            first_name=first_name,
                            last_name=last_name,
                            defaults={
                                'involvement_role_de': role_de,
                                'involvement_role_en': role_en,
                            }
                        )
                        prod.productioninvolvement_set.create(
                            person=p,
                            involvement_role_de=role_de,
                            involvement_role_en=role_en,
                            sort_order=person_node.get('position'),
                        )

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

            for event_node in prod_node.findall('event'):

                external_event_id = event_node.get('foreignId')

                event_mapper = None
                try:
                    # get exhibition from saved mapper
                    event_mapper = self.service.objectmapper_set.get(
                        external_id=external_event_id,
                        content_type__app_label="productions",
                        content_type__model="event",
                    )
                except models.ObjectDoesNotExist:
                    # or create a new exhibition and then create a mapper
                    event = Event()
                else:
                    event = event_mapper.content_object
                    if not event:
                        # if exhibition was deleted after import,
                        # don't import it again
                        self.stats['events_skipped'] += 1
                        continue

                event.production = prod

                start_datetime = parse_datetime(event_node.get('datetime'))
                event.start_date = start_datetime.date()
                event.start_time = start_datetime.time()
                duration_str = event_node.get('duration')
                if duration_str:
                    event.duration = int(duration_str)

                price_node = event_node.find('price')
                if price_node is not None:
                    event.price_from = price_node.get('minPrice').replace(',', '.')
                    event.price_till = price_node.get('maxPrice').replace(',', '.')
                    event.tickets_website = price_node.get('url')

                if event_node.get('takingPlace') == "1":
                    event.event_status = 'takes_place'
                else:
                    event.event_status = 'canceled'

                for text_node in event_node.findall('text'):
                    text_cat_id = int(text_node.get('relation'))
                    text_de = self.get_child_text(text_node, 'text', languageId="1")
                    text_en = self.get_child_text(text_node, 'text', languageId="2")
                    if text_cat_id == 14:  # Beschreibungstext kurz
                        event.teaser_de = text_de
                        event.teaser_de_markup_type = 'pt'
                        event.teaser_en = text_en
                        event.teaser_en_markup_type = 'pt'
                    elif text_cat_id == 15:  # Beschreibungstext lang
                        pass

                event.save()

                if not self.skip_images and not event.eventimage_set.count():
                    for picture_node in event_node.findall('picture'):
                        image_url = self.get_child_text(picture_node, 'Url')
                        mf = EventImage(event=event)
                        filename = image_url.split("/")[-1]
                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            image_mods.FileManager.save_file_for_object(
                                mf,
                                filename,
                                image_response.content,
                                field_name="path",
                                subpath="productions/%s/events/%s/gallery/" % (prod.slug, event.pk),
                            )
                            if picture_node.get('publishType') == "0":
                                mf.copyright_restrictions = "general_use"
                            else:
                                mf.copyright_restrictions = "protected"
                            mf.save()
                            try:
                                file_description = FileDescription.objects.filter(
                                    file_path=mf.path,
                                ).order_by("pk")[0]
                            except:
                                file_description = FileDescription(file_path=mf.path)

                            file_description.title_de = self.get_child_text(picture_node, 'text', languageId="1")
                            file_description.title_en = self.get_child_text(picture_node, 'text', languageId="2")
                            file_description.author = picture_node.get('photographer').replace("Foto: ", "")
                            file_description.copyright_limitations = picture_node.get('copyright')
                            file_description.save()
                            time.sleep(1)

                venue_node = event_node.find('location')
                if venue_node:
                    location, created = self.create_or_update_location(venue_node)
                    if location:
                        event.play_locations.clear()
                        event.play_locations.add(location)

                if not event.eventinvolvement_set.count():
                    for person_node in event_node.findall('person'):
                        role_de = self.get_child_text(person_node, 'mediaText/text', languageId="1")
                        role_en = self.get_child_text(person_node, 'mediaText/text', languageId="2")
                        for person_name in person_node.get('personFreetext').split(", "):
                            first_name, last_name = person_name.rsplit(" ", 1)
                            p, created = Person.objects.get_or_create(
                                first_name=first_name,
                                last_name=last_name,
                                defaults={
                                    'involvement_role_de': role_de,
                                    'involvement_role_en': role_en,
                                }
                            )
                            event.eventinvolvement_set.create(
                                person=p,
                                involvement_role_de=role_de,
                                involvement_role_en=role_en,
                                sort_order=person_node.get('position'),
                            )


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
