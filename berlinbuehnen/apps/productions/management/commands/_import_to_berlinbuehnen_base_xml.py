# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import requests
from datetime import timedelta
from dateutil.parser import parse as parse_datetime
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.utils.encoding import force_unicode
from django.utils.html import strip_tags
from django.db import models

from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify

from ._import_base import ImportCommandMixin, LocalFileAdapter


class ImportToBerlinBuehnenBaseXML(NoArgsCommand, ImportCommandMixin):
    """
    Base command to extend to import productions and events to Berlin Buehnen in XML format
    """
    help = "Import based on http://www.berlin-buehnen.de/media/docs/import-specification/production_import_specs.html"
    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3

    DEFAULT_PUBLISHING_STATUS = "import"
    DEFAULT_IN_PROGRAM_OF_LOCATION_ID = None
    service = None

    option_list = NoArgsCommand.option_list + (
        make_option('--skip_images', action='store_true', help='Skips image downloads'),
        make_option('--update_images', action='store_true', help='Forces image-download updates'),
        make_option('--untrash', action='store_true', help='Restores trashed productions'),
    )

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", self.NORMAL))
        self.skip_images = options.get("skip_images")
        self.update_images = options.get("update_images")
        self.untrash = options.get("untrash")
        self.prepare()
        self.main()
        self.finalize()

    def prepare(self):
        """Override this method to define self.service as an instance of external_services.Service model."""
        raise NotImplementedError("The define_service() method should be implemented.")

    def main(self):
        from xml.etree import ElementTree

        requests_session = requests.session()
        requests_session.mount('file://', LocalFileAdapter())

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Importing Productions ===")
            self.stdout.write(u"Processing page {}\n".format(self.service.url))

        r = requests_session.get(self.service.url)
        if r.status_code != 200:
            self.all_feeds_alright = False
            self.stderr.write(u"Error status {} when trying to access {}".format(r.status_code, self.service.url))
            return

        try:
            root_node = ElementTree.fromstring(r.content)
        except ElementTree.ParseError as err:
            self.all_feeds_alright = False
            self.stderr.write(u"Parsing error: %s" % unicode(err))
            return

        next_page = self.get_child_text(root_node.find("./meta"), "next")
        self._production_counter = 0
        self._total_production_count = int(self.get_child_text(root_node.find("./meta"), "total_count"))
        productions_node = root_node.find('./productions')
        self.save_page(productions_node)

        while(next_page):
            if self.verbosity >= self.NORMAL:
                self.stdout.write(u"Processing page {}\n".format(next_page))
            r = requests_session.get(next_page)
            if r.status_code != 200:
                self.all_feeds_alright = False
                self.stderr.write(u"Error status {} when trying to access {}".format(r.status_code, next_page))
                break # we want to show summary even if at some point the import breaks

            try:
                root_node = ElementTree.fromstring(r.content)
            except ElementTree.ParseError as err:
                self.all_feeds_alright = False
                self.stderr.write(u"Parsing error: %s" % unicode(err))
                return

            next_page = self.get_child_text(root_node.find('./meta'), "next")
            productions_node = root_node.find('./productions')
            self.save_page(productions_node)

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
                return force_unicode(u''.join([t for t in child_node.itertext()])).replace(r'\n', '\n')
        return u''

    def save_file_description(self, path, xml_node):
        from filebrowser.models import FileDescription
        try:
            file_description = FileDescription.objects.filter(
                file_path=path,
            ).order_by("pk")[0]
        except:
            file_description = FileDescription(file_path=path)
        file_description.title_de = self.get_child_text(xml_node, 'title_de')
        file_description.title_en = self.get_child_text(xml_node, 'title_en')
        # description and author go to the description field
        description_de_components = []
        description_en_components = []
        text = self.get_child_text(xml_node, 'description_de')
        if text:
            description_de_components.append(text)
        text = self.get_child_text(xml_node, 'description_en')
        if text:
            description_en_components.append(text)
        text = self.get_child_text(xml_node, 'author')
        if text:
            description_de_components.append(text)
            description_en_components.append(text)
        file_description.description_de = "\n".join(description_de_components)
        file_description.description_en = "\n".join(description_en_components)
        # copyright goes to the author field
        file_description.author = (self.get_child_text(xml_node, 'copyright') or text).replace("&copy;", "©")
        file_description.copyright_limitations = ""
        file_description.save()
        return file_description

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
        from berlinbuehnen.apps.productions.models import ProductionSponsor
        from berlinbuehnen.apps.productions.models import Event
        from berlinbuehnen.apps.productions.models import EventCharacteristics
        from berlinbuehnen.apps.productions.models import EventVideo
        from berlinbuehnen.apps.productions.models import EventLiveStream
        from berlinbuehnen.apps.productions.models import EventImage
        from berlinbuehnen.apps.productions.models import EventSponsor
        from berlinbuehnen.apps.productions.models import LanguageAndSubtitles

        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        image_mods = models.get_app("image_mods")

        prod_nodes = productions_node.findall('./production')

        for prod_index, prod_node in enumerate(prod_nodes, 1):
            self._production_counter += 1
            external_prod_id = self.get_child_text(prod_node, 'id')

            title_de = self.get_child_text(prod_node, 'title_de').replace('\n', ' ').strip()
            title_en = self.get_child_text(prod_node, 'title_en').replace('\n', ' ').strip()

            if self.verbosity >= self.NORMAL:
                self.stdout.write(u"%d/%d %s | %s" % (self._production_counter, self._total_production_count, title_de, title_en))

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
                prod = Production()
                prod.import_source = self.service
            else:
                prod = mapper.content_object
                self.production_ids_to_keep.add(prod.pk)
                if not prod or (not self.untrash and prod.status == "trashed"):
                    # if production was deleted after import,
                    # don't import it again
                    self.stats['prods_skipped'] += 1
                    continue

            if prod.no_overwriting:
                self.stats['prods_skipped'] += 1
                continue

            if not title_de:  # skip productions without title
                self.stats['prods_skipped'] += 1
                continue

            prod.status = self.get_child_text(prod_node, 'status') or self.DEFAULT_PUBLISHING_STATUS
            prod.title_de = strip_tags(title_de.replace('<br />', ' '))
            prod.title_en = strip_tags((title_en or title_de).replace('<br />', ' '))
            prod.prefix_de = strip_tags(self.get_child_text(prod_node, 'prefix_de').replace('<br />', ' '))
            prod.prefix_en = strip_tags(self.get_child_text(prod_node, 'prefix_en').replace('<br />', ' '))
            prod.subtitle_de = strip_tags(self.get_child_text(prod_node, 'subtitle_de').replace('<br />', ' '))
            prod.subtitle_en = strip_tags(self.get_child_text(prod_node, 'subtitle_en').replace('<br />', ' '))
            prod.original_de = strip_tags(self.get_child_text(prod_node, 'original_de').replace('<br />', ' '))
            prod.original_en = strip_tags(self.get_child_text(prod_node, 'original_en').replace('<br />', ' '))
            prod.website_de = self.get_child_text(prod_node, 'website_de')
            prod.website_en = self.get_child_text(prod_node, 'website_en')

            prod.slug = get_unique_value(Production, better_slugify(prod.title_de)[:200] or u"production", instance_pk=prod.pk)

            self.parse_and_use_texts(prod_node, prod)

            prod.ensembles = self.get_child_text(prod_node, 'ensembles')
            prod.organizers = self.get_child_text(prod_node, 'organizers')
            prod.in_cooperation_with = self.get_child_text(prod_node, 'in_cooperation_with')

            prod.free_entrance = (self.get_child_text(prod_node, 'free_entrance') == "true")
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

            prod.classiccard = (self.get_child_text(prod_node, 'classiccard') == "true")

            prod.save()
            self.production_ids_to_keep.add(prod.pk)

            prod.in_program_of.clear()
            if self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID:
                try:
                    location = Location.objects.get(pk=self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID)
                except Location.DoesNotExist:
                    pass
                else:
                    prod.in_program_of.add(location)
            for location_id_node in prod_node.findall("./in_program_of/location_id"):
                try:
                    location = Location.objects.get(pk=location_id_node.text)
                except Location.DoesNotExist:
                    pass
                else:
                    prod.in_program_of.add(location)

            prod.play_locations.clear()
            for location_id_node in prod_node.findall("./play_locations/location_id"):
                if not self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID or self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID != int(location_id_node.text):
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
            prod.fix_categories()

            prod.characteristics.clear()
            for ch_id_node in prod_node.findall("./characteristics/characteristic_id"):
                try:
                    ch = ProductionCharacteristics.objects.get(slug=ch_id_node.text)
                except ProductionCharacteristics.DoesNotExist:
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
            for live_stream_node in prod_node.findall("./live_streams/live_stream"):
                ls = ProductionLiveStream(production=prod)
                ls.creation_date = parse_datetime(self.get_child_text(live_stream_node, 'creation_date'))
                ls.modified_date = parse_datetime(self.get_child_text(live_stream_node, 'modified_date'))
                ls.title_de = self.get_child_text(live_stream_node, 'title_de')
                ls.title_en = self.get_child_text(live_stream_node, 'title_en')
                ls.link_or_embed = self.get_child_text(live_stream_node, 'embed')
                try:
                    ls.sort_order = int(self.get_child_text(live_stream_node, 'sort_order'))
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
                        if not self.update_images:
                            continue

                    filename = image_url.split("/")[-1]
                    if "?" in filename:
                        # clear the query parameters
                        filename = filename.split("?")[0]
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_mods.FileManager.save_file_for_object(
                            mf,
                            filename,
                            image_response.content,
                            field_name="path",
                            subpath="productions/{}/gallery/".format(prod.slug),
                        )
                        mf.copyright_restrictions = self.get_child_text(image_node, 'copyright_restrictions') or "general_use"
                        mf.save()
                        image_ids_to_keep.append(mf.pk)

                        file_description = self.save_file_description(mf.path, image_node)

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
                if "?" in filename:
                    # clear the query parameters
                    filename = filename.split("?")[0]
                pdf_response = requests.get(pdf_url)
                if pdf_response.status_code == 200:
                    image_mods.FileManager.save_file_for_object(
                        mf,
                        filename,
                        pdf_response.content,
                        field_name="path",
                        subpath="productions/{}/pdfs/".format(prod.slug),
                    )
                    mf.save()
                    pdf_ids_to_keep.append(mf.pk)
                    file_description = self.save_file_description(mf.path, pdf_node)

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
                    authorship_type = AuthorshipType.objects.get(slug=self.get_child_text(person_node, 'authorship_type_id'))
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
                    involvement_type = InvolvementType.objects.get(slug=self.get_child_text(person_node, 'involvement_type_id'))
                except:
                    involvement_type = None
                try:
                    imported_sort_order = int(self.get_child_text(person_node, 'sort_order'))
                except:
                    imported_sort_order = 1
                prod.productioninvolvement_set.create(
                    person=p,
                    involvement_type=involvement_type,
                    involvement_role_de=self.get_child_text(person_node, 'role_de'),
                    involvement_role_en=self.get_child_text(person_node, 'role_en'),
                    involvement_instrument_de=self.get_child_text(person_node, 'instrument_de'),
                    involvement_instrument_en=self.get_child_text(person_node, 'instrument_en'),
                    imported_sort_order=imported_sort_order,
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
            for sponsor_node in prod_node.findall('./sponsors/sponsor'):
                sponsor = ProductionSponsor(
                    production=prod,
                    title_de=self.get_child_text(sponsor_node, 'title_de'),
                    title_en=self.get_child_text(sponsor_node, 'title_en'),
                    website=self.get_child_text(sponsor_node, 'website'),
                )
                sponsor.save()
                image_url = self.get_child_text(sponsor_node, 'image_url')
                if image_url:
                    filename = image_url.split("/")[-1]
                    if "?" in filename:
                        # clear the query parameters
                        filename = filename.split("?")[0]
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

            for event_node in prod_node.findall('./events/event'):

                external_event_id = self.get_child_text(event_node, 'id')

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

                event.start_date = parse_datetime(self.get_child_text(event_node, 'start_date')).date()
                event.start_time = parse_datetime(self.get_child_text(event_node, 'start_time')).time()

                event.end_date = None
                end_date = self.get_child_text(event_node, 'end_date')
                if end_date:
                    try:
                        event.end_date = parse_datetime(end_date).date()
                    except:
                        pass

                event.end_time = None
                end_time = self.get_child_text(event_node, 'end_time')
                if end_time:
                    try:
                        event.end_time = parse_datetime().time()
                    except:
                        pass

                duration = None
                duration_str = self.get_child_text(event_node, 'duration')
                if duration_str:
                    try:
                        duration_time = parse_datetime(duration_str).time()
                    except:
                        pass
                    else:
                        duration = timedelta(
                            hours=duration_time.hour,
                            minutes=duration_time.minute,
                            seconds=duration_time.second,
                        ).total_seconds()
                event.duration = duration

                try:
                    event.pauses = int(self.get_child_text(event_node, 'pauses'))
                except:
                    event.pauses = None

                self.parse_and_use_texts(event_node, event)

                event.organizers = self.get_child_text(event_node, 'organizers')

                event.free_entrance = (self.get_child_text(event_node, 'free_entrance') == "true")
                try:
                    event.price_from = Decimal(self.get_child_text(event_node, 'price_from'))
                except:
                    event.price_from = None
                try:
                    event.price_till = Decimal(self.get_child_text(event_node, 'price_till'))
                except:
                    event.price_till = None
                event.tickets_website = self.get_child_text(event_node, 'tickets_website')
                event.location_title = self.get_child_text(event_node, 'location_title')
                event.street_address = self.get_child_text(event_node, 'street_address')
                event.street_address2 = self.get_child_text(event_node, 'street_address2')
                event.postal_code = self.get_child_text(event_node, 'postal_code')
                event.city = self.get_child_text(event_node, 'city')
                try:
                    event.latitude = float(self.get_child_text(event_node, 'latitude'))
                except:
                    event.latitude = None
                try:
                    event.longitude = float(self.get_child_text(event_node, 'longitude'))
                except:
                    event.longitude = None

                try:
                    event.language_and_subtitles = LanguageAndSubtitles.objects.get(slug=self.get_child_text(prod_node, 'language_and_subtitles_id'))
                except:
                    event.language_and_subtitles = None

                event.event_status = self.get_child_text(event_node, 'event_status')
                event.ticket_status = self.get_child_text(event_node, 'ticket_status')

                event.classiccard = (self.get_child_text(event_node, 'classiccard') == "true")

                event.save()
                self.event_ids_to_keep.add(event.pk)

                event.play_locations.clear()
                for location_id_node in event_node.findall("./play_locations/location_id"):
                    if not self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID or self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID != int(location_id_node.text):
                        try:
                            location = Location.objects.get(pk=location_id_node.text)
                        except Location.DoesNotExist:
                            pass
                        else:
                            event.play_locations.add(location)

                event.play_stages.clear()
                for stage_id_node in event_node.findall("./play_stages/stage_id"):
                    try:
                        stage = Stage.objects.get(pk=stage_id_node.text)
                    except Stage.DoesNotExist:
                        pass
                    else:
                        event.play_stages.add(stage)

                event.characteristics.clear()
                for ch_id_node in event_node.findall("./characteristics/characteristic_id"):
                    try:
                        ch = EventCharacteristics.objects.get(slug=ch_id_node.text)
                    except EventCharacteristics.DoesNotExist:
                        pass
                    else:
                        event.characteristics.add(ch)

                event.eventvideo_set.all().delete()
                for video_node in event_node.findall("./videos/video"):
                    video = EventVideo(event=event)
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
    
                event.eventlivestream_set.all().delete()
                for video_node in event_node.findall("./videos/video"):
                    ls = EventLiveStream(event=event)
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
                    for image_node in event_node.findall('./images/image'):
                        image_url = self.get_child_text(image_node, 'url')
                        if not image_url.startswith('http'):
                            continue
    
                        image_external_id = "event-%s-%s" % (event.pk, image_url)
                        image_mapper = None
                        try:
                            # get image model instance from saved mapper
                            image_mapper = self.service.objectmapper_set.get(
                                external_id=image_external_id,
                                content_type__app_label="events",
                                content_type__model="eventimage",
                            )
                        except models.ObjectDoesNotExist:
                            # or create a new exhibition and then create a mapper
                            mf = EventImage(event=event)
                        else:
                            mf = image_mapper.content_object
                            if mf:
                                image_ids_to_keep.append(mf.pk)
                            if not self.update_images:
                                continue
    
                        filename = image_url.split("/")[-1]
                        if "?" in filename:
                            # clear the query parameters
                            filename = filename.split("?")[0]
                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            image_mods.FileManager.save_file_for_object(
                                mf,
                                filename,
                                image_response.content,
                                field_name="path",
                                subpath="productions/{}/events/gallery/".format(event.production.slug),
                            )
                            mf.copyright_restrictions = self.get_child_text(image_node, 'copyright_restrictions') or "general_use"
                            mf.save()
                            image_ids_to_keep.append(mf.pk)
                            file_description = self.save_file_description(mf.path, image_node)

                            if not image_mapper:
                                image_mapper = ObjectMapper(
                                    service=self.service,
                                    external_id=image_external_id,
                                )
                                image_mapper.content_object = mf
                                image_mapper.save()
    
                    for mf in event.eventimage_set.exclude(id__in=image_ids_to_keep):
                        if mf.path:
                            # remove the file from the file system
                            image_mods.FileManager.delete_file(mf.path.name)
                        # delete image mapper
                        self.service.objectmapper_set.filter(
                            object_id=mf.pk,
                            content_type__app_label="events",
                            content_type__model="eventimage",
                        ).delete()
                        # delete image model instance
                        mf.delete()
    
                pdf_ids_to_keep = []
                for pdf_node in event_node.findall('./pdfs/pdf'):
                    pdf_url = self.get_child_text(pdf_node, 'url')
                    if not pdf_url.startswith('http'):
                        continue
    
                    pdf_external_id = "event-%s-%s" % (event.pk, pdf_url)
                    pdf_mapper = None
                    try:
                        # get pdf model instance from saved mapper
                        pdf_mapper = self.service.objectmapper_set.get(
                            external_id=pdf_external_id,
                            content_type__app_label="events",
                            content_type__model="eventpdf",
                        )
                    except models.ObjectDoesNotExist:
                        # or create a new exhibition and then create a mapper
                        mf = EventImage(event=event)
                    else:
                        mf = pdf_mapper.content_object
                        if mf:
                            pdf_ids_to_keep.append(mf.pk)
                        continue
    
                    filename = pdf_url.split("/")[-1]
                    if "?" in filename:
                        # clear the query parameters
                        filename = filename.split("?")[0]
                    pdf_response = requests.get(pdf_url)
                    if pdf_response.status_code == 200:
                        image_mods.FileManager.save_file_for_object(
                            mf,
                            filename,
                            pdf_response.content,
                            field_name="path",
                            subpath="productions/{}/events/gallery/".format(event.production.slug),
                        )
                        mf.save()
                        pdf_ids_to_keep.append(mf.pk)
                        file_description = self.save_file_description(mf.path, pdf_node)

                        if not pdf_mapper:
                            pdf_mapper = ObjectMapper(
                                service=self.service,
                                external_id=pdf_external_id,
                            )
                            pdf_mapper.content_object = mf
                            pdf_mapper.save()
    
                for mf in event.eventpdf_set.exclude(id__in=pdf_ids_to_keep):
                    if mf.path:
                        # remove the file from the file system
                        image_mods.FileManager.delete_file(mf.path.name)
                    # delete pdf mapper
                    self.service.objectmapper_set.filter(
                        object_id=mf.pk,
                        content_type__app_label="events",
                        content_type__model="eventpdf",
                    ).delete()
                    # delete pdf model instance
                    mf.delete()
    
    
                event.eventleadership_set.all().delete()
                for person_node in event_node.findall('./leaders/leader'):
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
                    event.eventleadership_set.create(
                        person=p,
                        function_de=self.get_child_text(person_node, 'function_de'),
                        function_en=self.get_child_text(person_node, 'function_en'),
                        imported_sort_order=imported_sort_order,
                    )
                for sort_order, item in enumerate(event.eventleadership_set.order_by('imported_sort_order'), 0):
                    item.sort_order = sort_order
                    item.save()
    
                event.eventauthorship_set.all().delete()
                for person_node in event_node.findall('./authors/author'):
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
                        authorship_type = AuthorshipType.objects.get(slug=self.get_child_text(person_node, 'authorship_type_id'))
                    except:
                        authorship_type = None
                    try:
                        imported_sort_order = int(self.get_child_text(person_node, 'sort_order'))
                    except:
                        imported_sort_order = 1
                    event.eventauthorship_set.create(
                        person=p,
                        authorship_type=authorship_type,
                        imported_sort_order=imported_sort_order,
                    )
                for sort_order, item in enumerate(event.eventauthorship_set.order_by('imported_sort_order'), 0):
                    item.sort_order = sort_order
                    item.save()
    
                event.eventinvolvement_set.all().delete()
                for person_node in event_node.findall('./participants/participant'):
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
                        involvement_type = InvolvementType.objects.get(slug=self.get_child_text(person_node, 'involvement_type_id'))
                    except:
                        involvement_type = None
                    try:
                        imported_sort_order = int(self.get_child_text(person_node, 'sort_order'))
                    except:
                        imported_sort_order = 1
                    event.eventinvolvement_set.create(
                        person=p,
                        involvement_type=involvement_type,
                        involvement_role_de=self.get_child_text(person_node, 'role_de'),
                        involvement_role_en=self.get_child_text(person_node, 'role_en'),
                        involvement_instrument_de=self.get_child_text(person_node, 'instrument_de'),
                        involvement_instrument_en=self.get_child_text(person_node, 'instrument_en'),
                        imported_sort_order=imported_sort_order,
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
                for sponsor_node in event_node.findall('./sponsors/sponsor'):
                    sponsor = EventSponsor(
                        event=event,
                        title_de=self.get_child_text(sponsor_node, 'title_de'),
                        title_en=self.get_child_text(sponsor_node, 'title_en'),
                        website=self.get_child_text(sponsor_node, 'website'),
                    )
                    sponsor.save()
                    image_url = self.get_child_text(sponsor_node, 'image_url')
                    if image_url:
                        filename = image_url.split("/")[-1]
                        if "?" in filename:
                            # clear the query parameters
                            filename = filename.split("?")[0]
                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            image_mods.FileManager.save_file_for_object(
                                sponsor,
                                filename,
                                image_response.content,
                                field_name="image",
                                subpath="productions/{}/sponsors/".format(event.production.slug),
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

            prod.update_actual_date_and_time()
