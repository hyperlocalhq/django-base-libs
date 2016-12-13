# -*- coding: UTF-8 -*-

import os
import shutil
import re
from dateutil.parser import parse as parse_datetime
import requests
import csv
from collections import namedtuple
from decimal import Decimal, InvalidOperation

from django.db import models
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode

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


StageSettings = namedtuple('StageSettings', ['location_title', 'internal_stage_title', 'should_create_stage_object'])

LOCATION_TITLE_MAPPER = dict((k.lower(), v) for k, v in {
    u"English Theatre Berlin | International Performing Arts Center": u"English Theatre Berlin",
    u"Wühlmäuse": u"Die Wühlmäuse",  # where does it happen?
    u"SCHAUBUDE BERLIN - Theater.PuppenFigurenObjekte": u"SCHAUBUDE BERLIN",
    u"Staatsoper im Schillertheater": u"Staatsoper im Schiller Theater",  # where does it happen?
    u"ATZE  Musiktheater": u"ATZE Musiktheater",
    u"Astrid Lindgren Bühne im FEZ Berlin": u"Astrid Lindgren Bühne im FEZ-Berlin",
    u"FEZ-Berlin und Landesmusikakademie Berlin": u"Landesmusikakademie Berlin im FEZ",
    u"UdK - Universität der Künste Berlin": u"UNI.T - Theater der UdK Berlin",
    u"Sophiensaele": u"Sophiensæle",
}.iteritems())


def convert_location_title(title):
    return LOCATION_TITLE_MAPPER.get(title.lower(), title)

LOCATIONS_TO_SKIP = [el.lower() for el in [
    u"-",
]]


PRODUCTION_VENUES = dict((k.lower(), v) for k, v in {
    u"Rotes Rathaus": u"Rotes Rathaus",
    u"Babylon Berlin-Mitte": u"Babylon Berlin-Mitte",
    u"Delphi Filmpalast": u"Delphi Filmpalast",
    u"Waldbühne Berlin": u"Waldbühne Berlin",
}.iteritems())


