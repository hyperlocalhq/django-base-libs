# -*- coding: UTF-8 -*-

import re
from dateutil.parser import parse as parse_datetime
import requests
import csv
from collections import namedtuple
from django.db import models

from django.utils.encoding import smart_str, force_unicode
from django.utils.text import slugify

from base_libs.utils.misc import get_unique_value

from berlinbuehnen.apps.productions.models import ProductionCategory
from berlinbuehnen.apps.productions.models import ProductionCharacteristics
from berlinbuehnen.apps.productions.models import Production
from berlinbuehnen.apps.productions.models import ProductionImage
from berlinbuehnen.apps.productions.models import Event
from berlinbuehnen.apps.productions.models import EventCharacteristics
from berlinbuehnen.apps.productions.models import EventImage
from berlinbuehnen.apps.people.models import Person
from berlinbuehnen.apps.sponsors.models import Sponsor

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


StageSettings = namedtuple('StageSettings', ['location_title', 'internal_stage_title'])

STAGE_TO_LOCATION_MAPPER = {
    u"Deutsches Theater - Box und Bar": StageSettings(u"Deutsches Theater Berlin", u"Box und Bar"),
    u"Deutsches Theater - Saal": StageSettings(u"Deutsches Theater Berlin", u"Saal"),
    u"Deutsches Theater Berlin - Kammerspiele": StageSettings(u"Deutsches Theater Berlin", u"Kammerspiele"),
    u"Hebbel am Ufer - HAU1": StageSettings(u"Hebbel am Ufer", u"HAU1"),  # new location name
    u"Hebbel am Ufer - HAU2": StageSettings(u"Hebbel am Ufer", u"HAU2"),  # new location name
    u"Hebbel am Ufer - HAU3": StageSettings(u"Hebbel am Ufer", u"HAU3"),  # new location name
    u"WAU im HAU2":  StageSettings(u"Hebbel am Ufer", u"WAU im HAU2"),  # new location name
    u"Volksbühne am Rosa-Luxemburg-Platz / 3. Stock": StageSettings(u"Volksbühne am Rosa-Luxemburg-Platz", u"3. Stock"),
    u"Volksbühne am Rosa-Luxemburg-Platz / Books": StageSettings(u"Volksbühne am Rosa-Luxemburg-Platz", u"Books"),
    u"Volksbühne am Rosa-Luxemburg-Platz / Grüner Salon": StageSettings(u"Volksbühne am Rosa-Luxemburg-Platz", u"Grüner Salon"),
    u"Volksbühne am Rosa-Luxemburg-Platz / Roter Salon": StageSettings(u"Volksbühne am Rosa-Luxemburg-Platz", u"Roter Salon"),
    u"Admiralspalast 101": StageSettings(u"Admiralspalast", u"F101"),  # new location name
    u"Admiralspalast Studio": StageSettings(u"Admiralspalast", u"Studio"),  # new location name
    u"Admiralspalast Theater": StageSettings(u"Admiralspalast", u"Theater"), # new location name
    u"Berliner Ensemble/ Foyer": StageSettings(u"Berliner Ensemble", u"Foyer"),
    u"Berliner Ensemble/ Pavillon": StageSettings(u"Berliner Ensemble", u"Pavillon"),
    u"Berliner Ensemble/ Probebühne": StageSettings(u"Berliner Ensemble", u"Probebühne"),
    u"Berliner Philharmonie – Kammermusiksaal": StageSettings(u"Berliner Philharmonie", u"Kammermusiksaal"),
	u"Konzerthaus Berlin - Großer Saal": StageSettings(u"Konzerthaus Berlin", u"Großer Saal"),
	u"Konzerthaus Berlin - Kleiner Saal": StageSettings(u"Konzerthaus Berlin", u"Kleiner Saal"),
	u"Konzerthaus Berlin - Ludwig-van-Beethoven-Saal": StageSettings(u"Konzerthaus Berlin", u"Ludwig-van-Beethoven-Saal"),
	u"Konzerthaus Berlin - Musikclub": StageSettings(u"Konzerthaus Berlin", u"Musikclub"),
	u"Konzerthaus Berlin - Werner-Otto-Saal": StageSettings(u"Konzerthaus Berlin", u"Werner-Otto-Saal"),
    u"Renaissance-Theater Berlin - Bruckner-Foyer": StageSettings(u"Renaissance-Theater Berlin", u"Bruckner-Foyer"),
    u"Sophiensaele - Festsaal": StageSettings(u"Sophiensaele", u"Festsaal"),
	u"Sophiensaele - Hochzeitssaal": StageSettings(u"Sophiensaele", u"Hochzeitssaal"),
	u"Staatsoper im Schiller Theater - Gläsernes Foyer": StageSettings(u"Staatsoper im Schiller Theater", u"Gläsernes Foyer"),
	u"Staatsoper im Schiller Theater - Werkstatt": StageSettings(u"Staatsoper im Schiller Theater", u"Werkstatt"),
    u"Theater an der Parkaue - Bühne 2": StageSettings(u"Theater an der Parkaue", u"Bühne 2"),
    u"Gorki Foyer Berlin": StageSettings(u"Gorki Theater", u"Gorki Foyer Berlin"),  # new location name
	u"Gorki Studio R": StageSettings(u"Gorki Theater", u"Studio Я"),  # new location name
}

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
    LOCATIONS = {}
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

    def load_and_parse_locations(self):
        response = requests.get("http://web2.heimat.de/cb-out/exports/address/address_id.php?city=berlin")
        if response.status_code != 200:
            return
        reader = csv.reader(response.content.splitlines(), delimiter=";")
        reader.next()  # skip the first line
        for row in reader:
            # if row[0] == "locationId":  # skip the first row
            #     continue
            self.LOCATIONS[row[0]] = CultureBaseLocation(*row)

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
            if all_attributes_match and child_node.text:
                return force_unicode(child_node.text)
        return u""

    def create_or_update_location(self, venue_node):
        from berlinbuehnen.apps.locations.models import Location
        ObjectMapper = models.get_model("external_services", "ObjectMapper")

        if not self.LOCATIONS:
            self.load_and_parse_locations()

        if venue_node.get('isId') == "1":
            external_id = venue_node.text
        else:  # unknown location id
            return None, False

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

        if external_id not in self.LOCATIONS:  # location not found in Berlin
            return None, False

        culturbase_location = self.LOCATIONS[external_id]

        locations_by_title = Location.objects.filter(title=culturbase_location.title)
        if locations_by_title and not location.pk:
            location = locations_by_title[0]
        else:
            location.title_de = location.title_en = culturbase_location.title
            location.street_address = culturbase_location.street_address
            location.postal_code = culturbase_location.postal_code
            location.city = "Berlin"
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

    def cleanup_text(self, text):
        from BeautifulSoup import BeautifulStoneSoup
        from django.utils.html import strip_tags
        text = text.replace('</div>', '\n')
        text = strip_tags(text)
        text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
        return text

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
                    instance.concert_programm_de = text_de
                    instance.concert_programm_de_markup_type = 'pt'
                if text_en:
                    instance.concert_programm_en = text_en
                    instance.concert_programm_en_markup_type = 'pt'
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
                    instance.supporting_programm_de = text_de
                    instance.supporting_programm_de_markup_type = 'pt'
                if text_en:
                    instance.supporting_programm_en = text_en
                    instance.supporting_programm_en_markup_type = 'pt'
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

    def save_page(self, root_node):
        import time
        from filebrowser.models import FileDescription
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        image_mods = models.get_app("image_mods")

        prod_nodes = root_node.findall('production')
        prods_count = len(prod_nodes)

        for prod_index, prod_node in enumerate(prod_nodes, 1):
            external_prod_id = prod_node.get('foreignId')

            title_de = self.get_child_text(prod_node, 'title', languageId="1")
            title_en = self.get_child_text(prod_node, 'title', languageId="2")
            if self.verbosity > NORMAL:
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

            if not title_de:  # skip productions without title
                self.stats['prods_skipped'] += 1
                continue
            prod.title_de = title_de
            prod.title_en = title_en or title_de
            prod.website = prod_node.get('url')

            prod.slug = get_unique_value(Production, slugify(prod.title_de))

            self.parse_and_use_texts(prod_node, prod)
            
            prod.save()

            venue_node = prod_node.find('location')
            if venue_node is not None:
                location, created = self.create_or_update_location(venue_node)
                if location:
                    prod.play_locations.clear()
                    prod.play_locations.add(location)
                else:
                    prod.location_title = venue_node.text
                    prod.save()

            institution_node = prod_node.find('institution')
            if institution_node is not None:
                location, created = self.create_or_update_location(institution_node)
                if location:
                    prod.in_program_of.clear()
                    prod.in_program_of.add(location)
                else:
                    prod.organizer_title = institution_node.text
                    prod.save()

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
                        if picture_node.get('publishType') == "1":
                            mf.copyright_restrictions = "general_use"
                        elif picture_node.get('publishType') == "3":
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
                        file_description.author = (picture_node.get('photographer') or u"").replace("Foto: ", "")
                        file_description.copyright_limitations = picture_node.get('copyright')
                        file_description.save()
                        #time.sleep(1)

            for category_node in prod_node.findall('category'):
                internal_cat_id = self.CATEGORY_MAPPER.get(int(category_node.text), None)
                if internal_cat_id:
                    prod.categories.add(ProductionCategory.objects.get(pk=internal_cat_id))

            for status_id_node in prod_node.findall('statusId'):
                internal_ch_slug = self.PRODUCTION_CHARACTERISTICS_MAPPER.get(int(status_id_node.text), None)
                if internal_ch_slug:
                    prod.characteristics.add(ProductionCharacteristics.objects.get(slug=internal_ch_slug))

            if not prod.productioninvolvement_set.count():
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

            if not prod.sponsors.count():
                for sponsor_node in prod_node.findall('./sponsor'):
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
                    else:
                        event.price_from = price_from
                    event.price_till = (price_node.get('maxPrice') or u"").replace(',', '.') or None
                    event.tickets_website = price_node.get('url')

                flag_status = int(event_node.get('takingPlace'))
                if flag_status == 0:  # fällt aus
                    event.event_status = 'canceled'
                elif flag_status == 1:  # findet statt
                    event.event_status = 'takes_place'
                elif flag_status == 2:  # ausverkauft
                    event.ticket_status = 'sold_out'

                self.parse_and_use_texts(event_node, event)

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
                            if picture_node.get('publishType') == "1":
                                mf.copyright_restrictions = "general_use"
                            elif picture_node.get('publishType') == "3":
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
                            file_description.author = (picture_node.get('photographer') or u"").replace("Foto: ", "")
                            file_description.copyright_limitations = picture_node.get('copyright')
                            file_description.save()
                            #time.sleep(1)

                venue_node = event_node.find('location')
                if venue_node is not None:
                    location, created = self.create_or_update_location(venue_node)
                    if location:
                        event.play_locations.clear()
                        event.play_locations.add(location)
                    else:
                        event.location_title = venue_node.text
                        event.save()

                for status_id_node in event_node.findall('statusId'):
                    internal_ch_slug = self.EVENT_CHARACTERISTICS_MAPPER.get(int(status_id_node.text), None)
                    if internal_ch_slug:
                        event.characteristics.add(EventCharacteristics.objects.get(slug=internal_ch_slug))

                if not event.eventinvolvement_set.count():
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
                if not event.sponsors.count():
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
