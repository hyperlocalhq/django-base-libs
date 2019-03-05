# -*- coding: UTF-8 -*-
import os
import shutil
from collections import namedtuple
import requests

from django.utils.encoding import smart_str, force_unicode


StageSettings = namedtuple('StageSettings', ['location_title', 'internal_stage_title', 'should_create_stage_object'])


class LazyDictionary(object):
    def __init__(self, callback=dict):
        self.data = None
        self.callback = callback

    def evaluate_callback(self):
        self.data = self.callback()

    def __getitem__(self, name):
        if(self.data is None):
            self.evaluate_callback()
        return self.data.__getitem__(name)

    def __setitem__(self, name, value):
        if(self.data is None):
            self.evaluate_callback()
        return self.data.__setitem__(name, value)

    def __getattr__(self, name):
        if(self.data is None):
            self.evaluate_callback()
        return getattr(self.data, name)


LOCATIONS_TO_SKIP = [el.lower() for el in [
    u"-",
]]

def load_stage_to_location_mapper():
    return dict((k.lower(), v) for k, v in {
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

        u"Theater an der Parkaue - Bühne 2": StageSettings(u"Theater an der Parkaue", u"Bühne 2", True),

        u"Alten Feuerwache Eichwalde": StageSettings(u"Neuköllner Oper", u"Alten Feuerwache Eichwalde", True),

        u"Gorki Foyer Berlin": StageSettings(u"Maxim Gorki Theater", u"Foyer", True),
        u"Gorki Studio R": StageSettings(u"Maxim Gorki Theater", u"Studio Я", True),
        u"Studio Я": StageSettings(u"Maxim Gorki Theater", u"Studio Я", True),
        u"Vorplatz GORKI": StageSettings(u"Maxim Gorki Theater", u"Vorplatz GORKI", True),
        u"Maxim Gorki Theater": StageSettings(u"Maxim Gorki Theater", u"Gorki Theater", True),

        u"Tempodrom": StageSettings(u"Die Wühlmäuse", u"Tempodrom", False),
    }.iteritems())

STAGE_TO_LOCATION_MAPPER = LazyDictionary(load_stage_to_location_mapper)


def load_production_venues():
    return dict((k.lower(), v) for k, v in {
        u"Rotes Rathaus": u"Rotes Rathaus",
        u"Babylon Berlin-Mitte": u"Babylon Berlin-Mitte",
        u"Delphi Filmpalast": u"Delphi Filmpalast",
        u"Waldbühne Berlin": u"Waldbühne Berlin",
    }.iteritems())

PRODUCTION_VENUES = LazyDictionary(load_production_venues)


def load_location_title_mapper():
    return dict((k.lower(), v) for k, v in {
        u"English Theatre Berlin | International Performing Arts Center": u"English Theatre Berlin",
        u"Wühlmäuse": u"Die Wühlmäuse",  # where does it happen?
        u"SCHAUBUDE BERLIN - Theater.PuppenFigurenObjekte": u"SCHAUBUDE BERLIN",
        u"ATZE  Musiktheater": u"ATZE Musiktheater",
        u"Astrid Lindgren Bühne im FEZ Berlin": u"Astrid Lindgren Bühne im FEZ-Berlin",
        u"FEZ-Berlin und Landesmusikakademie Berlin": u"Landesmusikakademie Berlin im FEZ",
        u"UdK - Universität der Künste Berlin": u"UNI.T - Theater der UdK Berlin",
        u"Sophiensaele": u"Sophiensæle",
    }.iteritems())

LOCATION_TITLE_MAPPER = LazyDictionary(load_location_title_mapper)


def convert_location_title(title):
    return LOCATION_TITLE_MAPPER.get(title.lower(), title)


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
        from urllib import url2pathname
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