STAGE_TO_LOCATION_MAPPER = dict((k.lower(), v) for k, v in {
    u"Große Orangerie Schloss Charlottenburg": StageSettings(u"Berliner Residenz Konzerte", u"Große Orangerie Schloss Charlottenburg", True),
    u"Große Orangerie Charlottenburg": StageSettings(u"Berliner Residenz Konzerte", u"Große Orangerie Schloss Charlottenburg", True),

    u"Deutsches Theater - Box und Bar": StageSettings(u"Deutsches Theater Berlin", u"Box und Bar", True),
    u"Deutsches Theater - Saal": StageSettings(u"Deutsches Theater Berlin", u"Saal", True),
    u"Deutsches Theater Berlin - Kammerspiele": StageSettings(u"Deutsches Theater Berlin", u"Kammerspiele", True),

    u"DISTEL-Studio": StageSettings(u"Distel Kabarett-Theater", u"DISTEL-Studio", True),

    u"Foyer Deutschen Oper Berlin": StageSettings(u"Deutsche Oper Berlin", u"Foyer", True),
    u"Restaurant Deutsche Oper": StageSettings(u"Deutsche Oper Berlin", u"Restaurant", True),
    u"Tischlerei Deutsche Oper Berlin": StageSettings(u"Deutsche Oper Berlin", u"Tischlerei Deutsche Oper Berlin", True),

    u"Freilichtbühne an der Zitadelle Spandau": StageSettings(u"Berliner Kindertheater", u"Freilichtbühne an der Zitadelle Spandau", False),

    u"GRIPS Hansaplatz": StageSettings(u"GRIPS Theater", u"GRIPS Hansaplatz", True),
    u"GRIPS Podewil": StageSettings(u"GRIPS Theater", u"GRIPS Podewil", True),

    u"Hebbel am Ufer - HAU1": StageSettings(u"HAU Hebbel am Ufer", u"HAU1", True),
    u"Hebbel am Ufer - HAU2": StageSettings(u"HAU Hebbel am Ufer", u"HAU2", True),
    u"Hebbel am Ufer - HAU3": StageSettings(u"HAU Hebbel am Ufer", u"HAU3", True),
    u"WAU im HAU2":  StageSettings(u"HAU Hebbel am Ufer", u"WAU im HAU2", True),
    u"HAU2 Installation":  StageSettings(u"HAU Hebbel am Ufer", u"HAU2 Installation", True),
    u"HAU1+2":  StageSettings(u"HAU Hebbel am Ufer", u"HAU1+2", True),
    u"HAU 1 in the Upper Foyer":  StageSettings(u"HAU Hebbel am Ufer", u"HAU 1 in the Upper Foyer", True),
    u"HAU2 Foyer":  StageSettings(u"HAU Hebbel am Ufer", u"HAU2 Foyer", True),
    u"HAU1 Installation":  StageSettings(u"HAU Hebbel am Ufer", u"HAU1 Installation", True),
    u"HAU3 Houseclub":  StageSettings(u"HAU Hebbel am Ufer", u"HAU3 Houseclub", True),
    u"HAU2 Outdoors":  StageSettings(u"HAU Hebbel am Ufer", u"HAU2 Outdoors", True),
    u"Privatwohnungen in Berlin":  StageSettings(u"HAU Hebbel am Ufer", u"Privatwohnungen in Berlin", True),
    u"Relexa Hotel":  StageSettings(u"HAU Hebbel am Ufer", u"Relexa Hotel", True),

    u"Haus der Berliner Festspiele": StageSettings(u"Berliner Festspiele", u"Haus der Berliner Festspiele", True),
    u"Martin-Gropius-Bau": StageSettings(u"Berliner Festspiele", u"Martin-Gropius-Bau", True),

    u"Volksbühne am Rosa-Luxemburg-Platz / 3. Stock": StageSettings(u"Volksbühne am Rosa-Luxemburg-Platz", u"3. Stock", True),
    u"Volksbühne am Rosa-Luxemburg-Platz / Books": StageSettings(u"Volksbühne am Rosa-Luxemburg-Platz", u"Books", True),
    u"Volksbühne am Rosa-Luxemburg-Platz / Grüner Salon": StageSettings(u"Volksbühne am Rosa-Luxemburg-Platz", u"Grüner Salon", True),
    u"Volksbühne am Rosa-Luxemburg-Platz / Roter Salon": StageSettings(u"Volksbühne am Rosa-Luxemburg-Platz", u"Roter Salon", True),
    u"Volksbühne am Rosa-Luxemburg-Platz / Sternfoyer": StageSettings(u"Volksbühne am Rosa-Luxemburg-Platz", u"Sternfoyer", True),

    u"Admiralspalast 101": StageSettings(u"Admiralspalast", u"F101", True),
    u"Admiralspalast Studio": StageSettings(u"Admiralspalast", u"Studio", True),
    u"Admiralspalast Theater": StageSettings(u"Admiralspalast", u"Theater", True),

    u"Berliner Ensemble/ Foyer": StageSettings(u"Berliner Ensemble", u"Foyer", True),
    u"Berliner Ensemble/ Pavillon": StageSettings(u"Berliner Ensemble", u"Pavillon", True),
    u"Berliner Ensemble/ Probebühne": StageSettings(u"Berliner Ensemble", u"Probebühne", True),
    u"Berliner Ensemble/ Treffpunkt Kassenhalle": StageSettings(u"Berliner Ensemble", u"Treffpunkt Kassenhalle", True),

    u"Berliner Philharmonie – Kammermusiksaal": StageSettings(u"Berliner Philharmonie", u"Kammermusiksaal", True),
    u"Foyer im Kammermusiksaal der Berliner Philharmoniker": StageSettings(u"Berliner Philharmonie", u"Foyer im Kammermusiksaal", True),
    u"Philharmonie Berlin - Großer Saal": StageSettings(u"Berliner Philharmonie", u"Großer Saal", True),
    u"München, Philharmonie im Gasteig": StageSettings(u"Berliner Philharmonie", u"München, Philharmonie im Gasteig", True),
    u"Philharmonie – Karl-Schuke-Orgel": StageSettings(u"Berliner Philharmonie", u"Philharmonie – Karl-Schuke-Orgel", True),
    u"Hermann-Wolff-Saal": StageSettings(u"Berliner Philharmonie", u"Hermann-Wolff-Saal", True),
    u"Mailand, Expo - La Scala": StageSettings(u"Berliner Philharmonie", u"Mailand, Expo - La Scala", True),
    u"Wien, Musikverein": StageSettings(u"Berliner Philharmonie", u"Wien, Musikverein", True),
    u"Philharmonie und Kammermusiksaal": StageSettings(u"Berliner Philharmonie", u"Philharmonie und Kammermusiksaal", True),

	u"Konzerthaus Berlin - Großer Saal": StageSettings(u"Konzerthaus Berlin", u"Großer Saal", True),
	u"Konzerthaus Berlin - Kleiner Saal": StageSettings(u"Konzerthaus Berlin", u"Kleiner Saal", True),
	u"Konzerthaus Berlin - Ludwig-van-Beethoven-Saal": StageSettings(u"Konzerthaus Berlin", u"Ludwig-van-Beethoven-Saal", True),
	u"Konzerthaus Berlin - Musikclub": StageSettings(u"Konzerthaus Berlin", u"Musikclub", True),
	u"Konzerthaus Berlin - Werner-Otto-Saal": StageSettings(u"Konzerthaus Berlin", u"Werner-Otto-Saal", True),

    u"Renaissance-Theater Berlin - Bruckner-Foyer": StageSettings(u"Renaissance-Theater Berlin", u"Bruckner-Foyer", True),

    u"Sophiensaele - Festsaal": StageSettings(u"Sophiensæle", u"Festsaal", True),
	u"Sophiensaele - Hochzeitssaal": StageSettings(u"Sophiensæle", u"Hochzeitssaal", True),
	u"Kantine": StageSettings(u"Sophiensæle", u"Kantine", True),
	u"gesamtes Haus": StageSettings(u"Sophiensæle", u"gesamtes Haus", True),
	u"Sophiensaele - Kantine": StageSettings(u"Sophiensæle", u"Kantine", True),

    u"Bode-Museum": StageSettings(u"Staatsoper im Schiller Theater", u"Bode Museum", True),
	u"Staatsoper im Schiller Theater - Gläsernes Foyer": StageSettings(u"Staatsoper im Schiller Theater", u"Gläsernes Foyer", True),
	u"Staatsoper im Schiller Theater - Werkstatt": StageSettings(u"Staatsoper im Schiller Theater", u"Werkstatt", True),
	u"Staatsoper Unter den Linden": StageSettings(u"Staatsoper im Schiller Theater", u"Staatsoper Unter den Linden", True),
    u"Staatsoper im Schiller Theater - Probebühne I": StageSettings(u"Staatsoper im Schiller Theater", u"Probebühne I", True),
    u"Bebelplatz": StageSettings(u"Staatsoper im Schiller Theater", u"Bebelplatz", True),

    u"Theater an der Parkaue - Bühne 2": StageSettings(u"Theater an der Parkaue", u"Bühne 2", True),

    u"Alten Feuerwache Eichwalde": StageSettings(u"Neuköllner Oper", u"Alten Feuerwache Eichwalde", True),

    u"Gorki Foyer Berlin": StageSettings(u"Maxim Gorki Theater", u"Foyer", True),
	u"Gorki Studio R": StageSettings(u"Maxim Gorki Theater", u"Studio Я", True),
	u"Studio Я": StageSettings(u"Maxim Gorki Theater", u"Studio Я", True),
	u"Vorplatz GORKI": StageSettings(u"Maxim Gorki Theater", u"Vorplatz GORKI", True),
	u"Maxim Gorki Theater": StageSettings(u"Maxim Gorki Theater", u"Gorki Theater", True),

    u"Tempodrom": StageSettings(u"Die Wühlmäuse", u"Tempodrom", False),
}.iteritems())


