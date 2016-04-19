# -*- coding: UTF-8 -*-

import re
import requests
from xml.etree import ElementTree
from dateutil.parser import parse as parse_datetime
from optparse import make_option
import csv
import os
from urllib import url2pathname

from django.core.management.base import NoArgsCommand
from django.utils.encoding import smart_str, force_unicode
from django.utils.text import slugify
from django.db import models
from django.conf import settings

from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class LocalFileAdapter(requests.adapters.BaseAdapter):
    """Protocol Adapter to allow Requests to GET file:// URLs

    @todo: Properly handle non-empty hostname portions.
    """

    @staticmethod
    def _chkpath(method, path):
        """Return an HTTP status for the given filesystem path."""
        if method.lower() in ('put', 'delete'):
            return 501, "Not Implemented"  # TODO
        elif method.lower() not in ('get', 'head'):
            return 405, "Method Not Allowed"
        elif os.path.isdir(path):
            return 400, "Path Not A File"
        elif not os.path.isfile(path):
            return 404, "File Not Found"
        elif not os.access(path, os.R_OK):
            return 403, "Access Denied"
        else:
            return 200, "OK"

    def send(self, req, **kwargs):  # pylint: disable=unused-argument
        """Return the file specified by the given request

        @type req: C{PreparedRequest}
        @todo: Should I bother filling `response.headers` and processing
               If-Modified-Since and friends using `os.stat`?
        """
        path = os.path.normcase(os.path.normpath(url2pathname(req.path_url)))
        response = requests.Response()

        response.status_code, response.reason = self._chkpath(req.method, path)
        if response.status_code == 200 and req.method.lower() != 'head':
            try:
                response.raw = open(path, 'rb')
            except (OSError, IOError), err:
                response.status_code = 500
                response.reason = str(err)

        if isinstance(req.url, bytes):
            response.url = req.url.decode('utf-8')
        else:
            response.url = req.url

        response.request = req
        response.connection = self

        return response

    def close(self):
        pass