class ImportCommandMixin(object):
    """
    Command mixin with methods common for all types of import scripts
    """
    production_ids_to_keep = set()
    event_ids_to_keep = set()
    stats = {
        'prods_added': 0,
        'prods_updated': 0,
        'prods_skipped': 0,
        'prods_trashed': 0,
        'prods_untrashed': 0,
        'events_added': 0,
        'events_updated': 0,
        'events_skipped': 0,
        'events_trashed': 0,
        'events_untrashed': 0,
    }
    all_feeds_alright = True

    def get_full_url(self, url):
        from urlparse import urlparse
        if url.startswith('//'):
            url = "http:" + url
        if url.startswith('/'):
            if not hasattr(self, "_protocol_and_domain"):
                url_parts = urlparse(self.IMPORT_URL)
                self._protocol_and_domain = "{}://{}".format(url_parts.scheme, url_parts.netloc)
            url = self._protocol_and_domain + url
        return url

    def deactivate_nonactual_productions_and_events(self):
        from datetime import datetime, time

        # if import wasn't 100% successful, skip this function
        if not self.all_feeds_alright:
            return

        # if nothing new was imported, also skip this function
        if not (self.production_ids_to_keep and self.event_ids_to_keep):
            return

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Trashing non actual productions ===\n")

        counter = 0
        # get productions that were imported before, but don't exist in the feed anymore
        for prod_index, mapper in enumerate(self.service.objectmapper_set.filter(
            content_type__model__iexact="production"
        ).exclude(
            object_id__in=self.production_ids_to_keep
        ), 1):
            production = mapper.content_object
            if production:
                production.update_actual_date_and_time()

                # skip the productions that are already expired or were trashed before
                if production.status in ("expired", "trashed"):
                    continue

                if self.verbosity >= self.NORMAL:
                    counter += 1
                    self.stdout.write(u"%d %s | %s\n" % (counter, mapper.content_object.title_de, mapper.content_object.title_en))
                # don't trash items with no_overwriting == True
                if production.no_overwriting:
                    continue

                production.status = "trashed"
                production.save()
                self.stats['prods_trashed'] += 1

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Trashing non actual events ===\n")

        for mapper in self.service.objectmapper_set.filter(
            content_type__model__iexact="event",
        ).exclude(
            object_id__in=self.event_ids_to_keep
        ):
            event = mapper.content_object
            if event:
                # don't cancel events which productions have no_overwriting == True
                if event.production.no_overwriting:
                    continue

                # skip already trashed events
                if event.event_status == "trashed":
                    continue

                # only care about the events that will happen in the future
                if event.start_time is not None:
                    event_start = datetime.combine(event.start_date, event.start_time)
                else:
                    event_start = datetime.combine(event.start_date, time(0, 0))
                if event_start > datetime.now():
                    event.event_status = "trashed"
                    event.save()
                    self.stats['events_trashed'] += 1

    def delete_existing_productions_and_events(self):
        from django.conf import settings
        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Deleting existing productions ===\n")

        # deleting productions and their mappers
        prods_count = self.service.objectmapper_set.filter(content_type__model__iexact="production").count()
        for prod_index, mapper in enumerate(self.service.objectmapper_set.filter(content_type__model__iexact="production"), 1):
            if mapper.content_object:
                if self.verbosity >= self.NORMAL:
                    self.stdout.write(u"%d/%d %s | %s\n" % (prod_index, prods_count, mapper.content_object.title_de, mapper.content_object.title_en))
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
        for mapper in self.service.objectmapper_set.filter(content_type__model__iexact="event"):
            if mapper.content_object:
                if mapper.content_object.production.no_overwriting:  # don't delete items with no_overwriting == True
                    continue

                mapper.content_object.delete()
            mapper.delete()

        # deleting production images and their mappers if a production was deleted
        for mapper in self.service.objectmapper_set.filter(content_type__model__iexact="productionimage"):
            if mapper.content_object:
                continue
            mapper.delete()

        # deleting event images and their mappers if an event was deleted
        for mapper in self.service.objectmapper_set.filter(content_type__model__iexact="eventimage"):
            if mapper.content_object:
                continue
            mapper.delete()

    def delete_outdated_productions_and_events(self):
        from django.conf import settings
        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Deleting outdated productions ===\n")

        # deleting productions and their mappers
        prods_count = self.service.objectmapper_set.filter(
            content_type__model__iexact="production"
        ).exclude(
            object_id__in=self.production_ids_to_keep
        ).count()

        for prod_index, mapper in enumerate(self.service.objectmapper_set.filter(
            content_type__model__iexact="production"
        ).exclude(
            object_id__in=self.production_ids_to_keep
        ), 1):
            if mapper.content_object:
                if self.verbosity >= self.NORMAL:
                    self.stdout.write(u"%d/%d %s | %s\n" % (prod_index, prods_count, mapper.content_object.title_de, mapper.content_object.title_en))
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
        for mapper in self.service.objectmapper_set.filter(content_type__model__iexact="event").exclude(
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
        for mapper in self.service.objectmapper_set.filter(content_type__model__iexact="productionimage"):
            if mapper.content_object:
                continue
            mapper.delete()

        # deleting event image mappers if an event was deleted
        for mapper in self.service.objectmapper_set.filter(content_type__model__iexact="eventimage"):
            if mapper.content_object:
                continue
            mapper.delete()

    def report_results(self):
        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Results ===\n")
            self.stdout.write(u"Productions added: {}\n".format(self.stats['prods_added']))
            self.stdout.write(u"Productions updated: {}\n".format(self.stats['prods_updated']))
            self.stdout.write(u"Productions skipped: {}\n".format(self.stats['prods_skipped']))
            self.stdout.write(u"Productions trashed: {}\n".format(self.stats['prods_trashed']))
            self.stdout.write(u"Productions untrashed: {}\n".format(self.stats['prods_untrashed']))
            self.stdout.write(u"Events added: {}\n".format(self.stats['events_added']))
            self.stdout.write(u"Events updated: {}\n".format(self.stats['events_updated']))
            self.stdout.write(u"Events skipped: {}\n".format(self.stats['events_skipped']))
            self.stdout.write(u"Events trashed: {}\n".format(self.stats['events_trashed']))
            self.stdout.write(u"Events untrashed: {}\n".format(self.stats['events_untrashed']))

    def finalize(self):
        self.deactivate_nonactual_productions_and_events()
        self.report_results()
