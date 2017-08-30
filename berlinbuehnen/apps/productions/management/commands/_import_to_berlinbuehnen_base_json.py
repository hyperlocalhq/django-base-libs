# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from ._import_to_berlinbuehnen_base_xml import *


class ImportToBerlinBuehnenBaseJSON(ImportToBerlinBuehnenBaseXML):
    """
    Base command to extend to import productions and events to Berlin Buehnen in JSON format
    """
    AUTH = ()

    def main(self):
        requests_session = requests.session()
        requests_session.mount('file://', LocalFileAdapter())

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Importing Productions ===\n")
            self.stdout.write(u"Processing page {}\n".format(self.service.url))

        r = requests_session.get(self.service.url, auth=self.AUTH)
        if r.status_code != 200:
            self.all_feeds_alright = False
            self.stderr.write(u"Error status {} when trying to access {}\n".format(r.status_code, self.service.url))
            return
        try:
            root_dict = r.json()
        except ValueError as err:
            self.all_feeds_alright = False
            self.stderr.write(u"Parsing error: %s" % unicode(err))
            return
        next_page = root_dict.get('meta', {}).get('next', "")
        self._production_counter = 0
        self._total_production_count = root_dict.get('meta', {}).get('total_count', "")
        productions_dict = root_dict.get('productions', {})
        self.save_page(productions_dict)

        while (next_page):
            if self.verbosity >= self.NORMAL:
                self.stdout.write(u"Processing page {}\n".format(next_page))
            r = requests_session.get(next_page, auth=self.AUTH)
            if r.status_code != 200:
                self.all_feeds_alright = False
                self.stderr.write(u"Error status {} when trying to access {}\n".format(r.status_code, next_page))
                break  # we want to show summary even if at some point the import breaks
            try:
                root_dict = r.json()
            except ValueError as err:
                self.all_feeds_alright = False
                self.stderr.write(u"Parsing error: %s" % unicode(err))
                return
            next_page = root_dict.get('meta', {}).get('next', "")
            productions_dict = root_dict.get('productions', {})
            self.save_page(productions_dict)

    def save_file_description(self, path, d):
        from filebrowser.models import FileDescription
        try:
            file_description = FileDescription.objects.filter(
                file_path=path,
            ).order_by("pk")[0]
        except:
            file_description = FileDescription(file_path=path)
        file_description.title_de = d.get('title_de', "")
        file_description.title_en = d.get('title_en', "")
        # description and author go to the description field
        description_de_components = []
        description_en_components = []
        text = d.get('description_de', "")
        if text:
            description_de_components.append(text)
        text = d.get('description_en', "")
        if text:
            description_en_components.append(text)
        text = d.get('author', "")
        if text:
            description_de_components.append(text)
            description_en_components.append(text)
        file_description.description_de = "\n".join(description_de_components)
        file_description.description_en = "\n".join(description_en_components)
        # copyright goes to the author field
        file_description.author = (d.get('copyright', "") or text).replace("&copy;", "©")
        file_description.copyright_limitations = ""
        file_description.save()
        return file_description

    def parse_and_use_texts(self, d, instance):
        instance.description_de = d.get('description_de', "").replace("&nbsp;", " ")
        instance.description_en = d.get('description_en', "").replace("&nbsp;", " ")
        instance.teaser_de = d.get('teaser_de', "").replace("&nbsp;", " ")
        instance.teaser_en = d.get('teaser_en', "").replace("&nbsp;", " ")
        instance.work_info_de = d.get('work_info_de', "").replace("&nbsp;", " ")
        instance.work_info_en = d.get('work_info_en', "").replace("&nbsp;", " ")
        instance.contents_de = d.get('contents_de', "").replace("&nbsp;", " ")
        instance.contents_en = d.get('contents_en', "").replace("&nbsp;", " ")
        instance.press_text_de = d.get('press_text_de', "").replace("&nbsp;", " ")
        instance.press_text_en = d.get('press_text_en', "").replace("&nbsp;", " ")
        instance.credits_de = d.get('credits_de', "").replace("&nbsp;", " ")
        instance.credits_en = d.get('credits_en', "").replace("&nbsp;", " ")
        instance.concert_program_de = d.get('concert_program_de', "").replace("&nbsp;", " ")
        instance.concert_program_en = d.get('concert_program_en', "").replace("&nbsp;", " ")
        instance.supporting_program_de = d.get('supporting_program_de', "").replace("&nbsp;", " ")
        instance.supporting_program_en = d.get('supporting_program_en', "").replace("&nbsp;", " ")
        instance.remarks_de = d.get('remarks_de', "").replace("&nbsp;", " ")
        instance.remarks_en = d.get('remarks_en', "").replace("&nbsp;", " ")
        instance.duration_text_de = d.get('duration_text_de', "").replace("&nbsp;", " ")
        instance.duration_text_en = d.get('duration_text_en', "").replace("&nbsp;", " ")
        instance.subtitles_text_de = d.get('subtitles_text_de', "").replace("&nbsp;", " ")
        instance.subtitles_text_en = d.get('subtitles_text_en', "").replace("&nbsp;", " ")
        instance.age_text_de = d.get('age_text_de', "").replace("&nbsp;", " ")
        instance.age_text_en = d.get('age_text_en', "").replace("&nbsp;", " ")
        instance.price_information_de = d.get('price_information_de', "").replace("&nbsp;", " ")
        instance.price_information_en = d.get('price_information_en', "").replace("&nbsp;", " ")

    def save_page(self, productions_dict):
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
        from filebrowser.models import FileDescription

        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        image_mods = models.get_app("image_mods")

        prods_count = len(productions_dict.keys())

        for prod_index, prod_dict in enumerate(productions_dict.values(), 1):
            self._production_counter += 1

            external_prod_id = prod_dict.get('id', "")

            title_de = prod_dict.get('title_de', "").replace('\n', ' ').strip()
            title_en = prod_dict.get('title_en', "").replace('\n', ' ').strip()

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
                if not prod or prod.status == "trashed":
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

            prod.status = prod_dict.get('status', "") or self.DEFAULT_PUBLISHING_STATUS
            prod.title_de = strip_tags(title_de.replace('<br />', ' '))
            prod.title_en = strip_tags((title_en or title_de).replace('<br />', ' '))
            prod.prefix_de = strip_tags(prod_dict.get('prefix_de', "").replace('<br />', ' '))
            prod.prefix_en = strip_tags(prod_dict.get('prefix_en', "").replace('<br />', ' '))
            prod.subtitle_de = strip_tags(prod_dict.get('subtitle_de', "").replace('<br />', ' '))
            prod.subtitle_en = strip_tags(prod_dict.get('subtitle_en', "").replace('<br />', ' '))
            prod.original_de = strip_tags(prod_dict.get('original_de', "").replace('<br />', ' '))
            prod.original_en = strip_tags(prod_dict.get('original_en', "").replace('<br />', ' '))
            prod.website_de = prod_dict.get('website_de', "")
            prod.website_en = prod_dict.get('website_en', "")

            prod.slug = get_unique_value(Production, better_slugify(prod.title_de)[:200] or u"production",
                                         instance_pk=prod.pk)

            self.parse_and_use_texts(prod_dict, prod)

            prod.ensembles = prod_dict.get('ensembles', "")
            prod.organizers = prod_dict.get('organizers', "")
            prod.in_cooperation_with = prod_dict.get('in_cooperation_with', "")

            prod.free_entrance = (prod_dict.get('free_entrance', "") == "true")
            try:
                prod.price_from = Decimal(prod_dict.get('price_from', ""))
            except:
                prod.price_from = None
            try:
                prod.price_till = Decimal(prod_dict.get('price_till', ""))
            except:
                prod.price_till = None
            prod.tickets_website = prod_dict.get('tickets_website', "")
            prod.edu_offer_website = prod_dict.get('edu_offer_website', "")

            try:
                prod.age_from = int(prod_dict.get('age_from', ""))
            except:
                prod.age_from = None
            try:
                prod.age_till = int(prod_dict.get('age_till', ""))
            except:
                prod.age_till = None

            prod.location_title = prod_dict.get('location_title', "")
            prod.street_address = prod_dict.get('street_address', "")
            prod.street_address2 = prod_dict.get('street_address2', "")
            prod.postal_code = prod_dict.get('postal_code', "")
            prod.city = prod_dict.get('city', "")
            try:
                prod.latitude = float(prod_dict.get('latitude', ""))
            except:
                prod.latitude = None
            try:
                prod.longitude = float(prod_dict.get('longitude', ""))
            except:
                prod.longitude = None

            try:
                prod.language_and_subtitles = LanguageAndSubtitles.objects.get(
                    slug=prod_dict.get('language_and_subtitles_id', ""))
            except:
                prod.language_and_subtitles = None

            prod.classiccard = (prod_dict.get('classiccard', "") == "true")

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
            for location_id in prod_dict.get('in_program_of', {}).values():
                try:
                    location = Location.objects.get(pk=location_id)
                except Location.DoesNotExist:
                    pass
                else:
                    prod.in_program_of.add(location)

            prod.play_locations.clear()
            for location_id in prod_dict.get('play_locations', {}).values():
                if not self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID or self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID != location_id:
                    try:
                        location = Location.objects.get(pk=location_id)
                    except Location.DoesNotExist:
                        pass
                    else:
                        prod.play_locations.add(location)

            prod.play_stages.clear()
            for stage_id in prod_dict.get('play_stages', {}).values():
                try:
                    stage = Stage.objects.get(pk=stage_id)
                except Stage.DoesNotExist:
                    pass
                else:
                    prod.play_stages.add(stage)

            prod.categories.clear()
            for category_id in prod_dict.get('categories', {}).values():
                if isinstance(category_id, dict):  # category_id might be either an id or a dictionary with 'category_id' key
                    category_id = category_id['category_id']
                try:
                    cat = ProductionCategory.objects.get(pk=category_id)
                except ProductionCategory.DoesNotExist:
                    pass
                else:
                    prod.categories.add(cat)
            prod.fix_categories()

            prod.characteristics.clear()
            for ch_id in prod_dict.get('characteristics', {}).values():
                if isinstance(ch_id, dict):  # ch_id might be either an id or a dictionary with 'characteristic_id' key
                    ch_id = ch_id['characteristic_id']
                try:
                    ch = ProductionCharacteristics.objects.get(slug=ch_id)
                except ProductionCharacteristics.DoesNotExist:
                    pass
                else:
                    prod.characteristics.add(ch)

            # for owner in self.owners:
            #     prod.set_owner(owner)

            prod.productionvideo_set.all().delete()
            for video_dict in prod_dict.get('videos', {}).values():
                video = ProductionVideo(production=prod)
                video.creation_date = parse_datetime(video_dict.get('creation_date', ""))
                video.modified_date = parse_datetime(video_dict.get('modified_date', ""))
                video.title_de = video_dict.get('title_de', "")
                video.title_en = video_dict.get('title_en', "")
                video.link_or_embed = video_dict.get('embed', "")
                try:
                    video.sort_order = int(video_dict.get('sort_order', ""))
                except:
                    video.sort_order = 1
                video.save()

            prod.productionlivestream_set.all().delete()
            for live_stream_dict in prod_dict.get('live_streams', {}).values():
                ls = ProductionLiveStream(production=prod)
                ls.creation_date = parse_datetime(live_stream_dict.get('creation_date', ""))
                ls.modified_date = parse_datetime(live_stream_dict.get('modified_date', ""))
                ls.title_de = live_stream_dict.get('title_de', "")
                ls.title_en = live_stream_dict.get('title_en', "")
                ls.link_or_embed = live_stream_dict.get('embed', "")
                try:
                    ls.sort_order = int(live_stream_dict.get('sort_order', ""))
                except:
                    ls.sort_order = 1
                ls.save()

            if not self.skip_images:
                image_ids_to_keep = []
                for image_dict in prod_dict.get('images', {}).values():
                    image_url = image_dict.get('url', "")
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
                            file_description = self.save_file_description(mf.path, image_dict)
                        if not self.update_images:
                            continue

                    filename = image_url.split("/")[-1]
                    if "?" in filename:
                        # clear the query parameters
                        filename = filename.split("?")[0]
                    image_response = requests.get(image_url, auth=self.AUTH)
                    if image_response.status_code == 200:
                        image_mods.FileManager.save_file_for_object(
                            mf,
                            filename,
                            image_response.content,
                            field_name="path",
                            subpath="productions/{}/gallery/".format(prod.slug),
                        )
                        mf.copyright_restrictions = image_dict.get('copyright_restrictions', "") or "general_use"
                        mf.save()
                        image_ids_to_keep.append(mf.pk)

                        file_description = self.save_file_description(mf.path, image_dict)

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
            for pdf_dict in prod_dict.get('pdfs', {}).values():
                pdf_url = pdf_dict.get('url')
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
                        file_description = self.save_file_description(mf.path, pdf_dict)
                    continue

                filename = pdf_url.split("/")[-1]
                if "?" in filename:
                    # clear the query parameters
                    filename = filename.split("?")[0]
                pdf_response = requests.get(pdf_url, auth=self.AUTH)
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
                    file_description = self.save_file_description(mf.path, pdf_dict)

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
            for person_dict in prod_dict.get('leaders', {}).values():
                try:
                    prefix = Prefix.objects.get(slug=person_dict.get('prefix_id', ""))
                except:
                    prefix = None
                first_name = person_dict.get('first_name', "")
                last_name = person_dict.get('last_name', "")
                p, created = Person.objects.get_first_or_create(
                    prefix=prefix,
                    first_name=first_name,
                    last_name=last_name,
                )
                try:
                    imported_sort_order = int(person_dict.get('sort_order', ""))
                except:
                    imported_sort_order = 1
                prod.productionleadership_set.create(
                    person=p,
                    function_de=person_dict.get('function_de', ""),
                    function_en=person_dict.get('function_en', ""),
                    imported_sort_order=imported_sort_order,
                )
            for sort_order, item in enumerate(prod.productionleadership_set.order_by('imported_sort_order'), 0):
                item.sort_order = sort_order
                item.save()

            prod.productionauthorship_set.all().delete()
            for person_dict in prod_dict.get('authors', {}).values():
                try:
                    prefix = Prefix.objects.get(slug=person_dict.get('prefix_id', ""))
                except:
                    prefix = None
                first_name = person_dict.get('first_name', "")
                last_name = person_dict.get('last_name', "")
                p, created = Person.objects.get_first_or_create(
                    prefix=prefix,
                    first_name=first_name,
                    last_name=last_name,
                )
                try:
                    authorship_type = AuthorshipType.objects.get(
                        slug=person_dict.get('authorship_type_id', ""))
                except:
                    authorship_type = None
                try:
                    imported_sort_order = int(person_dict.get('sort_order', ""))
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
            for person_dict in prod_dict.get('participants', {}).values():
                try:
                    prefix = Prefix.objects.get(slug=person_dict.get('prefix_id', ""))
                except:
                    prefix = None
                first_name = person_dict.get('first_name', "")
                last_name = person_dict.get('last_name', "")
                p, created = Person.objects.get_first_or_create(
                    prefix=prefix,
                    first_name=first_name,
                    last_name=last_name,
                )
                try:
                    involvement_type = InvolvementType.objects.get(
                        slug=person_dict.get('involvement_type_id', ""))
                except:
                    involvement_type = None
                try:
                    imported_sort_order = int(person_dict.get('sort_order', ""))
                except:
                    imported_sort_order = 1
                prod.productioninvolvement_set.create(
                    person=p,
                    involvement_type=involvement_type,
                    involvement_role_de=person_dict.get('role_de', ""),
                    involvement_role_en=person_dict.get('role_en', ""),
                    involvement_instrument_de=person_dict.get('instrument_de', ""),
                    involvement_instrument_en=person_dict.get('instrument_en', ""),
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
            for sponsor_dict in prod_dict.get('sponsors', {}).values():
                sponsor = ProductionSponsor(
                    production=prod,
                    title_de=sponsor_dict.get('title_de', ""),
                    title_en=sponsor_dict.get('title_en', ""),
                    website=sponsor_dict.get('website', ""),
                )
                sponsor.save()
                image_url = sponsor_dict.get('image_url', "")
                if image_url:
                    filename = image_url.split("/")[-1]
                    if "?" in filename:
                        # clear the query parameters
                        filename = filename.split("?")[0]
                    image_response = requests.get(image_url, auth=self.AUTH)
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

            for event_dict in prod_dict.get('events', {}).values():

                external_event_id = event_dict.get('id', "")

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

                event.start_date = parse_datetime(event_dict.get('start_date', "")).date()
                event.start_time = parse_datetime(event_dict.get('start_time', "")).time()

                event.end_date = None
                end_date = event_dict.get('end_date', "")
                if end_date:
                    try:
                        event.end_date = parse_datetime(end_date).date()
                    except:
                        pass

                event.end_time = None
                end_time = event_dict.get('end_time', "")
                if end_time:
                    try:
                        event.end_time = parse_datetime().time()
                    except:
                        pass

                duration = None
                duration_str = event_dict.get('duration')
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
                    event.pauses = int(event_dict.get('pauses', ""))
                except:
                    event.pauses = None

                self.parse_and_use_texts(event_dict, event)

                event.organizers = event_dict.get('organizers', "")

                event.free_entrance = (event_dict.get('free_entrance', "") == "true")
                try:
                    event.price_from = Decimal(event_dict.get('price_from', ""))
                except:
                    event.price_from = None
                try:
                    event.price_till = Decimal(event_dict.get('price_till', ""))
                except:
                    event.price_till = None
                event.tickets_website = event_dict.get('tickets_website', "")
                event.location_title = event_dict.get('location_title', "")
                event.street_address = event_dict.get('street_address', "")
                event.street_address2 = event_dict.get('street_address2', "")
                event.postal_code = event_dict.get('postal_code', "")
                event.city = event_dict.get('city', "")
                try:
                    event.latitude = float(event_dict.get('latitude', ""))
                except:
                    event.latitude = None
                try:
                    event.longitude = float(event_dict.get('longitude', ""))
                except:
                    event.longitude = None

                try:
                    event.language_and_subtitles = LanguageAndSubtitles.objects.get(
                        slug=prod_dict.get('language_and_subtitles_id', ""))
                except:
                    event.language_and_subtitles = None

                event.event_status = event_dict.get('event_status', "")
                event.ticket_status = event_dict.get('ticket_status', "")

                event.classiccard = (event_dict.get('classiccard', "") == "true")

                event.save()
                self.event_ids_to_keep.add(event.pk)

                event.play_locations.clear()
                for location_id in event_dict.get('play_locations', {}).values():
                    if not self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID or self.DEFAULT_IN_PROGRAM_OF_LOCATION_ID != location_id:
                        try:
                            location = Location.objects.get(pk=location_id)
                        except Location.DoesNotExist:
                            pass
                        else:
                            event.play_locations.add(location)

                event.play_stages.clear()
                for stage_id in event_dict.get('play_stages', {}).values():
                    try:
                        stage = Stage.objects.get(pk=stage_id)
                    except Stage.DoesNotExist:
                        pass
                    else:
                        event.play_stages.add(stage)

                event.characteristics.clear()
                for ch_id in event_dict.get('characteristics', {}).values():
                    try:
                        ch = EventCharacteristics.objects.get(slug=ch_id)
                    except EventCharacteristics.DoesNotExist:
                        pass
                    else:
                        event.characteristics.add(ch)

                event.eventvideo_set.all().delete()
                for video_dict in event_dict.get('videos', {}).values():
                    video = EventVideo(event=event)
                    video.creation_date = parse_datetime(video_dict.get('creation_date', ""))
                    video.modified_date = parse_datetime(video_dict.get('modified_date', ""))
                    video.title_de = video_dict.get('title_de', "")
                    video.title_en = video_dict.get('title_en', "")
                    video.link_or_embed = video_dict.get('embed', "")
                    try:
                        video.sort_order = int(video_dict.get('sort_order', ""))
                    except:
                        video.sort_order = 1
                    video.save()

                event.eventlivestream_set.all().delete()
                for live_stream_dict in event_dict.get('live_streams', {}).values():
                    ls = EventLiveStream(event=event)
                    ls.creation_date = parse_datetime(live_stream_dict.get('creation_date', ""))
                    ls.modified_date = parse_datetime(live_stream_dict.get('modified_date', ""))
                    ls.title_de = live_stream_dict.get('title_de', "")
                    ls.title_en = live_stream_dict.get('title_en', "")
                    ls.link_or_embed = live_stream_dict.get('embed', "")
                    try:
                        ls.sort_order = int(live_stream_dict.get('sort_order', ""))
                    except:
                        ls.sort_order = 1
                    ls.save()

                if not self.skip_images:
                    image_ids_to_keep = []
                    for image_dict in event_dict.get('images', {}).values():
                        image_url = image_dict.get('url', "")
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
                                file_description = self.save_file_description(mf.path, image_dict)
                            if not self.update_images:
                                continue

                        filename = image_url.split("/")[-1]
                        if "?" in filename:
                            # clear the query parameters
                            filename = filename.split("?")[0]
                        image_response = requests.get(image_url, auth=self.AUTH)
                        if image_response.status_code == 200:
                            image_mods.FileManager.save_file_for_object(
                                mf,
                                filename,
                                image_response.content,
                                field_name="path",
                                subpath="productions/{}/events/gallery/".format(event.production.slug),
                            )
                            mf.copyright_restrictions = image_dict.get('copyright_restrictions', "") or "general_use"
                            mf.save()
                            image_ids_to_keep.append(mf.pk)
                            file_description = self.save_file_description(mf.path, image_dict)

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
                for pdf_dict in event_dict.get('pdfs', {}).values():
                    pdf_url = pdf_dict.get('url', "")
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
                            file_description = self.save_file_description(mf.path, pdf_dict)
                        continue

                    filename = pdf_url.split("/")[-1]
                    if "?" in filename:
                        # clear the query parameters
                        filename = filename.split("?")[0]
                    pdf_response = requests.get(pdf_url, auth=self.AUTH)
                    if pdf_response.status_code == 200:
                        image_mods.FileManager.save_file_for_object(
                            mf,
                            filename,
                            pdf_response.content,
                            field_name="path",
                            subpath="productions/{}/events/pdf/".format(event.production.slug),
                        )
                        mf.save()
                        pdf_ids_to_keep.append(mf.pk)
                        file_description = self.save_file_description(mf.path, pdf_dict)

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
                for person_dict in event_dict.get('leaders', {}).values():
                    try:
                        prefix = Prefix.objects.get(slug=person_dict.get('prefix_id', ""))
                    except:
                        prefix = None
                    first_name = person_dict.get('first_name', "")
                    last_name = person_dict.get('last_name', "")
                    p, created = Person.objects.get_first_or_create(
                        prefix=prefix,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    try:
                        imported_sort_order = int(person_dict.get('sort_order', ""))
                    except:
                        imported_sort_order = 1
                    event.eventleadership_set.create(
                        person=p,
                        function_de=person_dict.get('function_de', ""),
                        function_en=person_dict.get('function_en', ""),
                        imported_sort_order=imported_sort_order,
                    )
                for sort_order, item in enumerate(event.eventleadership_set.order_by('imported_sort_order'), 0):
                    item.sort_order = sort_order
                    item.save()

                event.eventauthorship_set.all().delete()
                for person_dict in event_dict.get('authors', {}).values():
                    try:
                        prefix = Prefix.objects.get(slug=person_dict.get('prefix_id', ""))
                    except:
                        prefix = None
                    first_name = person_dict.get('first_name', "")
                    last_name = person_dict.get('last_name', "")
                    p, created = Person.objects.get_first_or_create(
                        prefix=prefix,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    try:
                        authorship_type = AuthorshipType.objects.get(
                            slug=person_dict.get('authorship_type_id', ""))
                    except:
                        authorship_type = None
                    try:
                        imported_sort_order = int(person_dict.get('sort_order', ""))
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
                for person_dict in event_dict.get('participants', {}).values():
                    try:
                        prefix = Prefix.objects.get(slug=person_dict.get('prefix_id', ""))
                    except:
                        prefix = None
                    first_name = person_dict.get('first_name', "")
                    last_name = person_dict.get('last_name', "")
                    p, created = Person.objects.get_first_or_create(
                        prefix=prefix,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    try:
                        involvement_type = InvolvementType.objects.get(
                            slug=person_dict.get('involvement_type_id', ""))
                    except:
                        involvement_type = None
                    try:
                        imported_sort_order = int(person_dict.get('sort_order', ""))
                    except:
                        imported_sort_order = 1
                    event.eventinvolvement_set.create(
                        person=p,
                        involvement_type=involvement_type,
                        involvement_role_de=person_dict.get('role_de', ""),
                        involvement_role_en=person_dict.get('role_en', ""),
                        involvement_instrument_de=person_dict.get('instrument_de', ""),
                        involvement_instrument_en=person_dict.get('instrument_en', ""),
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
                for sponsor_dict in event_dict.get('sponsors', {}).values():
                    sponsor = EventSponsor(
                        event=event,
                        title_de=sponsor_dict.get('title_de', ""),
                        title_en=sponsor_dict.get('title_en', ""),
                        website=sponsor_dict.get('website', ""),
                    )
                    sponsor.save()
                    image_url = sponsor_dict.get('image_url', "")
                    if image_url:
                        filename = image_url.split("/")[-1]
                        if "?" in filename:
                            # clear the query parameters
                            filename = filename.split("?")[0]
                        image_response = requests.get(image_url, auth=self.AUTH)
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