class CultureBaseLocation(object):
    def __init__(self, id, title, street_address, postal_code, city, *args, **kwargs):
        self.id = id
        self.title = force_unicode(title)
        self.street_address = force_unicode(street_address)
        self.postal_code = force_unicode(postal_code)
        self.city = force_unicode(city)

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return smart_str(u"<CultureBaseLocation: %s>" % self.title)


class ImportFromHeimatBase(object):
    """ Base interface for importing productions and events from different websites
    according to this XML schema: http://cb.heimat.de/interface/schema/interfaceformat.xsd
    """
    LOCATIONS_BY_EXTERNAL_ID = {}
    LOCATIONS_BY_TITLE = {}
    service = None
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
        6998: 17,  # Konzertante Vorstellung -> Konzertante Aufführung
        7020: 15,  # Lesung
        7000: 44,  # Liederabend
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
        7023: 5,  # Sonstige Musik -> Konzert
        6989: 48,  # Soul
        7011: 81,  # Special
        6997: 27,  # Tanztheater
        7027: 54,  # Variete
        7021: 73,  # Vortrag
        7004: 82,  # Workshop
    }
    PRODUCTION_CHARACTERISTICS_MAPPER = {
        1: '',  # Premiere
        2: 'wiederaufname',  # Wiederaufnahme
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
        27: '',  # Einfuhrung
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
    IMPORT_URL = None
    DEFAULT_PUBLISHING_STATUS = "published"  # "import"
    production_ids_to_keep = set()
    event_ids_to_keep = set()

    def load_and_parse_locations(self):
        response = requests.get("http://web2.heimat.de/cb-out/exports/address/address_id.php?city=berlin")
        if response.status_code != 200:
            return
        reader = csv.reader(response.content.splitlines(), delimiter=";")
        reader.next()  # skip the first line
        for row in reader:
            self.LOCATIONS_BY_EXTERNAL_ID[row[0]] = CultureBaseLocation(*row)
            self.LOCATIONS_BY_TITLE[row[1]] = CultureBaseLocation(*row)

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

    def get_updated_location_and_stage(self, venue_node):
        """
        Creates or gets and updates location and stage
        :param venue_node: XML node with venue data
        :return: named tuple LocationAndStage(location, stage)
        """
        from collections import namedtuple
        from berlinbuehnen.apps.locations.models import Location, Stage
        LocationAndStage = namedtuple('LocationAndStage', ['location', 'stage'])

        if not self.LOCATIONS_BY_EXTERNAL_ID:
            self.load_and_parse_locations()

        if venue_node.get('isId') == "1":
            external_id = venue_node.text
        else:  # unknown location id
            if not venue_node.text:
                return LocationAndStage(None, None)
            # return location and stage by title
            return self.get_updated_location_and_stage_from_free_text(venue_node.text)

        if external_id not in self.LOCATIONS_BY_EXTERNAL_ID:  # location not found in Berlin
            return LocationAndStage(None, None)

        culturebase_location = self.LOCATIONS_BY_EXTERNAL_ID[external_id]

        stage_settings = STAGE_TO_LOCATION_MAPPER.get(culturebase_location.title.lower(), None)
        if stage_settings:
            try:
                location = Location.objects.get(title_de=stage_settings.location_title)
            except Location.DoesNotExist:
                location = Location()
                location.title_de = location.title_en = stage_settings.location_title
        else:
            venue_to_save_at_production = PRODUCTION_VENUES.get(culturebase_location.title.lower(), '')
            if venue_to_save_at_production:
                stage_dict = {
                    'title': venue_to_save_at_production,
                }
                culturebase_location = self.LOCATIONS_BY_TITLE.get(venue_to_save_at_production, None)
                if culturebase_location:
                    stage_dict['street_address'] = culturebase_location.street_address
                    stage_dict['postal_code'] = culturebase_location.postal_code
                    stage_dict['city'] = u"Berlin"
                return LocationAndStage(None, stage_dict)
            try:
                location = Location.objects.get(title_de=convert_location_title(culturebase_location.title))
            except Location.DoesNotExist:
                location = Location()
                location.title_de = location.title_en = convert_location_title(culturebase_location.title)

            if not location.street_address:
                location.street_address = culturebase_location.street_address
                location.postal_code = culturebase_location.postal_code
                location.city = "Berlin"

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
                    stage.street_address = culturebase_location.street_address
                    stage.postal_code = culturebase_location.postal_code
                    stage.city = "Berlin"

                stage.save()
            else:
                return LocationAndStage(location, {
                    'title': stage_settings.internal_stage_title,
                    'street_address': culturebase_location.street_address,
                    'postal_code': culturebase_location.postal_code,
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
                    'title': venue_to_save_at_production,
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

            if not location.street_address:
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

    def cleanup_text(self, text):
        import re
        from BeautifulSoup import BeautifulStoneSoup
        from django.utils.html import strip_tags
        text = text.replace('<![CDATA[', '')
        text = text.replace(']]>', '')
        text = text.replace('</div>', '\n')
        text = strip_tags(text).strip()
        text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
        return text

    def save_file_description(self, path, xml_node):
        from filebrowser.models import FileDescription
        try:
            file_description = FileDescription.objects.filter(
                file_path=path,
            ).order_by("pk")[0]
        except:
            file_description = FileDescription(file_path=path)

        file_description.title_de = self.get_child_text(xml_node, 'title', languageId="1") or self.get_child_text(
            xml_node, 'text', languageId="1")
        file_description.title_en = self.get_child_text(xml_node, 'title', languageId="2") or self.get_child_text(
            xml_node, 'text', languageId="2")
        text = (xml_node.get('photographer') or u"").replace("Foto: ", "")
        if text:
            file_description.description_de = text
            file_description.description_en = text
        file_description.author = xml_node.get('copyright')
        file_description.copyright_limitations = ""
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
        for text_node in xml_node.findall('./mediaText'):
            text_cat_id = int(text_node.get('relation'))
            text_de = self.cleanup_text(self.get_child_text(text_node, 'text', languageId="1"))
            text_en = self.cleanup_text(self.get_child_text(text_node, 'text', languageId="2"))
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
            elif text_cat_id == 25:  # Übertitel - this is a subtitle, not subtitles
                if text_de:
                    instance.subtitles_text_de = ""
                    instance.subtitle_de = text_de
                if text_en:
                    instance.subtitles_text_en = ""
                    instance.subtitle_en = text_en
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

        # exception for the Schaubuehne and alike
        if not instance.subtitles_text_de:
            instance.subtitles_text_de = self.get_child_text(xml_node, 'language_and_subtitles')
        if not instance.subtitles_text_en:
            instance.subtitles_text_en = self.get_child_text(xml_node, 'language_and_subtitles')

    def save_page(self, root_node):
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        image_mods = models.get_app("image_mods")

        prod_nodes = root_node.findall('production')
        prods_count = len(prod_nodes)

        for prod_index, prod_node in enumerate(prod_nodes, 1):
            external_prod_id = prod_node.get('foreignId')

            title_de = self.get_child_text(prod_node, 'title', languageId="1").replace('\n', ' ').strip()
            title_en = self.get_child_text(prod_node, 'title', languageId="2").replace('\n', ' ').strip()

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

            prod.slug = get_unique_value(Production, better_slugify(prod.title_de)[:200] or u"production", instance_pk=prod.pk)

            self.parse_and_use_texts(prod_node, prod)

            prod.save()
            self.production_ids_to_keep.add(prod.pk)

            venue_node = prod_node.find('location')
            if venue_node is not None:
                location, stage = self.get_updated_location_and_stage(venue_node)
                if location:
                    prod.play_locations.clear()
                    prod.play_locations.add(location)
                #else:
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

    def should_reimport(self, service):
        from dateutil.parser import parse

        # read the last-modified header from the feed
        response = requests.head(self.IMPORT_URL)
        last_modified_str = response.headers.get('last-modified', '')
        if not last_modified_str:
            return False
        feed_last_modified = parse(last_modified_str)

        # compare feed_last_modified with the last updated production creation date
        mappers = service.objectmapper_set.filter(content_type__model__iexact="production").order_by('-pk')
        if mappers:
            productions_last_modified = mappers[0].content_object.creation_date
            return feed_last_modified > productions_last_modified
        return True

    def delete_existing_productions_and_events(self, service):
        if self.verbosity >= NORMAL:
            self.stdout.write(u"=== Deleting existing productions ===")

        # deleting productions and their mappers
        prods_count = service.objectmapper_set.filter(content_type__model__iexact="production").count()
        for prod_index, mapper in enumerate(service.objectmapper_set.filter(content_type__model__iexact="production"), 1):
            if mapper.content_object:
                if self.verbosity >= NORMAL:
                    self.stdout.write(u"%d/%d %s | %s" % (prod_index, prods_count, mapper.content_object.title_de, mapper.content_object.title_en))
                if mapper.content_object.no_overwriting:  # don't delete items with no_overwriting == True
                    continue

                # delete media files
                try:
                    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, "productions", mapper.content_object.slug))
                except OSError as err:
                    pass

                mapper.content_object.delete()
            mapper.delete()

        # deleting events and their mappers
        for mapper in service.objectmapper_set.filter(content_type__model__iexact="event"):
            if mapper.content_object:
                if mapper.content_object.production.no_overwriting:  # don't delete items with no_overwriting == True
                    continue

                mapper.content_object.delete()
            mapper.delete()

        # deleting production images and their mappers if a production was deleted
        for mapper in service.objectmapper_set.filter(content_type__model__iexact="productionimage"):
            if mapper.content_object:
                continue
            mapper.delete()

        # deleting event images and their mappers if an event was deleted
        for mapper in service.objectmapper_set.filter(content_type__model__iexact="eventimage"):
            if mapper.content_object:
                continue
            mapper.delete()


    def delete_outdated_productions_and_events(self, service):
        if self.verbosity >= NORMAL:
            self.stdout.write(u"=== Deleting outdated productions ===")

        # deleting productions and their mappers
        prods_count = service.objectmapper_set.filter(
            content_type__model__iexact="production"
        ).exclude(
            object_id__in=self.production_ids_to_keep
        ).count()

        for prod_index, mapper in enumerate(service.objectmapper_set.filter(
            content_type__model__iexact="production"
        ).exclude(
            object_id__in=self.production_ids_to_keep
        ), 1):
            if mapper.content_object:
                if self.verbosity >= NORMAL:
                    self.stdout.write(u"%d/%d %s | %s" % (prod_index, prods_count, mapper.content_object.title_de, mapper.content_object.title_en))
                if mapper.content_object.no_overwriting:  # don't delete items with no_overwriting == True
                    continue

                # delete media files
                try:
                    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, "productions", mapper.content_object.slug))
                except OSError as err:
                    pass

                mapper.content_object.delete()
            mapper.delete()
            self.stats.setdefault('prods_deleted', 0)
            self.stats['prods_deleted'] += 1

        # deleting events and their mappers
        for mapper in service.objectmapper_set.filter(content_type__model__iexact="event").exclude(
            object_id__in=self.event_ids_to_keep
        ):
            if mapper.content_object:
                if mapper.content_object.production.no_overwriting:  # don't delete items with no_overwriting == True
                    continue

                mapper.content_object.delete()
            mapper.delete()
            self.stats.setdefault('events_deleted', 0)
            self.stats['events_deleted'] += 1

        # deleting production image mappers if a production was deleted
        for mapper in service.objectmapper_set.filter(content_type__model__iexact="productionimage"):
            if mapper.content_object:
                continue
            mapper.delete()

        # deleting event image mappers if an event was deleted
        for mapper in service.objectmapper_set.filter(content_type__model__iexact="eventimage"):
            if mapper.content_object:
                continue
            mapper.delete()
