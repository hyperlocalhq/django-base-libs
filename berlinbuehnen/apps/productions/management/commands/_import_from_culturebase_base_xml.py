# -*- coding: UTF-8 -*-

import re
import requests
from xml.etree import ElementTree
from dateutil.parser import parse as parse_datetime
from optparse import make_option
import csv

from django.core.management.base import NoArgsCommand
from django.utils.encoding import force_unicode
from django.db import models

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
from berlinbuehnen.apps.people.models import Person, AuthorshipType

from _import_from_heimat_base_xml import LOCATIONS_TO_SKIP, STAGE_TO_LOCATION_MAPPER, PRODUCTION_VENUES, convert_location_title, CultureBaseLocation

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class ImportFromCulturebaseBase(object):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells Django to NOT download images.'),
    )
    help = "Imports productions and events from Culturebase"

    LOCATIONS_BY_TITLE = {}

    CATEGORY_MAPPER = {
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
        #7017: 14,  # Komödie
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

    PRODUCTION_CHARACTERISTICS_MAPPER = {
        1: '',  # Premiere
        2: 'wiederaufnahme',  # Wiederaufnahme
        3: '',  # Vorauffuhrung
        5: '',  # Publikumsgespräch
        6: 'gastspiel',  # Gastspiel
        11: '',  # öffentliche Probe
        17: '',  # Deutsche Erstauffuhrung
        21: 'repertoire',  # Repertoire
        22: '',  # zum letzten Mal
        23: 'urauffuehrung',  # Urauffuhrung
        24: '',  # Familienvorstellung
        25: '',  # Kindervorstellung
        27: '',  # Einfuhrung
        28: '',  # zum letzten Mal in dieser Spielzeit
        30: '',  # Deutschsprachige Erstauffuhrung
        31: 'on-tour',  # On Tour
        33: '',  # B-Premiere
        34: '',  # Matinee
        35: '',  # Schulervorstellung
        36: '',  # Volkstheater
    }

    EVENT_CHARACTERISTICS_MAPPER = {
        1: 'premiere',  # Premiere
        2: '',  # Wiederaufnahme
        3: 'vorauffuehrung',  # Vorauffuhrung
        5: '',  # Publikumsgespräch
        6: '',  # Gastspiel
        11: '',  # öffentliche Probe
        17: 'deutsche-erstauffuehrung',  # Deutsche Erstauffuhrung
        21: '',  # Repertoire
        22: 'zum-letzten-mal',  # zum letzten Mal
        23: '',  # Urauffuhrung
        24: 'familienpreise',  # Familienvorstellung
        25: '',  # Kindervorstellung
        27: 'einfuehrung',  # Einfuhrung
        28: 'zum-letzten-mal-dieser-spielzeit',  # zum letzten Mal in dieser Spielzeit
        30: 'deutschsprachige-erstauffuehrung',  # Deutschsprachige Erstauffuhrung
        31: '',  # On Tour
        33: 'berliner-premiere',  # B-Premiere
        34: '',  # Matinee
        35: '',  # Schulervorstellung
        36: '',  # Volkstheater
    }

    ROLE_ID_MAPPER = {
        1: (u'Regie', u'Director'),
        4: (u'Dramaturgie', u'Dramaturgy'),
        6: (u'Ausstatter/-in', u'Designer'),
        8: (u'Sänger/-in', u'Singer'),
        9: (u'Schauspieler/-in', u'Actor'),
        10: (u'Solist/-in', u'Solist'),
        11: (u'Tänzer/-in', u'Dancer'),
        12: (u'Dirigent/-in', u'Director'),
        48: (u'Requisite', u'Requisite'),
        15: (u'Künstlerische Leitung', u'Artistic director'),
        17: (u'Buhnenbildner/-in', u'Scene designer'),
        18: (u'Kostüme', u'Costumes'),
        20: (u'Choreografie', u'Choreography'),
        21: (u'Licht', u'Light'),
        22: (u'Einstudierung', u'Production'),
        23: (u'Regieassistenz', u'Assistant director'),
        25: (u'Musik', u'Music'),
        46: (u'Text', u'Text'),
        29: (u'Video', u'Video'),
        30: (u'Pyrotechnik', u'Pyrotechnics'),
        33: (u'Souffleur/Souffleuse', u'Prompter'),
        34: (u'Künstler/-in', u'Performer'),
        47: (u'Inspizient/-in', u'Stage caller'),
        36: (u'Moderator/-in', u'Moderator'),
        37: (u'Referent/-in', u'Referent'),
        38: (u'Diskussionsteilnehmer/-in', u'Discussant'),
        39: (u'Rezitation', u'Recitation'),
        40: (u'Orchester', u'Orchestra'),
        41: (u'Chor', u'Choir'),
        43: (u'Statisterie', u'Extra'),
        45: (u'Ensemble', u'Ensemble'),
    }

    in_program_of = None
    owners = []
    DEFAULT_PUBLISHING_STATUS = "published"  # "import"

    def load_and_parse_locations(self):
        response = requests.get("http://web2.heimat.de/cb-out/exports/address/address_id.php?city=berlin")
        if response.status_code != 200:
            return
        reader = csv.reader(response.content.splitlines(), delimiter=";")
        reader.next()  # skip the first line
        for row in reader:
            self.LOCATIONS_BY_TITLE[row[1]] = CultureBaseLocation(*row)

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
        for child_node in node.findall('%(prefix)s%(tag)s' % dict(tag=tag, **self.helper_dict)):
            all_attributes_match = True
            for name, val in attrs.items():
                if child_node.get(name) != val:
                    all_attributes_match = False
                    break
            if all_attributes_match and child_node.text:
                return force_unicode(child_node.text)
        return u""

    def get_updated_location_and_stage(self, venue_node):
        """
        Creates or gets and updates location and stage
        :param venue_node: XML node with venue data
        :return: named tuple LocationAndStage(location, stage)
        """
        from collections import namedtuple
        from berlinbuehnen.apps.locations.models import Location, Stage
        city_suffix = re.compile(r' \[[^\]]+\]')
        LocationAndStage = namedtuple('LocationAndStage', ['location', 'stage'])

        venue_title = convert_location_title(self.get_child_text(venue_node, 'Name'))
        stage_settings = STAGE_TO_LOCATION_MAPPER.get(venue_title.lower(), None)
        if stage_settings:
            try:
                location = Location.objects.get(title_de=stage_settings.location_title)
            except Location.DoesNotExist:
                location = Location()
                location.title_de = location.title_en = stage_settings.location_title
        else:
            venue_to_save_at_production = PRODUCTION_VENUES.get(venue_title.lower(), '')
            if venue_to_save_at_production:
                return LocationAndStage(None, {
                    'title': venue_to_save_at_production,
                    'street_address': self.get_child_text(venue_node, 'Street'),
                    'postal_code': self.get_child_text(venue_node, 'ZipCode'),
                    'city': "Berlin",
                })
            try:
                location = Location.objects.get(title_de=venue_title)
            except Location.DoesNotExist:
                location = Location()
                location.title_de = location.title_en = venue_title

            if not location.street_address:
                lat = self.get_child_text(venue_node, 'Latitude')
                if lat:
                    location.latitude = float(lat)
                lng = self.get_child_text(venue_node, 'Longitude')
                if lng:
                    location.longitude = float(lng)
                location.street_address = self.get_child_text(venue_node, 'Street')
                location.postal_code = self.get_child_text(venue_node, 'ZipCode')
                location.city = city_suffix.sub('', self.get_child_text(venue_node, 'City') or "")

        location.save()

        if location == self.in_program_of:
            location = None

        stage = None
        if stage_settings:
            if stage_settings.should_create_stage_object:
                try:
                    stage = Stage.objects.get(location=location or self.in_program_of, title_de=stage_settings.internal_stage_title)
                except Stage.DoesNotExist:
                    stage = Stage()
                    stage.location = location or self.in_program_of
                    stage.title_de = stage.title_en = stage_settings.internal_stage_title

                if not stage.street_address:
                    lat = self.get_child_text(venue_node, 'Latitude')
                    if lat:
                        stage.latitude = float(lat)
                    lng = self.get_child_text(venue_node, 'Longitude')
                    if lng:
                        stage.longitude = float(lng)
                    stage.street_address = self.get_child_text(venue_node, 'Street')
                    stage.postal_code = self.get_child_text(venue_node, 'ZipCode')
                    stage.city = city_suffix.sub('', self.get_child_text(venue_node, 'City') or "")

                stage.save()
            else:
                return LocationAndStage(location, {
                    'title': stage_settings.internal_stage_title,
                    'street_address': self.get_child_text(venue_node, 'Street'),
                    'postal_code': self.get_child_text(venue_node, 'ZipCode'),
                    'city': "Berlin",
                })

        return LocationAndStage(location, stage)

    def get_updated_location_and_stage_from_free_text(self, free_text_venue):
        """
        Creates or gets and updates location and stage
        :param free_text_venue: venue title
        :return: named tuple LocationAndStage(location, stage) or LocationAndStage(location, stage_dict)
        where location is Location instance,
        stage is Stage instance,
        stage_dict is dict with details to save at production or event
        """
        from collections import namedtuple
        from berlinbuehnen.apps.locations.models import Location, Stage
        city_suffix = re.compile(r' \[[^\]]+\]')
        LocationAndStage = namedtuple('LocationAndStage', ['location', 'stage'])

        if free_text_venue.lower() in LOCATIONS_TO_SKIP:
            return LocationAndStage(None, None)

        venue_title = convert_location_title(free_text_venue)
        stage_settings = STAGE_TO_LOCATION_MAPPER.get(venue_title.lower(), None)
        if stage_settings:
            try:
                location = Location.objects.get(title_de=stage_settings.location_title)
            except Location.DoesNotExist:
                location = Location()
                location.title_de = location.title_en = stage_settings.location_title
        else:
            venue_to_save_at_production = PRODUCTION_VENUES.get(venue_title.lower(), '')
            if venue_to_save_at_production:
                stage_dict = {
                    'title': venue_title,
                }
                culturebase_location = self.LOCATIONS_BY_TITLE.get(venue_to_save_at_production, None)
                if culturebase_location:
                    stage_dict['street_address'] = culturebase_location.street_address
                    stage_dict['postal_code'] = culturebase_location.postal_code
                    stage_dict['city'] = u"Berlin"
                return LocationAndStage(None, stage_dict)
            try:
                location = Location.objects.get(title_de=venue_title)
            except Location.DoesNotExist:
                stage_dict = {
                    'title': venue_title,
                }
                culturebase_location = self.LOCATIONS_BY_TITLE.get(venue_title, None)
                if culturebase_location:
                    stage_dict['street_address'] = culturebase_location.street_address
                    stage_dict['postal_code'] = culturebase_location.postal_code
                    stage_dict['city'] = u"Berlin"
                return LocationAndStage(None, stage_dict)

            if location.street_address:
                culturebase_location = self.LOCATIONS_BY_TITLE.get(venue_title, None)
                if culturebase_location:
                    location.street_address = culturebase_location.street_address
                    location.postal_code = culturebase_location.postal_code
                    location.city = u"Berlin"

        location.save()

        if location == self.in_program_of:
            location = None

        stage = None
        if stage_settings:
            if stage_settings.should_create_stage_object:
                try:
                    stage = Stage.objects.get(location=location or self.in_program_of, title_de=stage_settings.internal_stage_title)
                except Stage.DoesNotExist:
                    stage = Stage()
                    stage.location = location or self.in_program_of
                    stage.title_de = stage.title_en = stage_settings.internal_stage_title

                if not stage.street_address:
                    culturebase_location = self.LOCATIONS_BY_TITLE.get(stage_settings.internal_stage_title, None)
                    if culturebase_location:
                        stage.street_address = culturebase_location.street_address
                        stage.postal_code = culturebase_location.postal_code
                        stage.city = u"Berlin"

                stage.save()
            else:
                stage_dict = {
                    'title': stage_settings.internal_stage_title,
                    'street_address': '',
                    'postal_code': '',
                    'city': 'Berlin',
                }
                culturebase_location = self.LOCATIONS_BY_TITLE.get(stage_settings.internal_stage_title, None)
                if culturebase_location:
                    stage_dict['street_address'] = culturebase_location.street_address
                    stage_dict['postal_code'] = culturebase_location.postal_code
                return LocationAndStage(location, stage_dict)

        return LocationAndStage(location, stage)

    def get_location_by_title(self, title):
        from berlinbuehnen.apps.locations.models import Location
        locations = Location.objects.filter(title_de=title)
        if locations:
            return locations[0]
        return None

    def cleanup_text(self, text):
        from django.utils.html import strip_tags
        text = text.replace('</div>', '\n')
        return strip_tags(text)

    def save_file_description(self, path, xml_node):
        from filebrowser.models import FileDescription
        try:
            file_description = FileDescription.objects.filter(
                file_path=path,
            ).order_by("pk")[0]
        except:
            file_description = FileDescription(file_path=path)

        file_description.title_de = self.get_child_text(xml_node, 'Title', Language="de")
        file_description.title_en = self.get_child_text(xml_node, 'Title', Language="en")
        # Description and Photographer go to the description field
        description_de_components = []
        description_en_components = []
        text = self.get_child_text(xml_node, 'Description', Language="de")
        if text:
            description_de_components.append(text)
        text = self.get_child_text(xml_node, 'Description', Language="en")
        if text:
            description_en_components.append(text)
        text = self.get_child_text(xml_node, 'Photographer')
        if text:
            description_de_components.append(text)
            description_en_components.append(text)
        file_description.description_de = "\n".join(description_de_components)
        file_description.description_en = "\n".join(description_en_components)
        # Copyright goes to the author field
        file_description.author = self.get_child_text(xml_node, 'Copyright')
        file_description.save()
        return file_description

    def parse_and_use_texts(self, xml_node, instance):
        description_de = description_en = u""
        teaser_de = teaser_en = u""
        pressetext_de = pressetext_en = u""
        kritik_de = kritik_en = u""
        werkinfo_kurz_de = werkinfo_kurz_en = u""
        werbezeile_de = werbezeile_en = u""
        werkinfo_gesamt_de = werkinfo_gesamt_en = u""
        hintergrundinformation_de = hintergrundinformation_en = u""
        inhaltsangabe_de = inhaltsangabe_en = u""
        programbuch_de = programbuch_en = u""
        for text_node in xml_node.findall('./%(prefix)sText' % self.helper_dict):
            text_cat_id = int(text_node.find('%(prefix)sCategory' % self.helper_dict).get('Id'))
            text_de = self.cleanup_text(self.get_child_text(text_node, 'Value', Language="de"))
            text_en = self.cleanup_text(self.get_child_text(text_node, 'Value', Language="en"))
            if text_cat_id == 14:  # Beschreibungstext kurz
                if text_de:
                    teaser_de = text_de
                if text_en:
                    teaser_en = text_en
            elif text_cat_id == 15:  # Beschreibungstext lang
                if text_de:
                    description_de = text_de
                if text_en:
                    description_en = text_en
            elif text_cat_id == 16:  # Inhaltsangabe
                if text_de:
                    inhaltsangabe_de = text_de
                if text_en:
                    inhaltsangabe_en = text_en
            elif text_cat_id == 17:  # Konzertprogramm
                if text_de:
                    instance.concert_program_de = text_de
                    instance.concert_program_de_markup_type = 'pt'
                if text_en:
                    instance.concert_program_en = text_en
                    instance.concert_program_en_markup_type = 'pt'
            elif text_cat_id == 18:  # Koproduktion
                if text_de:
                    instance.credits_de = text_de
                    instance.credits_de_markup_type = 'pt'
                if text_en:
                    instance.credits_en = text_en
                    instance.credits_en_markup_type = 'pt'
            elif text_cat_id == 19:  # Kritik
                if text_de:
                    kritik_de = text_de
                if text_en:
                    kritik_en = text_en
            elif text_cat_id == 20:  # Originaltitel
                if text_de:
                    instance.original_de = text_de
                if text_en:
                    instance.original_en = text_en
            elif text_cat_id == 21:  # Pressetext
                if text_de:
                    pressetext_de = text_de
                if text_en:
                    pressetext_de = text_en
            elif text_cat_id == 22:  # Rahmenprogramm zur Veranstaltung
                if text_de:
                    instance.supporting_program_de = text_de
                    instance.supporting_program_de_markup_type = 'pt'
                if text_en:
                    instance.supporting_program_en = text_en
                    instance.supporting_program_en_markup_type = 'pt'
            elif text_cat_id == 23:  # Sondermerkmal
                if text_de:
                    instance.remarks_de = text_de
                    instance.remarks_de_markup_type = 'pt'
                if text_en:
                    instance.remarks_en = text_en
                    instance.remarks_en_markup_type = 'pt'
            elif text_cat_id == 24:  # Spieldauer
                if text_de:
                    instance.duration_text_de = text_de
                if text_en:
                    instance.duration_text_en = text_en
            elif text_cat_id == 25:  # Übertitel
                if text_de:
                    instance.subtitles_text_de = text_de
                if text_en:
                    instance.subtitles_text_en = text_en
            elif text_cat_id == 26:  # Werbezeile
                if text_de:
                    werbezeile_de = text_de
                if text_en:
                    werbezeile_en = text_en
            elif text_cat_id == 27:  # Werkinfo gesamt
                if text_de:
                    werkinfo_gesamt_de = text_de
                if text_en:
                    werkinfo_gesamt_en = text_en
            elif text_cat_id == 28:  # Werkinfo kurz
                if text_de:
                    werkinfo_kurz_de = text_de
                if text_en:
                    werkinfo_kurz_en = text_en
            elif text_cat_id == 29:  # zusätzliche Preisinformationen
                if text_de:
                    instance.price_information_de = text_de
                    instance.price_information_de_markup_type = 'pt'
                if text_en:
                    instance.price_information_en = text_en
                    instance.price_information_en_markup_type = 'pt'
            elif text_cat_id == 30:  # Titelprefix
                if text_de:
                    instance.prefix_de = text_de
                if text_en:
                    instance.prefix_en = text_en
            elif text_cat_id == 35:  # Programmbuch
                if text_de:
                    programbuch_de = text_de
                if text_en:
                    programbuch_en = text_en
            elif text_cat_id == 36:  # Hintergrundinformation
                if text_de:
                    hintergrundinformation_de = text_de
                if text_en:
                    hintergrundinformation_en = text_en
            elif text_cat_id == 39:  # Altersangabe
                if text_de:
                    instance.age_text_de = text_de
                if text_en:
                    instance.age_text_en = text_en
            elif text_cat_id == 40:  # Audio & Video
                pass

        if pressetext_de or kritik_de:
            instance.press_text_de = u"\n".join([text for text in (pressetext_de, kritik_de) if text])
            instance.press_text_de_markup_type = 'pt'
        if pressetext_en or kritik_en:
            instance.press_text_en = u"\n".join([text for text in (pressetext_en, kritik_en) if text])
            instance.press_text_en_markup_type = 'pt'

        if inhaltsangabe_de or programbuch_de:
            instance.contents_de = u"\n".join([text for text in (inhaltsangabe_de, programbuch_de) if text])
            instance.contents_de_markup_type = 'pt'
        if inhaltsangabe_en or programbuch_en:
            instance.contents_en = u"\n".join([text for text in (inhaltsangabe_en, programbuch_en) if text])
            instance.contents_en_markup_type = 'pt'

        # according to Bjorn's request:
        if werbezeile_de:
            instance.teaser_de = werbezeile_de
        elif werkinfo_kurz_de:
            instance.teaser_de = werkinfo_kurz_de
            werkinfo_kurz_de = u""
        instance.teaser_de_markup_type = 'pt'

        if werbezeile_en:
            instance.teaser_en = werbezeile_en
        elif werkinfo_kurz_en:
            instance.teaser_en = werkinfo_kurz_en
            werkinfo_kurz_en = u""
        instance.teaser_en_markup_type = 'pt'

        if teaser_de or description_de:
            instance.description_de = u"\n".join([text for text in (teaser_de, description_de) if text])
        elif werkinfo_kurz_de:
            instance.description_de = werkinfo_kurz_de
            werkinfo_kurz_de = u""
        elif werkinfo_gesamt_de:
            instance.description_de = werkinfo_gesamt_de
            werkinfo_gesamt_de = u""
        instance.description_de_markup_type = 'pt'

        if teaser_en or description_en:
            instance.description_en = u"\n".join([text for text in (teaser_en, description_en) if text])
        elif werkinfo_kurz_en:
            instance.description_en = werkinfo_kurz_en
            werkinfo_kurz_en = u""
        elif werkinfo_gesamt_en:
            instance.description_en = werkinfo_gesamt_en
            werkinfo_gesamt_en = u""
        instance.description_en_markup_type = 'pt'
        
        instance.work_info_de = u"\n".join([text for text in (werkinfo_kurz_de, werkinfo_gesamt_de, hintergrundinformation_de) if text])
        instance.work_info_de_markup_type = 'pt'

        instance.work_info_en = u"\n".join([text for text in (werkinfo_kurz_en, werkinfo_gesamt_en, hintergrundinformation_en) if text])
        instance.work_info_en_markup_type = 'pt'

        # additional from 2015-04-07

        if not instance.description_de and instance.press_text_de:
            instance.description_de = instance.press_text_de
            instance.press_text_de = u""

        if not instance.description_en and instance.press_text_en:
            instance.description_en = instance.press_text_en
            instance.press_text_en = u""

    def save_page(self, root_node):
        import time
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        image_mods = models.get_app("image_mods")

        prod_nodes = root_node.findall('%(prefix)sProduction' % self.helper_dict)
        prods_count = len(prod_nodes)

        for prod_index, prod_node in enumerate(prod_nodes, 1):
            external_prod_id = prod_node.get('Id')

            title_de = self.get_child_text(prod_node, 'Title', Language="de").replace('\n', ' ').strip()
            title_en = self.get_child_text(prod_node, 'Title', Language="en").replace('\n', ' ').strip()
            if self.verbosity >= NORMAL:
                self.stdout.write(u"%d/%d %s | %s" % (prod_index, prods_count, title_de, title_en))

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
                if not prod or prod.status == "trashed":
                    # if production was deleted after import,
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

            prod.status = self.DEFAULT_PUBLISHING_STATUS
            prod.title_de = title_de
            prod.title_en = title_en or title_de
            prod.website_de = prod.website_en = self.get_child_text(prod_node, 'Url')

            prod.slug = get_unique_value(Production, better_slugify(prod.title_de)[:200] or u"production", instance_pk=prod.pk)

            ticket_node = prod_node.find('./%(prefix)sTicket' % self.helper_dict)
            if ticket_node is not None:
                prices = self.get_child_text(ticket_node, 'Price')
                if prices:
                    prod.price_from, prod.price_till = prices.split(u' - ')
                prod.tickets_website = self.get_child_text(ticket_node, 'TicketLink')

            self.parse_and_use_texts(prod_node, prod)
            
            prod.save()

            venue_node = prod_node.find('./%(prefix)sVenue' % self.helper_dict)
            if venue_node is not None:
                location, stage = self.get_updated_location_and_stage(venue_node)
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
                location, stage = self.get_updated_location_and_stage_from_free_text(free_text_venue)
                if location:
                    prod.play_locations.clear()
                    prod.play_locations.add(location)
                #else:
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
            for organisation_node in prod_node.findall('./%(prefix)sOrganisation' % self.helper_dict):
                organizers_list.append(self.get_child_text(organisation_node, 'Name'))

            if organizers_list:
                prod.organizers = u', '.join(organizers_list)
                prod.save()

            if not self.skip_images:
                image_ids_to_keep = []
                for picture_node in prod_node.findall('./%(prefix)sPicture' % self.helper_dict):
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
                        # or create a new exhibition and then create a mapper
                        mf = ProductionImage(production=prod)
                    else:
                        mf = image_mapper.content_object
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
                        if self.get_child_text(picture_node, 'PublishType') == "publish_type_for_free_use":
                            mf.copyright_restrictions = "general_use"
                        else:
                            mf.copyright_restrictions = "protected"
                        mf.save()
                        image_ids_to_keep.append(mf.pk)

                        file_description = self.save_file_description(mf.path, picture_node)

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
            for category_id_node in prod_node.findall('./%(prefix)sContentCategory/%(prefix)sCategoryId' % self.helper_dict):
                internal_cat_id = self.CATEGORY_MAPPER.get(int(category_id_node.text), None)
                if internal_cat_id:
                    cats = ProductionCategory.objects.filter(pk=internal_cat_id)
                    if cats:
                        prod.categories.add(cats[0])
                        if cats[0].parent:
                            prod.categories.add(cats[0].parent)

            prod.characteristics.clear()
            for status_node in prod_node.findall('./%(prefix)sStatus' % self.helper_dict):
                internal_ch_slug = self.PRODUCTION_CHARACTERISTICS_MAPPER.get(int(status_node.get('Id')), None)
                if internal_ch_slug:
                    prod.characteristics.add(ProductionCharacteristics.objects.get(slug=internal_ch_slug))
                elif int(status_node.get('Id')) == 25:
                    prod.categories.add(ProductionCategory.objects.get(slug="kinder-jugend"))

            prod.productionleadership_set.all().delete()
            prod.productionauthorship_set.all().delete()
            prod.productioninvolvement_set.all().delete()
            for person_node in prod_node.findall('./%(prefix)sPerson' % self.helper_dict):
                first_and_last_name = self.get_child_text(person_node, 'Name')
                if u" " in first_and_last_name:
                    first_name, last_name = first_and_last_name.rsplit(" ", 1)
                else:
                    first_name = ""
                    last_name = first_and_last_name
                role_de = self.get_child_text(person_node, 'RoleDescription', Language="de")
                role_en = self.get_child_text(person_node, 'RoleDescription', Language="en")
                if not role_de and person_node.find('%(prefix)sCategory' % self.helper_dict) is not None:
                    role_de, role_en = self.ROLE_ID_MAPPER[int(person_node.find('%(prefix)sCategory' % self.helper_dict).get("Id"))]

                if role_de in self.authorship_types_de:
                    authorship_type = AuthorshipType.objects.get(title_de=role_de)
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
            for sort_order, item in enumerate(prod.productionauthorship_set.order_by('imported_sort_order'), 0):
                item.sort_order = sort_order
                item.save()
            for sort_order, item in enumerate(prod.productionleadership_set.order_by('imported_sort_order'), 0):
                item.sort_order = sort_order
                item.save()
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
            for sponsor_node in prod_node.findall('./%(prefix)sSponsor' % self.helper_dict):
                sponsor = ProductionSponsor(production=prod)
                sponsor.title_de = self.get_child_text(sponsor_node, 'Description', Language="de")
                sponsor.title_en = self.get_child_text(sponsor_node, 'Description', Language="en")
                sponsor.website = self.get_child_text(sponsor_node, 'Url')
                sponsor.save()
                image_url = self.get_child_text(sponsor_node, 'ImageUrl')
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

                self.parse_and_use_texts(event_node, event)

                organisation_node = event_node.find('./%(prefix)sOrganisation' % self.helper_dict)
                if organisation_node:
                    event.organizers = self.get_child_text(organisation_node, 'Name')

                event.save()

                if not self.skip_images:
                    image_ids_to_keep = []
                    for picture_node in event_node.findall('%(prefix)sPicture' % self.helper_dict):
                        image_url = self.get_child_text(picture_node, 'Url')

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
                            if self.get_child_text(picture_node, 'PublishType') == "publish_type_for_free_use":
                                mf.copyright_restrictions = "general_use"
                            else:
                                mf.copyright_restrictions = "protected"
                            mf.save()
                            image_ids_to_keep.append(mf.pk)

                            file_description = self.save_file_description(mf.path, picture_node)

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

                venue_node = event_node.find('%(prefix)sVenue' % self.helper_dict)
                if venue_node is not None:
                    location, stage = self.get_updated_location_and_stage(venue_node)
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
                free_text_venue = self.get_child_text(prod_node, 'FreeTextVenue')
                if free_text_venue:
                    location, stage = self.get_updated_location_and_stage_from_free_text(free_text_venue)
                    if location:
                        event.play_locations.clear()
                        event.play_locations.add(location)
                    #else:
                    #    event.location_title = free_text_venue
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
                for status_node in event_node.findall('%(prefix)sStatus' % self.helper_dict):
                    internal_ch_slug = self.EVENT_CHARACTERISTICS_MAPPER.get(int(status_node.get('Id')), None)
                    if internal_ch_slug:
                        event.characteristics.add(EventCharacteristics.objects.get(slug=internal_ch_slug))

                event.eventauthorship_set.all().delete()
                event.eventleadership_set.all().delete()
                event.eventinvolvement_set.all().delete()
                for person_node in event_node.findall('%(prefix)sPerson' % self.helper_dict):
                    first_and_last_name = self.get_child_text(person_node, 'Name')
                    if u" " in first_and_last_name:
                        first_name, last_name = first_and_last_name.rsplit(" ", 1)
                    else:
                        first_name = ""
                        last_name = first_and_last_name
                    role_de = self.get_child_text(person_node, 'RoleDescription', Language="de")
                    role_en = self.get_child_text(person_node, 'RoleDescription', Language="en")
                    if not role_de and person_node.find('%(prefix)sCategory' % self.helper_dict) is not None:
                        role_de, role_en = self.ROLE_ID_MAPPER[int(person_node.find('%(prefix)sCategory' % self.helper_dict).get("Id"))]

                    if role_de in self.authorship_types_de:
                        authorship_type = AuthorshipType.objects.get(title_de=role_de)
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
                for sort_order, item in enumerate(event.eventauthorship_set.order_by('imported_sort_order'), 0):
                    item.sort_order = sort_order
                    item.save()
                for sort_order, item in enumerate(event.eventleadership_set.order_by('imported_sort_order'), 0):
                    item.sort_order = sort_order
                    item.save()
                for sort_order, item in enumerate(event.eventinvolvement_set.order_by('imported_sort_order'), 0):
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
