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
    help = "Imports productions and events from Komische Oper Berlin"

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        Service = models.get_model("external_services", "Service")

        self.CATEGORY_MAPPER = {
            7002: 74,  # Ausstellung
            6999: 25,  # Ballett
            6995: 35,  # Blues
            6988: 36,  # Chanson
            7009: 56,  # Comedy
            6994: 37,  # Country
            7003: 68,  # Diskussion
            7001: 38,  # Elektro
            7010: 76,  # Film
            6993: 39,  # Folk
            6986: 77,  # Fotografie
            6992: 40,  # Funk
            6987: 78,  # Fuhrung
            6991: 41,  # HipHop
            6990: 42,  # Jazz
            7008: 57,  # Kabarett
            7022: 8,  # Kinder/Jugend
            7013: 43,  # Klassik
            7017: 14,  # Komödie
            7019: 69,  # Konferenz
            6998: 17,  # Konzertante Vorstellung
            7020: 15,  # Lesung
            7000: 14,  # Liederabend
            7014: 18,  # Musical
            7018: 79,  # Neue Medien
            6996: 45,  # Neue Musik
            7024: 20,  # Oper
            7015: 22,  # Operette
            7012: 80,  # Party
            7016: 32,  # Performance
            7006: 46,  # Pop
            7007: 66,  # Puppentheater
            7026: 52,  # Revue
            7005: 47,  # Rock
            7028: 16,  # Schauspiel
            7025: 53,  # Show
            7023: 5,  # Sonstige Musik
            6989: 48,  # Soul
            7011: 49,  # Special
            6997: 27,  # Tanztheater
            7027: 54,  # Variete
            7021: 70,  # Vortrag
            7004: 82,  # Workshop
        }

        self.service, created = Service.objects.get_or_create(
            sysname="komische_oper_berlin_prods",
            defaults={
                'url': "http://www.komische-oper-berlin.de/cbstage/export.xml",
                'title': "Komische Oper Berlin Productions",
            },
        )

        r = requests.get(self.service.url, params={})
        self.helper_dict = {
            'prefix': '{http://export.culturebase.org/schema/event/CultureBaseExport}'
        }

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
        :param tag: the tag name without prefix of the children to get
        :param attrs: attributes of the children to match
        :return: text value of the selected child or empty string otherwise
        """
        all_attributes_match = True
        for child_node in node.findall('%(prefix)s%(tag)s' % dict(tag=tag, **self.helper_dict)):
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

        for prod_node in root_node.findall('%(prefix)sProduction' % self.helper_dict):
            external_prod_id = prod_node.get('Id')

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

            title_de = self.get_child_text(prod_node, 'Title', Language="de")
            title_en = self.get_child_text(prod_node, 'Title', Language="en")
            prod.title_de = title_de
            prod.title_en = title_en or title_de
            prod.website = self.get_child_text(prod_node, 'Url')

            if self.verbosity > NORMAL:
                print smart_str(title_de) + " | " + smart_str(title_en)

            prod.slug = get_unique_value(Production, slugify(prod.title_de))

            ticket_node = prod_node.find('%(prefix)sTicket' % self.helper_dict)
            if ticket_node is not None:
                prices = self.get_child_text(ticket_node, 'Price')
                if prices:
                    prod.price_from, prod.price_till = prices.split(u' - ')
                prod.tickets_website = self.get_child_text(ticket_node, 'TicketLink')

            pressetext_de = pressetext_en = u""
            kritik_de = kritik_en = u""
            werkinfo_kurz_de = werkinfo_kurz_en = u""
            werbezeile_de = werbezeile_en = u""
            werkinfo_gesamt_de = werkinfo_gesamt_en = u""
            hintergrundinformation_de = hintergrundinformation_en = u""
            inhaltsangabe_de = inhaltsangabe_en = u""
            programbuch_de = programbuch_en = u""
            for text_node in prod_node.findall('%(prefix)sText' % self.helper_dict):
                text_cat_id = int(text_node.find('%(prefix)sCategory' % self.helper_dict).get('Id'))
                text_de = self.get_child_text(text_node, 'Value', Language="de")
                text_en = self.get_child_text(text_node, 'Value', Language="en")
                if text_cat_id == 14:  # Beschreibungstext kurz
                    prod.teaser_de = text_de
                    prod.teaser_de_markup_type = 'pt'
                    prod.teaser_en = text_en
                    prod.teaser_en_markup_type = 'pt'
                elif text_cat_id == 15:  # Beschreibungstext lang
                    prod.description_de = text_de
                    prod.description_de_markup_type = 'pt'
                    prod.description_en = text_en
                    prod.description_en_markup_type = 'pt'
                elif text_cat_id == 16:  # Inhaltsangabe
                    inhaltsangabe_de = text_de
                    inhaltsangabe_en = text_en
                elif text_cat_id == 17:  # Konzertprogramm
                    prod.concert_programm_de = text_de
                    prod.concert_programm_de_markup_type = 'pt'
                    prod.concert_programm_en = text_en
                    prod.concert_programm_en_markup_type = 'pt'
                elif text_cat_id == 18:  # Koproduktion
                    prod.credits_de = text_de
                    prod.credits_de_markup_type = 'pt'
                    prod.credits_en = text_en
                    prod.credits_en_markup_type = 'pt'
                elif text_cat_id == 19:  # Kritik
                    kritik_de = text_de
                    kritik_en = text_en
                elif text_cat_id == 20:  # Originaltitel
                    prod.original_de = text_de
                    prod.original_en = text_en
                elif text_cat_id == 21:  # Pressetext
                    pressetext_de = text_de
                    pressetext_de = text_en
                elif text_cat_id == 22:  # Rahmenprogramm zur Veranstaltung
                    prod.supporting_programm_de = text_de
                    prod.supporting_programm_de_markup_type = 'pt'
                    prod.supporting_programm_en = text_en
                    prod.supporting_programm_en_markup_type = 'pt'
                elif text_cat_id == 23:  # Sondermerkmal
                    prod.remarks_de = text_de
                    prod.remarks_de_markup_type = 'pt'
                    prod.remarks_en = text_en
                    prod.remarks_en_markup_type = 'pt'
                elif text_cat_id == 24:  # Spieldauer
                    prod.duration_text_de = text_de
                    prod.duration_text_en = text_en
                elif text_cat_id == 25:  # Übertitel
                    prod.subtitles_text_de = text_de
                    prod.subtitles_text_en = text_en
                elif text_cat_id == 26:  # Werbezeile
                    werbezeile_de = text_de
                    werbezeile_en = text_en
                elif text_cat_id == 27:  # Werkinfo gesamt
                    werkinfo_gesamt_de = text_de
                    werkinfo_gesamt_en = text_en
                elif text_cat_id == 28:  # Werkinfo kurz
                    werkinfo_kurz_de = text_de
                    werkinfo_kurz_en = text_en
                elif text_cat_id == 29:  # zusätzliche Preisinformationen
                    prod.price_information_de = text_de
                    prod.price_information_de_markup_type = 'pt'
                    prod.price_information_en = text_en
                    prod.price_information_en_markup_type = 'pt'
                elif text_cat_id == 30:  # Titelprefix
                    prod.prefix_de = text_de
                    prod.prefix_en = text_en
                elif text_cat_id == 35:  # Programmbuch
                    programbuch_de = text_de
                    programbuch_en = text_en
                elif text_cat_id == 36:  # Hintergrundinformation
                    hintergrundinformation_de = text_de
                    hintergrundinformation_en = text_en
                elif text_cat_id == 39:  # Altersangabe
                    prod.age_text_de = text_de
                    prod.age_text_en = text_en
                elif text_cat_id == 40:  # Audio & Video
                    pass

            prod.press_text_de = pressetext_de + u'\n' + kritik_de
            prod.press_text_de_markup_type = 'pt'
            prod.press_text_en = pressetext_en + u'\n' + kritik_en
            prod.press_text_en_markup_type = 'pt'

            prod.teaser_de = werkinfo_kurz_de + u'\n' + werbezeile_de
            prod.teaser_de_markup_type = 'pt'
            prod.teaser_en = werkinfo_kurz_en + u'\n' + werbezeile_en
            prod.teaser_en_markup_type = 'pt'

            prod.work_info_de = werkinfo_gesamt_de + u'\n' + hintergrundinformation_de
            prod.work_info_de_markup_type = 'pt'
            prod.work_info_en = werkinfo_gesamt_en + u'\n' + hintergrundinformation_en
            prod.work_info_en_markup_type = 'pt'

            prod.contents_de = inhaltsangabe_de + u'\n' + programbuch_de
            prod.contents_de_markup_type = 'pt'
            prod.contents_en = inhaltsangabe_en + u'\n' + programbuch_en
            prod.contents_en_markup_type = 'pt'

            prod.save()

            venue_node = prod_node.find('%(prefix)sVenue' % self.helper_dict)
            if venue_node:
                location, created = self.create_or_update_location(venue_node)
                if location:
                    prod.play_locations.clear()
                    prod.play_locations.add(location)

            if not self.skip_images and not prod.productionimage_set.count():
                for picture_node in prod_node.findall('%(prefix)sPicture' % self.helper_dict):
                    image_url = self.get_child_text(picture_node, 'Url')
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
                        if self.get_child_text(picture_node, 'PublishType') == "publish_type_for_free_use":
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

                        file_description.title_de = self.get_child_text(picture_node, 'Title', Language="de")
                        file_description.title_en = self.get_child_text(picture_node, 'Title', Language="en")
                        file_description.description_de = self.get_child_text(picture_node, 'Description', Language="de")
                        file_description.description_en = self.get_child_text(picture_node, 'Description', Language="en")
                        file_description.author = self.get_child_text(picture_node, 'Photographer')
                        file_description.save()
                        time.sleep(1)

            for category_id_node in prod_node.findall('%(prefix)sContentCategory/%(prefix)sCategoryId' % self.helper_dict):
                internal_cat_id = self.CATEGORY_MAPPER.get(int(category_id_node.text), None)
                if internal_cat_id:
                    prod.categories.add(ProductionCategory.objects.get(pk=internal_cat_id))

            if not prod.productioninvolvement_set.count():
                for person_node in prod_node.findall('%(prefix)sPerson' % self.helper_dict):
                    first_name, last_name = self.get_child_text(person_node, 'Name').rsplit(" ", 1)
                    role_de = self.get_child_text(person_node, 'RoleDescription', Language="de")
                    role_en = self.get_child_text(person_node, 'RoleDescription', Language="en")
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
                        sort_order=person_node.get('Position'),
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

            for event_node in prod_node.findall('%(prefix)sEvent' % self.helper_dict):

                external_event_id = event_node.get('Id')

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

                ticket_node = event_node.find('%(prefix)sTicket' % self.helper_dict)
                if ticket_node is not None:
                    prices = self.get_child_text(ticket_node, 'Price')
                    if prices:
                        event.price_from, event.price_till = prices.split(u' - ')
                    event.tickets_website = self.get_child_text(ticket_node, 'TicketLink')

                flag_status = event_node.find('%(prefix)sFlagStatus' % self.helper_dict).get('Id')
                if flag_status == 0:  # fällt aus
                    event.event_status = 'canceled'
                elif flag_status == 1:  # findet statt
                    event.event_status = 'takes_place'
                elif flag_status == 2:  # ausverkauft
                    event.ticket_status = 'sold_out'

                pressetext_de = pressetext_en = u""
                kritik_de = kritik_en = u""
                werkinfo_kurz_de = werkinfo_kurz_en = u""
                werbezeile_de = werbezeile_en = u""
                werkinfo_gesamt_de = werkinfo_gesamt_en = u""
                hintergrundinformation_de = hintergrundinformation_en = u""
                inhaltsangabe_de = inhaltsangabe_en = u""
                programbuch_de = programbuch_en = u""
                for text_node in event_node.findall('%(prefix)sText' % self.helper_dict):
                    text_cat_id = int(text_node.find('%(prefix)sCategory' % self.helper_dict).get('Id'))
                    text_de = self.get_child_text(text_node, 'Value', Language="de")
                    text_en = self.get_child_text(text_node, 'Value', Language="en")
                    if text_cat_id == 14:  # Beschreibungstext kurz
                        event.teaser_de = text_de
                        event.teaser_de_markup_type = 'pt'
                        event.teaser_en = text_en
                        event.teaser_en_markup_type = 'pt'
                    elif text_cat_id == 15:  # Beschreibungstext lang
                        event.description_de = text_de
                        event.description_de_markup_type = 'pt'
                        event.description_en = text_en
                        event.description_en_markup_type = 'pt'
                    elif text_cat_id == 16:  # Inhaltsangabe
                        inhaltsangabe_de = text_de
                        inhaltsangabe_en = text_en
                    elif text_cat_id == 17:  # Konzertprogramm
                        event.concert_programm_de = text_de
                        event.concert_programm_de_markup_type = 'pt'
                        event.concert_programm_en = text_en
                        event.concert_programm_en_markup_type = 'pt'
                    elif text_cat_id == 18:  # Koproduktion
                        event.credits_de = text_de
                        event.credits_de_markup_type = 'pt'
                        event.credits_en = text_en
                        event.credits_en_markup_type = 'pt'
                    elif text_cat_id == 19:  # Kritik
                        kritik_de = text_de
                        kritik_en = text_en
                    elif text_cat_id == 20:  # Originaltitel
                        pass
                    elif text_cat_id == 21:  # Pressetext
                        pressetext_de = text_de
                        pressetext_en = text_en
                    elif text_cat_id == 22:  # Rahmenprogramm zur Veranstaltung
                        event.supporting_programm_de = text_de
                        event.supporting_programm_de_markup_type = 'pt'
                        event.supporting_programm_en = text_en
                        event.supporting_programm_en_markup_type = 'pt'
                    elif text_cat_id == 23:  # Sondermerkmal
                        event.remarks_de = text_de
                        event.remarks_de_markup_type = 'pt'
                        event.remarks_en = text_en
                        event.remarks_en_markup_type = 'pt'
                    elif text_cat_id == 24:  # Spieldauer
                        event.duration_text_de = text_de
                        event.duration_text_en = text_en
                    elif text_cat_id == 25:  # Übertitel
                        event.subtitles_text_de = text_de
                        event.subtitles_text_en = text_en
                    elif text_cat_id == 26:  # Werbezeile
                        werbezeile_de = text_de
                        werbezeile_en = text_en
                    elif text_cat_id == 27:  # Werkinfo gesamt
                        werkinfo_gesamt_de = text_de
                        werkinfo_gesamt_en = text_en
                    elif text_cat_id == 28:  # Werkinfo kurz
                        werkinfo_kurz_de = text_de
                        werkinfo_kurz_en = text_en
                    elif text_cat_id == 29:  # zusätzliche Preisinformationen
                        event.price_information_de = text_de
                        event.price_information_de_markup_type = 'pt'
                        event.price_information_en = text_en
                        event.price_information_en_markup_type = 'pt'
                    elif text_cat_id == 30:  # Titelprefix
                        pass
                    elif text_cat_id == 35:  # Programmbuch
                        programbuch_de = text_de
                        programbuch_en = text_en
                    elif text_cat_id == 36:  # Hintergrundinformation
                        hintergrundinformation_de = text_de
                        hintergrundinformation_en = text_en
                    elif text_cat_id == 39:  # Altersangabe
                        event.age_text_de = text_de
                        event.age_text_en = text_en
                    elif text_cat_id == 40:  # Audio & Video
                        pass

                event.press_text_de = pressetext_de + u'\n' + kritik_de
                event.press_text_de_markup_type = 'pt'
                event.press_text_en = pressetext_en + u'\n' + kritik_en
                event.press_text_en_markup_type = 'pt'

                event.teaser_de = werkinfo_kurz_de + u'\n' + werbezeile_de
                event.teaser_de_markup_type = 'pt'
                event.teaser_en = werkinfo_kurz_en + u'\n' + werbezeile_en
                event.teaser_en_markup_type = 'pt'

                event.work_info_de = werkinfo_gesamt_de + u'\n' + hintergrundinformation_de
                event.work_info_de_markup_type = 'pt'
                event.work_info_en = werkinfo_gesamt_en + u'\n' + hintergrundinformation_en
                event.work_info_en_markup_type = 'pt'

                event.contents_de = inhaltsangabe_de + u'\n' + programbuch_de
                event.contents_de_markup_type = 'pt'
                event.contents_en = inhaltsangabe_en + u'\n' + programbuch_en
                event.contents_en_markup_type = 'pt'

                event.save()

                if not self.skip_images and not event.eventimage_set.count():
                    for picture_node in event_node.findall('%(prefix)sPicture' % self.helper_dict):
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
                            if self.get_child_text(picture_node, 'PublishType') == "publish_type_for_free_use":
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

                            file_description.title_de = self.get_child_text(picture_node, 'Title', Language="de")
                            file_description.title_en = self.get_child_text(picture_node, 'Title', Language="en")
                            file_description.description_de = self.get_child_text(picture_node, 'Description', Language="de")
                            file_description.description_en = self.get_child_text(picture_node, 'Description', Language="en")
                            file_description.author = self.get_child_text(picture_node, 'Photographer')
                            file_description.save()
                            time.sleep(1)

                venue_node = event_node.find('%(prefix)sVenue' % self.helper_dict)
                if venue_node:
                    location, created = self.create_or_update_location(venue_node)
                    if location:
                        event.play_locations.clear()
                        event.play_locations.add(location)

                if not event.eventinvolvement_set.count():
                    for person_node in event_node.findall('%(prefix)sPerson' % self.helper_dict):
                        first_name, last_name = self.get_child_text(person_node, 'Name').rsplit(" ", 1)
                        role_de = self.get_child_text(person_node, 'RoleDescription', Language="de")
                        role_en = self.get_child_text(person_node, 'RoleDescription', Language="en")
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
                            sort_order=person_node.get('Position'),
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