class Command(NoArgsCommand, ImportFromCulturebaseBase):
    help = "Imports productions and events from Culturebase / Deutsche Oper Berlin"

    DEFAULT_PUBLISHING_STATUS = "import"
    production_ids_to_keep = set()
    event_ids_to_keep = set()

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        Service = models.get_model("external_services", "Service")

        self.service, created = Service.objects.get_or_create(
            sysname="bb_example",
            defaults={
                'url': "file://{}/production_import_specs/example.xml".format(settings.PROJECT_PATH),
                'title': u"Berlin Bühnen Import API Example",
            },
        )

        requests_session = requests.session()
        requests_session.mount('file://', LocalFileAdapter())

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

        r = requests_session.get(self.service.url)
        if r.status_code != 200:
            print(u"Error status: %s" % r.status_code)
            return
        root_node = ElementTree.fromstring(r.content)
        next_page = self.get_child_text(root_node.find('./meta'), "next")
        productions_node = root_node.find('./productions')
        self.save_page(productions_node)

        while(next_page):
            r = requests_session.get(next_page)
            if r.status_code != 200:
                print(u"Error status: %s" % r.status_code)
                return
            root_node = ElementTree.fromstring(r.content)
            next_page = self.get_child_text(root_node.find('./meta'), "next")
            productions_node = root_node.find('./productions')
            self.save_page(productions_node)

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

    def parse_and_use_texts(self, xml_node, instance):
        instance.description_de = self.get_child_text(xml_node, 'description_de')
        instance.description_en = self.get_child_text(xml_node, 'description_en')
        instance.teaser_de = self.get_child_text(xml_node, 'teaser_de')
        instance.teaser_en = self.get_child_text(xml_node, 'teaser_en')
        instance.work_info_de = self.get_child_text(xml_node, 'work_info_de')
        instance.work_info_en = self.get_child_text(xml_node, 'work_info_en')
        instance.contents_de = self.get_child_text(xml_node, 'contents_de')
        instance.contents_en = self.get_child_text(xml_node, 'contents_en')
        instance.press_text_de = self.get_child_text(xml_node, 'press_text_de')
        instance.press_text_en = self.get_child_text(xml_node, 'press_text_en')
        instance.credits_de = self.get_child_text(xml_node, 'credits_de')
        instance.credits_en = self.get_child_text(xml_node, 'credits_en')
        instance.concert_program_de = self.get_child_text(xml_node, 'concert_program_de')
        instance.concert_program_en = self.get_child_text(xml_node, 'concert_program_en')
        instance.supporting_program_de = self.get_child_text(xml_node, 'supporting_program_de')
        instance.supporting_program_en = self.get_child_text(xml_node, 'supporting_program_en')
        instance.remarks_de = self.get_child_text(xml_node, 'remarks_de')
        instance.remarks_en = self.get_child_text(xml_node, 'remarks_en')
        instance.duration_text_de = self.get_child_text(xml_node, 'duration_text_de')
        instance.duration_text_en = self.get_child_text(xml_node, 'duration_text_en')
        instance.subtitles_text_de = self.get_child_text(xml_node, 'subtitles_text_de')
        instance.subtitles_text_en = self.get_child_text(xml_node, 'subtitles_text_en')
        instance.age_text_de = self.get_child_text(xml_node, 'age_text_de')
        instance.age_text_en = self.get_child_text(xml_node, 'age_text_en')
        instance.price_information_de = self.get_child_text(xml_node, 'price_information_de')
        instance.price_information_en = self.get_child_text(xml_node, 'price_information_en')


    def save_page(self, productions_node):
        from decimal import Decimal
        from berlinbuehnen.apps.people.models import Person
        from berlinbuehnen.apps.people.models import Prefix
        from berlinbuehnen.apps.people.models import AuthorshipType
        from berlinbuehnen.apps.people.models import InvolvementType
        from berlinbuehnen.apps.locations.models import Location
        from berlinbuehnen.apps.locations.models import Stage
        from berlinbuehnen.apps.productions.models import Production
        from berlinbuehnen.apps.productions.models import ProductionCategory
        from berlinbuehnen.apps.productions.models import ProductionCharacteristics
        from berlinbuehnen.apps.productions.models import ProductionVideo
        from berlinbuehnen.apps.productions.models import ProductionLiveStream
        from berlinbuehnen.apps.productions.models import ProductionImage
        from berlinbuehnen.apps.productions.models import ProductionPDF
        from berlinbuehnen.apps.productions.models import Event
        from berlinbuehnen.apps.productions.models import EventVideo
        from berlinbuehnen.apps.productions.models import EventLiveStream
        from berlinbuehnen.apps.productions.models import EventImage
        from berlinbuehnen.apps.productions.models import EventPDF
        from berlinbuehnen.apps.productions.models import LanguageAndSubtitles
        from berlinbuehnen.apps.sponsors.models import Sponsor

        from filebrowser.models import FileDescription
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        image_mods = models.get_app("image_mods")

        prod_nodes = productions_node.findall('./production')
        prods_count = len(prod_nodes)

        for prod_index, prod_node in enumerate(prod_nodes, 1):
            external_prod_id = prod_node.get('id')

            title_de = self.get_child_text(prod_node, 'title_de').replace('\n', ' ').strip()
            title_en = self.get_child_text(prod_node, 'title_en').replace('\n', ' ').strip()

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
                prod = Production()
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

            prod.status = self.get_child_text(prod_node, 'status') or self.DEFAULT_PUBLISHING_STATUS
            prod.title_de = title_de
            prod.title_en = title_en or title_de
            prod.prefix_de = self.get_child_text(prod_node, 'prefix_de')
            prod.prefix_en = self.get_child_text(prod_node, 'prefix_en')
            prod.subtitle_de = self.get_child_text(prod_node, 'subtitle_de')
            prod.subtitle_en = self.get_child_text(prod_node, 'subtitle_en')
            prod.original_de = self.get_child_text(prod_node, 'original_de')
            prod.original_en = self.get_child_text(prod_node, 'original_en')
            prod.website_de = self.get_child_text(prod_node, 'website_de')
            prod.website_en = self.get_child_text(prod_node, 'website_en')

            prod.slug = get_unique_value(Production, better_slugify(prod.title_de) or u"production", instance_pk=prod.pk)

            self.parse_and_use_texts(prod_node, prod)

            prod.ensembles = self.get_child_text(prod_node, 'ensembles')
            prod.organizers = self.get_child_text(prod_node, 'organizers')
            prod.in_cooperation_with = self.get_child_text(prod_node, 'in_cooperation_with')

            prod.free_entrance = (self.get_child_text(prod_node, 'free_entrance') == "True")
            try:
                prod.price_from = Decimal(self.get_child_text(prod_node, 'price_from'))
            except:
                prod.price_from = None
            try:
                prod.price_till = Decimal(self.get_child_text(prod_node, 'price_till'))
            except:
                prod.price_till = None
            prod.tickets_website = self.get_child_text(prod_node, 'tickets_website')
            prod.edu_offer_website = self.get_child_text(prod_node, 'edu_offer_website')

            try:
                prod.age_from = int(self.get_child_text(prod_node, 'age_from'))
            except:
                prod.age_from = None
            try:
                prod.age_till = int(self.get_child_text(prod_node, 'age_till'))
            except:
                prod.age_till = None

            prod.location_title = self.get_child_text(prod_node, 'location_title')
            prod.street_address = self.get_child_text(prod_node, 'street_address')
            prod.street_address2 = self.get_child_text(prod_node, 'street_address2')
            prod.postal_code = self.get_child_text(prod_node, 'postal_code')
            prod.city = self.get_child_text(prod_node, 'city')
            try:
                prod.latitude = float(self.get_child_text(prod_node, 'latitude'))
            except:
                prod.latitude = None
            try:
                prod.longitude = float(self.get_child_text(prod_node, 'longitude'))
            except:
                prod.longitude = None

            try:
                prod.language_and_subtitles = LanguageAndSubtitles.objects.get(slug=self.get_child_text(prod_node, 'language_and_subtitles_id'))
            except:
                prod.language_and_subtitles = None

            prod.save()
            self.production_ids_to_keep.add(prod.pk)

            prod.in_program_of.clear()
            for location_id_node in prod_node.findall("./in_program_of/location_id"):
                try:
                    location = Location.objects.get(pk=location_id_node.text)
                except Location.DoesNotExist:
                    pass
                else:
                    prod.in_program_of.add(location)

            prod.play_locations.clear()
            for location_id_node in prod_node.findall("./play_locations/location_id"):
                try:
                    location = Location.objects.get(pk=location_id_node.text)
                except Location.DoesNotExist:
                    pass
                else:
                    prod.play_locations.add(location)

            prod.play_stages.clear()
            for stage_id_node in prod_node.findall("./play_stages/stage_id"):
                try:
                    stage = Stage.objects.get(pk=stage_id_node.text)
                except Stage.DoesNotExist:
                    pass
                else:
                    prod.play_stages.add(stage)

            prod.categories.clear()
            for category_id_node in prod_node.findall("./categories/category_id"):
                try:
                    cat = ProductionCategory.objects.get(pk=category_id_node.text)
                except ProductionCategory.DoesNotExist:
                    pass
                else:
                    prod.categories.add(cat)

            prod.characteristics.clear()
            for ch_id_node in prod_node.findall("./characteristics/characteristic_id"):
                try:
                    ch = ProductionCharacteristics.objects.get(pk=ch_id_node.text)
                except ProductionCategory.DoesNotExist:
                    pass
                else:
                    prod.characteristics.add(ch)

            # for owner in self.owners:
            #     prod.set_owner(owner)

            prod.productionvideo_set.all().delete()
            for video_node in prod_node.findall("./videos/video"):
                video = ProductionVideo(production=prod)
                video.creation_date = parse_datetime(self.get_child_text(video_node, 'creation_date'))
                video.modified_date = parse_datetime(self.get_child_text(video_node, 'modified_date'))
                video.title_de = self.get_child_text(video_node, 'title_de')
                video.title_en = self.get_child_text(video_node, 'title_en')
                video.link_or_embed = self.get_child_text(video_node, 'embed')
                try:
                    video.sort_order = int(self.get_child_text(video_node, 'sort_order'))
                except:
                    video.sort_order = 1
                video.save()

            prod.productionlivestream_set.all().delete()
            for video_node in prod_node.findall("./videos/video"):
                ls = ProductionLiveStream(production=prod)
                ls.creation_date = parse_datetime(self.get_child_text(video_node, 'creation_date'))
                ls.modified_date = parse_datetime(self.get_child_text(video_node, 'modified_date'))
                ls.title_de = self.get_child_text(video_node, 'title_de')
                ls.title_en = self.get_child_text(video_node, 'title_en')
                ls.link_or_embed = self.get_child_text(video_node, 'embed')
                try:
                    ls.sort_order = int(self.get_child_text(video_node, 'sort_order'))
                except:
                    ls.sort_order = 1
                ls.save()

            if not self.skip_images:
                image_ids_to_keep = []
                for image_node in prod_node.findall('./images/image'):
                    image_url = self.get_child_text(image_node, 'url')
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
                        mf.copyright_restrictions = self.get_child_text(image_node, 'copyright_restrictions') or "general_use"
                        mf.save()
                        image_ids_to_keep.append(mf.pk)
                        try:
                            file_description = FileDescription.objects.filter(
                                file_path=mf.path,
                            ).order_by("pk")[0]
                        except:
                            file_description = FileDescription(file_path=mf.path)

                        file_description.title_de = self.get_child_text(image_node, 'title_de')
                        file_description.title_en = self.get_child_text(image_node, 'title_en')
                        file_description.description_de = self.get_child_text(image_node, 'description_de')
                        file_description.description_en = self.get_child_text(image_node, 'description_en')
                        file_description.author = self.get_child_text(image_node, 'author')
                        file_description.copyright_limitations = self.get_child_text(image_node, 'copyright')
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

            pdf_ids_to_keep = []
            for pdf_node in prod_node.findall('./pdfs/pdf'):
                pdf_url = self.get_child_text(pdf_node, 'url')
                if not pdf_url.startswith('http'):
                    continue

                pdf_external_id = "prod-%s-%s" % (prod.pk, pdf_url)
                pdf_mapper = None
                try:
                    # get pdf model instance from saved mapper
                    pdf_mapper = self.service.objectmapper_set.get(
                        external_id=pdf_external_id,
                        content_type__app_label="productions",
                        content_type__model="productionpdf",
                    )
                except models.ObjectDoesNotExist:
                    # or create a new exhibition and then create a mapper
                    mf = ProductionImage(production=prod)
                else:
                    mf = pdf_mapper.content_object
                    if mf:
                        pdf_ids_to_keep.append(mf.pk)
                    continue

                filename = pdf_url.split("/")[-1]
                pdf_response = requests.get(pdf_url)
                if pdf_response.status_code == 200:
                    image_mods.FileManager.save_file_for_object(
                        mf,
                        filename,
                        pdf_response.content,
                        field_name="path",
                        subpath="productions/%s/pdfs/" % prod.slug,
                    )
                    mf.save()
                    pdf_ids_to_keep.append(mf.pk)
                    try:
                        file_description = FileDescription.objects.filter(
                            file_path=mf.path,
                        ).order_by("pk")[0]
                    except:
                        file_description = FileDescription(file_path=mf.path)

                    file_description.title_de = self.get_child_text(pdf_node, 'title_de')
                    file_description.title_en = self.get_child_text(pdf_node, 'title_en')
                    file_description.description_de = self.get_child_text(pdf_node, 'description_de')
                    file_description.description_en = self.get_child_text(pdf_node, 'description_en')
                    file_description.author = self.get_child_text(pdf_node, 'author')
                    file_description.copyright_limitations = self.get_child_text(pdf_node, 'copyright')
                    file_description.save()

                    if not pdf_mapper:
                        pdf_mapper = ObjectMapper(
                            service=self.service,
                            external_id=pdf_external_id,
                        )
                        pdf_mapper.content_object = mf
                        pdf_mapper.save()

            for mf in prod.productionpdf_set.exclude(id__in=pdf_ids_to_keep):
                if mf.path:
                    # remove the file from the file system
                    image_mods.FileManager.delete_file(mf.path.name)
                # delete pdf mapper
                self.service.objectmapper_set.filter(
                    object_id=mf.pk,
                    content_type__app_label="productions",
                    content_type__model="productionpdf",
                ).delete()
                # delete pdf model instance
                mf.delete()


            prod.productionleadership_set.all().delete()
            for person_node in prod_node.findall('./leaders/leader'):
                try:
                    prefix = Prefix.objects.get(slug=self.get_child_text(person_node, 'prefix_id'))
                except:
                    prefix = None
                first_name = self.get_child_text(person_node, 'first_name')
                last_name = self.get_child_text(person_node, 'last_name')
                p, created = Person.objects.get_first_or_create(
                    prefix=prefix,
                    first_name=first_name,
                    last_name=last_name,
                )
                try:
                    imported_sort_order = int(self.get_child_text(person_node, 'sort_order'))
                except:
                    imported_sort_order = 1
                prod.productionleadership_set.create(
                    person=p,
                    function_de=self.get_child_text(person_node, 'function_de'),
                    function_en=self.get_child_text(person_node, 'function_en'),
                    imported_sort_order=imported_sort_order,
                )
            for sort_order, item in enumerate(prod.productionleadership_set.order_by('imported_sort_order'), 0):
                item.sort_order = sort_order
                item.save()

            prod.productionauthorship_set.all().delete()
            for person_node in prod_node.findall('./authors/author'):
                try:
                    prefix = Prefix.objects.get(slug=self.get_child_text(person_node, 'prefix_id'))
                except:
                    prefix = None
                first_name = self.get_child_text(person_node, 'first_name')
                last_name = self.get_child_text(person_node, 'last_name')
                p, created = Person.objects.get_first_or_create(
                    prefix=prefix,
                    first_name=first_name,
                    last_name=last_name,
                )
                try:
                    authorship_type = AuthorshipType.objects.get(slug=self.get_child_text(person_node, 'type_id'))
                except:
                    authorship_type = None
                try:
                    imported_sort_order = int(self.get_child_text(person_node, 'sort_order'))
                except:
                    imported_sort_order = 1
                prod.productionauthorship_set.create(
                    person=p,
                    authorship_type=authorship_type,
                    imported_sort_order=imported_sort_order,
                )
            for sort_order, item in enumerate(prod.productionauthorship_set.order_by('imported_sort_order'), 0):
                item.sort_order = sort_order
                item.save()

            prod.productioninvolvement_set.all().delete()
            for person_node in prod_node.findall('./participants/participant'):
                try:
                    prefix = Prefix.objects.get(slug=self.get_child_text(person_node, 'prefix_id'))
                except:
                    prefix = None
                first_name = self.get_child_text(person_node, 'first_name')
                last_name = self.get_child_text(person_node, 'last_name')
                p, created = Person.objects.get_first_or_create(
                    prefix=prefix,
                    first_name=first_name,
                    last_name=last_name,
                )
                try:
                    involvement_type = InvolvementType.objects.get(slug=self.get_child_text(person_node, 'type_id'))
                except:
                    involvement_type = None
                try:
                    imported_sort_order = int(self.get_child_text(person_node, 'sort_order'))
                except:
                    imported_sort_order = 1
                prod.productioninvolvement_set.create(
                    person=p,
                    involvement_type=involvement_type,
                    role_de=self.get_child_text(person_node, 'role_de'),
                    role_en=self.get_child_text(person_node, 'role_en'),
                    instrument_de=self.get_child_text(person_node, 'instrument_de'),
                    instrument_en=self.get_child_text(person_node, 'instrument_en'),
                    imported_sort_order=imported_sort_order,
                )
            for sort_order, item in enumerate(prod.productioninvolvement_set.order_by('imported_sort_order'), 0):
                item.sort_order = sort_order
                item.save()

            prod.sponsors.clear()
            for sponsor_node in prod_node.findall('./sponsors/sponsor'):
                sponsor, created = Sponsor.objects.get_or_create(
                    title_de=self.get_child_text(person_node, 'title_de'),
                    defaults={
                        'title_en': self.get_child_text(person_node, 'title_en'),
                        'website': self.get_child_text(person_node, 'website'),
                    }
                )
                image_url = self.get_child_text(person_node, 'image_url')
                if image_url and created:
                    filename = image_url.split("/")[-1]
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_mods.FileManager.save_file_for_object(
                            sponsor,
                            filename,
                            image_response.content,
                            field_name="image",
                            subpath="sponsors/",
                        )
                    sponsor.save()
                prod.sponsors.add(sponsor)

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
                    for image_node in event_node.findall('picture'):
                        image_url = self.get_child_text(image_node, 'Url')
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
                            if image_node.get('publishType') == "1":
                                mf.copyright_restrictions = "general_use"
                            elif image_node.get('publishType') == "3":
                                mf.copyright_restrictions = "protected"
                            mf.save()
                            image_ids_to_keep.append(mf.pk)
                            try:
                                file_description = FileDescription.objects.filter(
                                    file_path=mf.path,
                                ).order_by("pk")[0]
                            except:
                                file_description = FileDescription(file_path=mf.path)

                            file_description.title_de = self.get_child_text(image_node, 'title', languageId="1") or self.get_child_text(image_node, 'text', languageId="1")
                            file_description.title_en = self.get_child_text(image_node, 'title', languageId="2") or self.get_child_text(image_node, 'text', languageId="2")
                            file_description.author = (image_node.get('photographer') or u"").replace("Foto: ", "")
                            file_description.copyright_limitations = image_node.get('copyright')
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
                    #else:
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

                event.sponsors.clear()
                for sponsor_node in event_node.findall('sponsor'):
                    sponsor, created = Sponsor.objects.get_or_create(
                        title_de=self.get_child_text(sponsor_node, 'title', languageId="1"),
                        defaults={
                            'title_en': self.get_child_text(sponsor_node, 'title', languageId="2"),
                            'website': sponsor_node.get('linkURL'),
                        }
                    )
                    image_url = sponsor_node.get('pictureURL')
                    if image_url and created:
                        filename = image_url.split("/")[-1]
                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            image_mods.FileManager.save_file_for_object(
                                sponsor,
                                filename,
                                image_response.content,
                                field_name="image",
                                subpath="sponsors/",
                            )
                        sponsor.save()
                        event.sponsors.add(sponsor)

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

