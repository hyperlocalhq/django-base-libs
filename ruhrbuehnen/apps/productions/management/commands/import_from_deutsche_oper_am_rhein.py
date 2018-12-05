# -*- coding: UTF-8 -*-
from ._import_from_culturebase_base_xml import ImportFromCulturebaseBase


class Command(ImportFromCulturebaseBase):
    help = "Imports productions and events from Culturebase / Deutsche Oper am Rhein"
    WHITELISTED_VENUE_IDS = [
        4413,  # Theater Duisburg
        47069,  # Theater Duisburg – Opernfoyer
    ]

    def prepare(self):
        from django.apps import apps
        from ruhrbuehnen.apps.locations.models import Location

        self.load_and_parse_locations()

        self.in_program_of, created = Location.objects.get_or_create(
            title_de=u"Deutsche Oper am Rhein im Theater Duisburg",
            defaults={
                'title_en': u"Deutsche Oper am Rhein im Theater Duisburg",
                'slug': 'deutsche-oper-am-rhein-im-theater-duisburg',
                'street_address': u'Opernplatz',
                'postal_code': u'47051',
                'city': u'Duisburg',
            },
        )
        self.owners = list(self.in_program_of.get_owners())

        Service = apps.get_model("external_services", "Service")

        URL = "https://export.culturebase.org/studio_38/event/dor.xml"
        self.service, created = Service.objects.get_or_create(
            sysname="culturebase_deutsche_oper_am_rhein_prods",
            defaults={
                'url': URL,
                'title': "Culturebase Radialsystem Productions",
            },
        )
        if self.service.url != URL:
            self.service.url = URL
            self.service.save()

        self.helper_dict = {
            'prefix':
                '{http://export.culturebase.org/schema/event/CultureBaseExport}'
        }

    def save_page(self, root_node):
        import requests
        from dateutil.parser import parse as parse_datetime

        from django.apps import apps
        from django.db import models

        from base_libs.utils.betterslugify import better_slugify
        from base_libs.utils.misc import get_unique_value

        from ruhrbuehnen.apps.people.models import AuthorshipType, Person
        from ruhrbuehnen.apps.productions.models import (
            Production,
            ProductionImage,
            ProductionCategory,
            ProductionCharacteristics,
            ProductionSponsor,
            Event,
            EventImage,
            EventCharacteristics,
        )

        ObjectMapper = apps.get_model("external_services", "ObjectMapper")
        image_mods = apps.get_app("image_mods")

        prod_nodes = root_node.findall(
            '%(prefix)sProduction' % self.helper_dict
        )
        prods_count = len(prod_nodes)

        for prod_index, prod_node in enumerate(prod_nodes, 1):
            external_prod_id = prod_node.get('Id')

            title_de = self.get_child_text(
                prod_node, 'Title', Language="de"
            ).replace('\n', ' ').strip()
            title_en = self.get_child_text(
                prod_node, 'Title', Language="en"
            ).replace('\n', ' ').strip()
            if self.verbosity >= self.NORMAL:
                self.stdout.write(
                    u"%d/%d %s | %s" %
                    (prod_index, prods_count, title_de, title_en)
                )
                self.stdout.flush()

            venue_node = prod_node.find('./%(prefix)sVenue' % self.helper_dict)
            if not (venue_node and int(venue_node.get('Id')) in self.WHITELISTED_VENUE_IDS):
                self.stats['prods_skipped'] += 1
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
                if not prod:
                    # if production was deleted after import,
                    # don't import it again
                    self.stats['prods_skipped'] += 1
                    continue
                if prod.status == "trashed":
                    self.stats['prods_untrashed'] += 1
                # else:
                #     if parse_datetime(production_dict['lastaction'], ignoretz=True) < datetime.now() - timedelta(days=1):
                #         self.stats['prods_skipped'] += 1
                #         continue

            if prod.no_overwriting:
                self.stats['prods_skipped'] += 1
                continue

            prod.status = self.DEFAULT_PUBLISHING_STATUS
            prod.title_de = title_de
            prod.title_en = title_en or title_de
            prod.website_de = prod.website_en = self.get_child_text(
                prod_node, 'Url'
            )

            prod.slug = get_unique_value(
                Production,
                better_slugify(prod.title_de)[:200] or u"production",
                instance_pk=prod.pk
            )

            ticket_node = prod_node.find(
                './%(prefix)sTicket' % self.helper_dict
            )
            if ticket_node is not None:
                prices = self.get_child_text(ticket_node, 'Price')
                if prices:
                    prod.price_from, prod.price_till = prices.split(u' - ')
                prod.tickets_website = self.get_child_text(
                    ticket_node, 'TicketLink'
                )

            self.parse_and_use_texts(prod_node, prod)

            prod.save()
            self.production_ids_to_keep.add(prod.pk)

            venue_node = prod_node.find('./%(prefix)sVenue' % self.helper_dict)
            if venue_node is not None:
                location, stage = self.get_updated_location_and_stage(
                    venue_node
                )
                if location:
                    prod.play_locations.clear()
                    prod.play_locations.add(location)

                if stage:
                    if isinstance(stage, dict):
                        prod.location_title = stage['title']
                        prod.street_address = stage['street_address']
                        prod.postal_code = stage['postal_code']
                        prod.city = stage['city']
                        prod.save()
                    else:
                        prod.play_stages.clear()
                        prod.play_stages.add(stage)
            free_text_venue = self.get_child_text(prod_node, 'FreeTextVenue')
            if free_text_venue:
                location, stage = self.get_updated_location_and_stage_from_free_text(
                    free_text_venue
                )
                if location:
                    prod.play_locations.clear()
                    prod.play_locations.add(location)
                # else:
                #    prod.location_title = free_text_venue
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

            if self.in_program_of:
                prod.in_program_of.add(self.in_program_of)

            for owner in self.owners:
                prod.set_owner(owner)

            organizers_list = []
            for organisation_node in prod_node.findall(
                    './%(prefix)sOrganisation' % self.helper_dict
            ):
                organizers_list.append(
                    self.get_child_text(organisation_node, 'Name')
                )

            if organizers_list:
                prod.organizers = u', '.join(organizers_list)
                prod.save()

            if not self.skip_images:
                image_ids_to_keep = []
                for picture_node in prod_node.findall(
                        './%(prefix)sPicture' % self.helper_dict
                ):
                    image_url = self.get_child_text(picture_node, 'Url')

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
                        # or create a new production and then create a mapper
                        mf = ProductionImage(production=prod)
                    else:
                        mf = image_mapper.content_object
                        if mf:
                            image_ids_to_keep.append(mf.pk)
                            # update description
                            file_description = self.save_file_description(
                                mf.path, picture_node
                            )
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
                    if image_response.status_code == 200:
                        image_mods.FileManager.delete_file_for_object(
                            mf,
                            field_name="path",
                        )
                        image_mods.FileManager.save_file_for_object(
                            mf,
                            filename,
                            image_response.content,
                            field_name="path",
                            subpath="productions/%s/gallery/" % prod.slug,
                        )
                        if self.get_child_text(
                                picture_node, 'PublishType'
                        ) == "publish_type_for_free_use":
                            mf.copyright_restrictions = "general_use"
                        else:
                            mf.copyright_restrictions = "protected"
                        mf.save()
                        image_ids_to_keep.append(mf.pk)

                        file_description = self.save_file_description(
                            mf.path, picture_node
                        )

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

            prod.categories.clear()
            for category_id_node in prod_node.findall(
                    './%(prefix)sContentCategory/%(prefix)sCategoryId' %
                    self.helper_dict
            ):
                internal_cat_id = self.CATEGORY_MAPPER.get(
                    int(category_id_node.text), None
                )
                if internal_cat_id:
                    cats = ProductionCategory.objects.filter(pk=internal_cat_id)
                    if cats:
                        prod.categories.add(cats[0])
                        if cats[0].parent:
                            prod.categories.add(cats[0].parent)

            prod.characteristics.clear()
            for status_node in prod_node.findall(
                    './%(prefix)sStatus' % self.helper_dict
            ):
                internal_ch_slug = self.PRODUCTION_CHARACTERISTICS_MAPPER.get(
                    int(status_node.get('Id')), None
                )
                if internal_ch_slug:
                    prod.characteristics.add(
                        ProductionCharacteristics.objects.get(
                            slug=internal_ch_slug
                        )
                    )
                elif int(status_node.get('Id')) == 25:
                    prod.categories.add(
                        ProductionCategory.objects.get(slug="kinder-jugend")
                    )

            prod.productionleadership_set.all().delete()
            prod.productionauthorship_set.all().delete()
            prod.productioninvolvement_set.all().delete()
            for person_node in prod_node.findall(
                    './%(prefix)sPerson' % self.helper_dict
            ):
                first_and_last_name = self.get_child_text(person_node, 'Name')
                if u" " in first_and_last_name:
                    first_name, last_name = first_and_last_name.rsplit(" ", 1)
                else:
                    first_name = ""
                    last_name = first_and_last_name
                role_de = self.get_child_text(
                    person_node, 'RoleDescription', Language="de"
                )
                role_en = self.get_child_text(
                    person_node, 'RoleDescription', Language="en"
                )
                if not role_de and person_node.find(
                        '%(prefix)sCategory' % self.helper_dict
                ) is not None:
                    role_de, role_en = self.ROLE_ID_MAPPER[int(
                        person_node.find(
                            '%(prefix)sCategory' % self.helper_dict
                        ).get("Id")
                    )]

                if role_de in self.authorship_types_de:
                    authorship_type = AuthorshipType.objects.get(
                        title_de=role_de
                    )
                    p, created = Person.objects.get_first_or_create(
                        first_name=first_name,
                        last_name=last_name,
                    )
                    prod.productionauthorship_set.create(
                        person=p,
                        authorship_type=authorship_type,
                        imported_sort_order=person_node.get('Position'),
                    )
                elif role_de in (u"Regie", u"Regisseur", u"Regisseurin"):
                    p, created = Person.objects.get_first_or_create(
                        first_name=first_name,
                        last_name=last_name,
                    )
                    prod.productionleadership_set.create(
                        person=p,
                        function_de=role_de,
                        function_en=role_en,
                        imported_sort_order=person_node.get('Position'),
                    )
                else:
                    p, created = Person.objects.get_first_or_create(
                        first_name=first_name,
                        last_name=last_name,
                    )
                    prod.productioninvolvement_set.create(
                        person=p,
                        involvement_role_de=role_de,
                        involvement_role_en=role_en,
                        imported_sort_order=person_node.get('Position'),
                    )
            for sort_order, item in enumerate(
                    prod.productionauthorship_set.order_by('imported_sort_order'), 0
            ):
                item.sort_order = sort_order
                item.save()
            for sort_order, item in enumerate(
                    prod.productionleadership_set.order_by('imported_sort_order'), 0
            ):
                item.sort_order = sort_order
                item.save()
            for sort_order, item in enumerate(
                    prod.productioninvolvement_set.order_by('imported_sort_order'),
                    0
            ):
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
            for sponsor_node in prod_node.findall(
                    './%(prefix)sSponsor' % self.helper_dict
            ):
                sponsor = ProductionSponsor(production=prod)
                sponsor.title_de = self.get_child_text(
                    sponsor_node, 'Description', Language="de"
                )
                sponsor.title_en = self.get_child_text(
                    sponsor_node, 'Description', Language="en"
                )
                sponsor.website = self.get_child_text(sponsor_node, 'Url')
                sponsor.save()
                image_url = self.get_child_text(sponsor_node, 'ImageUrl')
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

            for event_node in prod_node.findall(
                    '%(prefix)sEvent' % self.helper_dict
            ):

                external_event_id = event_node.get('Id')

                venue_node = event_node.find(
                    '%(prefix)sVenue' % self.helper_dict
                )

                if venue_node and int(venue_node.get('Id')) not in self.WHITELISTED_VENUE_IDS:
                    self.stats['events_skipped'] += 1
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
                    event = Event()
                else:
                    event = event_mapper.content_object
                    if not event:
                        # don't import deleted events again
                        self.stats['events_skipped'] += 1
                        continue

                event.production = prod

                start_date_str = self.get_child_text(event_node, 'Date')
                if start_date_str:
                    event.start_date = parse_datetime(start_date_str).date()
                start_time_str = self.get_child_text(event_node, 'Begin')
                if start_time_str:
                    event.start_time = parse_datetime(start_time_str).time()
                end_time_str = self.get_child_text(event_node, 'End')
                if end_time_str:
                    event.end_time = parse_datetime(end_time_str).time()
                duration_str = self.get_child_text(event_node, 'Duration')
                if duration_str:
                    event.duration = int(duration_str)

                ticket_node = event_node.find(
                    '%(prefix)sTicket' % self.helper_dict
                )
                if ticket_node is not None:
                    prices = self.get_child_text(ticket_node, 'Price')
                    if prices:
                        event.price_from, event.price_till = prices.split(
                            u' - '
                        )
                    event.tickets_website = self.get_child_text(
                        ticket_node, 'TicketLink'
                    )

                flag_status = event_node.find(
                    '%(prefix)sFlagStatus' % self.helper_dict
                ).get('Id')
                if flag_status == 0:  # fällt aus
                    if event.event_status == "trashed":
                        self.stats['events_untrashed'] += 1
                    event.event_status = 'canceled'
                elif flag_status == 1:  # findet statt
                    if event.event_status == "trashed":
                        self.stats['events_untrashed'] += 1
                    event.event_status = 'takes_place'
                elif flag_status == 2:  # ausverkauft
                    event.ticket_status = 'sold_out'

                self.parse_and_use_texts(event_node, event)

                organisation_node = event_node.find(
                    './%(prefix)sOrganisation' % self.helper_dict
                )
                if organisation_node:
                    event.organizers = self.get_child_text(
                        organisation_node, 'Name'
                    )

                event.save()
                self.event_ids_to_keep.add(event.pk)

                if not self.skip_images:
                    image_ids_to_keep = []
                    for picture_node in event_node.findall(
                            '%(prefix)sPicture' % self.helper_dict
                    ):
                        image_url = self.get_child_text(picture_node, 'Url')

                        image_external_id = "event-%s-%s" % (
                            event.pk, image_url
                        )
                        image_mapper = None
                        try:
                            # get image model instance from saved mapper
                            image_mapper = self.service.objectmapper_set.get(
                                external_id=image_external_id,
                                content_type__app_label="productions",
                                content_type__model="eventimage",
                            )
                        except models.ObjectDoesNotExist:
                            # or create a new production and then create a mapper
                            mf = EventImage(event=event)
                        else:
                            mf = image_mapper.content_object
                            if mf:
                                image_ids_to_keep.append(mf.pk)
                                file_description = self.save_file_description(
                                    mf.path, picture_node
                                )
                            else:
                                if self.update_images:
                                    # restore image
                                    mf = EventImage(event=event)
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
                        if image_response.status_code == 200:
                            image_mods.FileManager.delete_file_for_object(
                                mf,
                                field_name="path",
                            )
                            image_mods.FileManager.save_file_for_object(
                                mf,
                                filename,
                                image_response.content,
                                field_name="path",
                                subpath="productions/%s/events/%s/gallery/" %
                                        (prod.slug, event.pk),
                            )
                            if self.get_child_text(
                                    picture_node, 'PublishType'
                            ) == "publish_type_for_free_use":
                                mf.copyright_restrictions = "general_use"
                            else:
                                mf.copyright_restrictions = "protected"
                            mf.save()
                            image_ids_to_keep.append(mf.pk)

                            file_description = self.save_file_description(
                                mf.path, picture_node
                            )

                            if not image_mapper:
                                image_mapper = ObjectMapper(
                                    service=self.service,
                                    external_id=image_external_id,
                                )
                            image_mapper.content_object = mf
                            image_mapper.save()

                    for mf in event.eventimage_set.exclude(
                            pk__in=image_ids_to_keep
                    ):
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

                if venue_node is not None:
                    location, stage = self.get_updated_location_and_stage(
                        venue_node
                    )
                    if location:
                        event.play_locations.clear()
                        event.play_locations.add(location)

                    if stage:
                        if isinstance(stage, dict):
                            event.location_title = stage['title']

                            event.street_address = stage['street_address']
                            event.postal_code = stage['postal_code']
                            event.city = stage['city']
                            event.save()
                        else:
                            event.play_stages.clear()
                            event.play_stages.add(stage)
                free_text_venue = self.get_child_text(
                    prod_node, 'FreeTextVenue'
                )
                if free_text_venue:
                    location, stage = self.get_updated_location_and_stage_from_free_text(
                        free_text_venue
                    )
                    if location:
                        event.play_locations.clear()
                        event.play_locations.add(location)
                    # else:
                    #    event.location_title = free_text_venue
                    #    event.save()

                    if stage:
                        if isinstance(stage, dict):
                            event.location_title = stage['title']
                            event.street_address = stage.get(
                                'street_address', u''
                            )
                            event.postal_code = stage.get('postal_code', u'')
                            event.city = stage.get('city', u'Berlin')
                            event.save()
                        else:
                            event.play_stages.clear()
                            event.play_stages.add(stage)

                event.characteristics.clear()
                for status_node in event_node.findall(
                        '%(prefix)sStatus' % self.helper_dict
                ):
                    internal_ch_slug = self.EVENT_CHARACTERISTICS_MAPPER.get(
                        int(status_node.get('Id')), None
                    )
                    if internal_ch_slug:
                        event.characteristics.add(
                            EventCharacteristics.objects.get(
                                slug=internal_ch_slug
                            )
                        )

                event.eventauthorship_set.all().delete()
                event.eventleadership_set.all().delete()
                event.eventinvolvement_set.all().delete()
                for person_node in event_node.findall(
                        '%(prefix)sPerson' % self.helper_dict
                ):
                    first_and_last_name = self.get_child_text(
                        person_node, 'Name'
                    )
                    if u" " in first_and_last_name:
                        first_name, last_name = first_and_last_name.rsplit(
                            " ", 1
                        )
                    else:
                        first_name = ""
                        last_name = first_and_last_name
                    role_de = self.get_child_text(
                        person_node, 'RoleDescription', Language="de"
                    )
                    role_en = self.get_child_text(
                        person_node, 'RoleDescription', Language="en"
                    )
                    if not role_de and person_node.find(
                            '%(prefix)sCategory' % self.helper_dict
                    ) is not None:
                        role_de, role_en = self.ROLE_ID_MAPPER[int(
                            person_node.find(
                                '%(prefix)sCategory' % self.helper_dict
                            ).get("Id")
                        )]

                    if role_de in self.authorship_types_de:
                        authorship_type = AuthorshipType.objects.get(
                            title_de=role_de
                        )
                        p, created = Person.objects.get_first_or_create(
                            first_name=first_name,
                            last_name=last_name,
                        )
                        event.eventauthorship_set.create(
                            person=p,
                            authorship_type=authorship_type,
                            imported_sort_order=person_node.get('Position'),
                        )
                    elif role_de in (u"Regie",):
                        p, created = Person.objects.get_first_or_create(
                            first_name=first_name,
                            last_name=last_name,
                        )
                        event.eventleadership_set.create(
                            person=p,
                            function_de=role_de,
                            function_en=role_en,
                            imported_sort_order=person_node.get('Position'),
                        )
                    else:
                        p, created = Person.objects.get_first_or_create(
                            first_name=first_name,
                            last_name=last_name,
                        )
                        event.eventinvolvement_set.create(
                            person=p,
                            involvement_role_de=role_de,
                            involvement_role_en=role_en,
                            imported_sort_order=person_node.get('Position'),
                        )
                for sort_order, item in enumerate(
                        event.eventauthorship_set.order_by('imported_sort_order'), 0
                ):
                    item.sort_order = sort_order
                    item.save()
                for sort_order, item in enumerate(
                        event.eventleadership_set.order_by('imported_sort_order'), 0
                ):
                    item.sort_order = sort_order
                    item.save()
                for sort_order, item in enumerate(
                        event.eventinvolvement_set.order_by('imported_sort_order'),
                        0
                ):
                    item.sort_order = sort_order
                    item.save()

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
