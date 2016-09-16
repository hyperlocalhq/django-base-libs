# -*- coding: UTF-8 -*-

import requests
import json
import re
from dateutil.parser import parse as parse_datetime
from optparse import make_option
from decimal import Decimal, InvalidOperation

from django.core.management.base import NoArgsCommand
from django.db import models
from django.utils.encoding import smart_str, force_unicode

from import_base import ImportFromHeimatBase

from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from berlinbuehnen.apps.productions.models import ProductionCategory
from berlinbuehnen.apps.productions.models import ProductionCharacteristics
from berlinbuehnen.apps.productions.models import Production
from berlinbuehnen.apps.productions.models import ProductionImage
from berlinbuehnen.apps.productions.models import ProductionSponsor
from berlinbuehnen.apps.productions.models import Event
from berlinbuehnen.apps.productions.models import EventCharacteristics
from berlinbuehnen.apps.productions.models import EventImage
from berlinbuehnen.apps.productions.models import EventSponsor
from berlinbuehnen.apps.people.models import Person

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand, ImportFromHeimatBase):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells Django to NOT download images.'),
    )
    help = "Imports productions and events from Maxim Gorki Theater"

    # IMPORT_URL = "http://www.gorki.de/cbstage/export.xml"
    IMPORT_URL = "http://production.gorki.de/gorki/export?token=DSIFHSDFIEWJSDF9734adadsd342342sdf23432esd9uejdvnpaodhefghdsnhdffgasncvqw3dsf3fsdf"

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

        json_document = json.loads(r.content)
        self.save_json_page(json_document)

        if self.verbosity >= NORMAL:
            print u"Productions added: %d" % self.stats['prods_added']
            print u"Productions updated: %d" % self.stats['prods_updated']
            print u"Productions skipped: %d" % self.stats['prods_skipped']
            print u"Events added: %d" % self.stats['events_added']
            print u"Events updated: %d" % self.stats['events_updated']
            print u"Events skipped: %d" % self.stats['events_skipped']
            print

    def save_json_page(self, json_document):
        from filebrowser.models import FileDescription
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        image_mods = models.get_app("image_mods")

        productions = json_document['productions']
        prods_count = len(productions)

        for prod_index_string, prod_node in productions.items():
            prod_index = int(prod_index_string)
            external_prod_id = prod_node.get('foreignId', prod_index)

            title_de = prod_node['title_de'].replace('\n', ' ').strip()
            title_en = prod_node['title_en'].replace('\n', ' ').strip()

            if self.verbosity >= NORMAL:
                print "%d/%d %s | %s" % (prod_index, prods_count, smart_str(title_de), smart_str(title_en))

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
                prod = Production(status=self.DEFAULT_PUBLISHING_STATUS)
                prod.import_source = self.service
            else:
                prod = mapper.content_object
                self.production_ids_to_keep.add(prod.pk)
                if not prod or prod.status == "trashed":
                    # if exhibition was deleted after import,
                    # don't import it again
                    self.stats['prods_skipped'] += 1
                    continue
                    # else:
                    #     if parse_datetime(exhibition_dict['lastaction'], ignoretz=True) < datetime.now() - timedelta(days=1):
                    #         self.stats['prods_skipped'] += 1
                    #         continue

            if prod.no_overwriting:
                self.stats['prods_skipped'] += 1
                continue

            if not title_de:  # skip productions without title
                self.stats['prods_skipped'] += 1
                continue

            prod.status = self.DEFAULT_PUBLISHING_STATUS
            prod.title_de = title_de
            prod.title_en = title_en or title_de
            prod.website_de = prod.website_en = prod_node.get('url')

            prod.slug = get_unique_value(Production, better_slugify(prod.title_de) or u"production", instance_pk=prod.pk)

            self.parse_and_use_texts(prod_node, prod)

            prod.save()
            self.production_ids_to_keep.add(prod.pk)

            venue_node = prod_node.find('location')
            if venue_node is not None:
                location, stage = self.get_updated_location_and_stage(venue_node)
                if location:
                    prod.play_locations.clear()
                    prod.play_locations.add(location)
                # else:
                #    prod.location_title = venue_node.text
                #    prod.save()
                if stage:
                    if isinstance(stage, dict):
                        prod.location_title = stage['title']
                        prod.street_address = stage.get('street_address', u'')
                        prod.postal_code = stage.get('postal_code', u'')
                        prod.city = stage.get('city', u'Berlin')
                        prod.save()
                    else:
                        prod.play_stages.clear()
                        prod.play_stages.add(stage)

            institution_node = prod_node.find('institution')
            if institution_node is not None:
                location, stage = self.get_updated_location_and_stage(institution_node)
                if location:
                    prod.in_program_of.clear()
                    prod.in_program_of.add(location)
                else:
                    prod.organizers = institution_node.text
                    prod.save()

            if self.in_program_of:
                prod.in_program_of.add(self.in_program_of)

            for owner in self.owners:
                prod.set_owner(owner)

            if not self.skip_images:
                image_ids_to_keep = []
                for picture_node in prod_node.findall('./picture'):
                    image_url = picture_node.get('url')
                    if not image_url.startswith('http'):
                        continue

                    image_external_id = "prod-%s-%s" % (prod.pk, image_url)
                    image_mapper = None
                    try:
                        # get image model instance from saved mapper
                        image_mapper = self.service.objectmapper_set.get(
                            external_id=image_external_id,
                            content_type__app_label="productions",
                            content_type__model="productionimage",
                        )
                    except models.ObjectDoesNotExist:
                        # or create a new exhibition and then create a mapper
                        mf = ProductionImage(production=prod)
                    else:
                        mf = image_mapper.content_object
                        if mf:
                            image_ids_to_keep.append(mf.pk)
                        continue

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
                        if picture_node.get('publishType') == "1":
                            mf.copyright_restrictions = "general_use"
                        elif picture_node.get('publishType') == "3":
                            mf.copyright_restrictions = "protected"
                        mf.save()
                        image_ids_to_keep.append(mf.pk)
                        try:
                            file_description = FileDescription.objects.filter(
                                file_path=mf.path,
                            ).order_by("pk")[0]
                        except:
                            file_description = FileDescription(file_path=mf.path)

                        file_description.title_de = self.get_child_text(picture_node, 'title',
                                                                        languageId="1") or self.get_child_text(picture_node,
                                                                                                               'text',
                                                                                                               languageId="1")
                        file_description.title_en = self.get_child_text(picture_node, 'title',
                                                                        languageId="2") or self.get_child_text(picture_node,
                                                                                                               'text',
                                                                                                               languageId="2")
                        file_description.author = (picture_node.get('photographer') or u"").replace("Foto: ", "")
                        file_description.copyright_limitations = picture_node.get('copyright')
                        file_description.save()

                        if not image_mapper:
                            image_mapper = ObjectMapper(
                                service=self.service,
                                external_id=image_external_id,
                            )
                            image_mapper.content_object = mf
                            image_mapper.save()

                for mf in prod.productionimage_set.exclude(id__in=image_ids_to_keep):
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

            prod.categories.clear()
            for category_node in prod_node.findall('category'):
                internal_cat_id = self.CATEGORY_MAPPER.get(int(category_node.text), None)
                if internal_cat_id:
                    cats = ProductionCategory.objects.filter(pk=internal_cat_id)
                    if cats:
                        prod.categories.add(cats[0])
                        if cats[0].parent:
                            prod.categories.add(cats[0].parent)

            prod.characteristics.clear()
            for status_id_node in prod_node.findall('statusId'):
                if status_id_node.text:
                    internal_ch_slug = self.PRODUCTION_CHARACTERISTICS_MAPPER.get(int(status_id_node.text), None)
                    if internal_ch_slug:
                        prod.characteristics.add(ProductionCharacteristics.objects.get(slug=internal_ch_slug))

            prod.productioninvolvement_set.all().delete()
            for person_node in prod_node.findall('person'):
                role_de = self.get_child_text(person_node, 'mediaText/text', languageId="1")
                role_en = self.get_child_text(person_node, 'mediaText/text', languageId="2")
                if not role_de and int(person_node.get('roleId')) in self.ROLE_ID_MAPPER:
                    role_de, role_en = self.ROLE_ID_MAPPER[int(person_node.get('roleId'))]
                for person_name in re.split(r'\s*[/,]\s*', person_node.get('personFreetext')):
                    first_and_last_name = person_name
                    if u" " in first_and_last_name:
                        first_name, last_name = first_and_last_name.rsplit(" ", 1)
                    else:
                        first_name = ""
                        last_name = first_and_last_name
                    p, created = Person.objects.get_first_or_create(
                        first_name=first_name,
                        last_name=last_name,
                    )
                    prod.productioninvolvement_set.create(
                        person=p,
                        involvement_role_de=role_de,
                        involvement_role_en=role_en,
                        imported_sort_order=person_node.get('position'),
                    )
            for sort_order, item in enumerate(prod.productioninvolvement_set.order_by('imported_sort_order'), 0):
                item.sort_order = sort_order
                item.save()

            # delete old sponsors
            for sponsor in prod.productionsponsor_set.all():
                if sponsor.image:
                    try:
                        image_mods.FileManager.delete_file(sponsor.image.path)
                    except OSError:
                        pass
                sponsor.delete()
            # add new sponsors
            for sponsor_node in prod_node.findall('./sponsor'):
                sponsor = ProductionSponsor(
                    production=prod,
                    title_de=self.get_child_text(sponsor_node, 'title', languageId="1"),
                    title_en=self.get_child_text(sponsor_node, 'title', languageId="2"),
                    website=sponsor_node.get('linkURL'),
                )
                sponsor.save()
                image_url = sponsor_node.get('pictureURL')
                if image_url:
                    filename = image_url.split("/")[-1]
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_mods.FileManager.save_file_for_object(
                            sponsor,
                            filename,
                            image_response.content,
                            field_name="image",
                            subpath="productions/{}/sponsors/".format(prod.slug),
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
                if not external_event_id:
                    external_event_id = u"%s_%s" % (external_prod_id, event_node.get('datetime'))

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
                    if event:
                        self.event_ids_to_keep.add(event.pk)
                    else:
                        # skip deleted events
                        self.stats['events_skipped'] += 1
                        continue

                event.production = prod

                start_datetime = parse_datetime(event_node.get('datetime'), dayfirst=True)
                event.start_date = start_datetime.date()
                event.start_time = start_datetime.time()
                duration_str = event_node.get('duration')
                if duration_str:
                    event.duration = int(duration_str)

                price_node = event_node.find('price')
                if price_node is not None:
                    price_from = (price_node.get('minPrice') or u"").replace(',', '.') or None
                    if price_from == u"Eintritt frei":
                        event.free_entrance = True
                    elif price_from is not None:
                        try:
                            # in case of price conversion errors, save the price into price_information fields
                            Decimal(price_from)
                        except InvalidOperation:
                            if price_from not in event.price_information_de:
                                event.price_information_de += '\n' + price_from
                            if price_from not in event.price_information_en:
                                event.price_information_en += '\n' + price_from
                        else:
                            event.price_from = price_from

                    price_till = (price_node.get('maxPrice') or u"").replace(',', '.') or None
                    if price_till is not None:
                        try:
                            # in case of price conversion errors, save the price into price_information fields
                            Decimal(price_till)
                        except InvalidOperation:
                            if price_till not in event.price_information_de:
                                event.price_information_de += '\n' + price_till
                            if price_till not in event.price_information_en:
                                event.price_information_en += '\n' + price_till
                        else:
                            event.price_till = price_till
                    event.tickets_website = price_node.get('url')

                if event_node.get('takingPlace'):
                    flag_status = int(event_node.get('takingPlace'))
                    if flag_status == 0:  # fällt aus
                        event.event_status = 'canceled'
                    elif flag_status == 1:  # findet statt
                        event.event_status = 'takes_place'
                    elif flag_status == 2:  # ausverkauft
                        event.ticket_status = 'sold_out'

                self.parse_and_use_texts(event_node, event)

                event.save()
                self.event_ids_to_keep.add(event.pk)

                if not self.skip_images:
                    image_ids_to_keep = []
                    for picture_node in event_node.findall('picture'):
                        image_url = self.get_child_text(picture_node, 'Url')
                        if not image_url.startswith('http'):
                            continue

                        image_external_id = "event-%s-%s" % (event.pk, image_url)
                        image_mapper = None
                        try:
                            # get image model instance from saved mapper
                            image_mapper = self.service.objectmapper_set.get(
                                external_id=image_external_id,
                                content_type__app_label="productions",
                                content_type__model="eventimage",
                            )
                        except models.ObjectDoesNotExist:
                            # or create a new exhibition and then create a mapper
                            mf = EventImage(event=event)
                        else:
                            mf = image_mapper.content_object
                            if mf:
                                image_ids_to_keep.append(mf.pk)
                            continue

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
                            if picture_node.get('publishType') == "1":
                                mf.copyright_restrictions = "general_use"
                            elif picture_node.get('publishType') == "3":
                                mf.copyright_restrictions = "protected"
                            mf.save()
                            image_ids_to_keep.append(mf.pk)
                            try:
                                file_description = FileDescription.objects.filter(
                                    file_path=mf.path,
                                ).order_by("pk")[0]
                            except:
                                file_description = FileDescription(file_path=mf.path)

                            file_description.title_de = self.get_child_text(picture_node, 'title',
                                                                            languageId="1") or self.get_child_text(
                                picture_node, 'text', languageId="1")
                            file_description.title_en = self.get_child_text(picture_node, 'title',
                                                                            languageId="2") or self.get_child_text(
                                picture_node, 'text', languageId="2")
                            file_description.author = (picture_node.get('photographer') or u"").replace("Foto: ", "")
                            file_description.copyright_limitations = picture_node.get('copyright')
                            file_description.save()

                            if not image_mapper:
                                image_mapper = ObjectMapper(
                                    service=self.service,
                                    external_id=image_external_id,
                                )
                                image_mapper.content_object = mf
                                image_mapper.save()

                    for mf in event.eventimage_set.exclude(pk__in=image_ids_to_keep):
                        if mf.path:
                            # remove the file from the file system
                            image_mods.FileManager.delete_file(mf.path.name)
                        # delete image mapper
                        self.service.objectmapper_set.filter(
                            object_id=mf.pk,
                            content_type__app_label="productions",
                            content_type__model="eventimage",
                        ).delete()
                        # delete image model instance
                        mf.delete()

                venue_node = event_node.find('location')
                if venue_node is not None:
                    location, stage = self.get_updated_location_and_stage(venue_node)
                    if location:
                        event.play_locations.clear()
                        event.play_locations.add(location)
                    # else:
                    #    event.location_title = venue_node.text
                    #    event.save()

                    if stage:
                        if isinstance(stage, dict):
                            event.location_title = stage['title']
                            event.street_address = stage.get('street_address', u'')
                            event.postal_code = stage.get('postal_code', u'')
                            event.city = stage.get('city', u'Berlin')
                            event.save()
                        else:
                            event.play_stages.clear()
                            event.play_stages.add(stage)

                event.characteristics.clear()
                for status_id_node in event_node.findall('statusId'):
                    if status_id_node.text:
                        internal_ch_slug = self.EVENT_CHARACTERISTICS_MAPPER.get(int(status_id_node.text), None)
                        if internal_ch_slug:
                            event.characteristics.add(EventCharacteristics.objects.get(slug=internal_ch_slug))

                event.eventinvolvement_set.all().delete()
                for person_node in event_node.findall('person'):
                    role_de = self.get_child_text(person_node, 'mediaText/text', languageId="1")
                    role_en = self.get_child_text(person_node, 'mediaText/text', languageId="2")
                    if not role_de and int(person_node.get('roleId')) in self.ROLE_ID_MAPPER:
                        role_de, role_en = self.ROLE_ID_MAPPER[int(person_node.get('roleId'))]
                    for person_name in re.split(r'\s*[/,]\s*', person_node.get('personFreetext')):
                        first_and_last_name = person_name
                        if u" " in first_and_last_name:
                            first_name, last_name = first_and_last_name.rsplit(" ", 1)
                        else:
                            first_name = ""
                            last_name = first_and_last_name
                        p, created = Person.objects.get_first_or_create(
                            first_name=first_name,
                            last_name=last_name,
                        )
                        event.eventinvolvement_set.create(
                            person=p,
                            involvement_role_de=role_de,
                            involvement_role_en=role_en,
                            imported_sort_order=person_node.get('position'),
                        )
                for sort_order, item in enumerate(event.eventinvolvement_set.order_by('imported_sort_order'), 0):
                    item.sort_order = sort_order
                    item.save()

                # delete old sponsors
                for sponsor in event.eventsponsor_set.all():
                    if sponsor.image:
                        try:
                            image_mods.FileManager.delete_file(sponsor.image.path)
                        except OSError:
                            pass
                    sponsor.delete()
                # add new sponsors
                for sponsor_node in event_node.findall('./sponsor'):
                    sponsor = EventSponsor(
                        event=event,
                        title_de=self.get_child_text(sponsor_node, 'title', languageId="1"),
                        title_en=self.get_child_text(sponsor_node, 'title', languageId="2"),
                        website=sponsor_node.get('linkURL'),
                    )
                    sponsor.save()
                    image_url = sponsor_node.get('pictureURL')
                    if image_url:
                        filename = image_url.split("/")[-1]
                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            image_mods.FileManager.save_file_for_object(
                                sponsor,
                                filename,
                                image_response.content,
                                field_name="image",
                                subpath="productions/{}/sponsors/".format(prod.slug),
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
