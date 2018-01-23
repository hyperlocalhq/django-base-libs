# -*- coding: UTF-8 -*-
from optparse import make_option
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells Django to NOT download images.'),
    )
    help = """Imports exhibitions, events, and workshops from Staatliche Museen zu Berlin"""

    MUSEUM_MAPPER = {
        43009: 62,      # Ethnologisches Museum
        43010: 129,     # Museum Europäischer Kulturen
        43011: 130,     # Museum für Asiatische Kunst
        31: 150,        # Neue Nationalgalerie
        35: 77,         # Gemäldegalerie
        37: 105,        # Kunstgewerbemuseum
        39: 107,        # Kupferstichkabinett
        40: 103,        # Kunstbibliothek
        24: 9,          # Altes Museum
        25: 152,        # Neues Museum
        27: 157,        # Pergamonmuseum
        28: 35,         # Bode-Museum
        29: 8,          # Alte Nationalgalerie
        32: 67,         # Friedrichswerdersche Kirche
        179: 113,       # Martin-Gropiu-Bau
        26: 177,        # Schloss Köpenick
        30: 84,         # Hamburger Bahnhof - Museum für Gegenwart
        43: 79,         # Gipsformerei
        48: 0,          # Institut für Museumsforschung
        2433: 0,        # Rathgen-Forschungslabor
        27774: 0,       # Zentralarchiv
        37096: 0,       # Archäologisches Zentrum
        43007: 0,       # Humboldt-Forum
        43008: 0,       # Generaldirektion
        45: 166,        # Sammlung Scharf-Gerstenberg
        2976: 124,      # Museum Berggruen
        6124: 131,      # Museum für Fotografie
    }

    LINKED_INSTITUTION_MAPPER = {
        3: 13,          # Antikensammlung
        2: 16,          # Ägyptisches Museum und Papyrussammlung
        12: 132,        # Museum für Islamische Kunst
        15: 135,        # Museum für Vor- und Frühgeschichte
        9: 118,         # Münzkabinett
        14: 185,        # Skulpturensammlung und Museum für Byzantinische Kunst
        23: 195,        # Vorderasiatisches Museum
    }

    def handle_noargs(self, **options):
        self.import_exhibitions(**options)
        self.import_events_and_workshops(**options)

    def import_exhibitions(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        skip_images = options.get('skip_images')
        
        weekdays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

        import time
        import urllib2
        import json
        from datetime import datetime, timedelta
        from dateutil.parser import parse as parse_datetime
        from decimal import Decimal
        
        from django.db import models
        from django.template.defaultfilters import slugify

        from filebrowser.models import FileDescription

        from base_libs.utils.misc import get_unique_value

        image_mods = models.get_app("image_mods")
        Museum = models.get_model("museums", "Museum")
        Exhibition = models.get_model("exhibitions", "Exhibition")
        ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")
        Organizer = models.get_model("exhibitions", "Organizer")
        MediaFile = models.get_model("exhibitions", "MediaFile")
        Season = models.get_model("exhibitions", "Season")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Service = models.get_model("external_services", "Service")
        
        ### IMPORT EXHIBITIONS ###
        if verbosity > 1:
            print u"### IMPORTING EXHIBITIONS ###"
        s_exhibitions, created = Service.objects.get_or_create(
            sysname="smb_exhibitions_smart",
            defaults={
                'url': "http://ww2.smb.museum/smb/export/getExhibitionListFromSMart.php?format=json",
                'title': "SMB - Exhibitions SMart",
            },
        )
        response = urllib2.urlopen(s_exhibitions.url)
        data = response.read()
        response.close()

        list_data_dict = json.loads(data)

        stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
        }
        for external_id, exhibition_dict in list_data_dict.items():

            # get or create exhibition
            mapper = None
            try:
                # get exhibition from saved mapper
                mapper = s_exhibitions.objectmapper_set.get(
                    external_id=external_id,
                    content_type__app_label="exhibitions",
                    content_type__model="exhibition",
                )
            except models.ObjectDoesNotExist:
                # or create a new exhibition and then create a mapper
                exhibition = Exhibition()
            else:
                exhibition = mapper.content_object
                if not exhibition:
                    # if exhibition was deleted after import,
                    # don't import it again
                    stats['skipped'] += 1
                    continue
                else:
                    if parse_datetime(exhibition_dict['lastaction'], ignoretz=True) < datetime.now() - timedelta(days=1):
                        stats['skipped'] += 1
                        continue

            museum = None
            museum_guid = int(exhibition_dict['location']['SMart_id'])
            try:
                museum = Museum.objects.get(pk=self.MUSEUM_MAPPER[museum_guid])
            except:
                pass

            response = urllib2.urlopen("http://ww2.smb.museum/smb/export/getExhibitionFromSMart.php?format=json&SMart_id=%s" % external_id)
            data = response.read()
            response.close()
            data_dict = json.loads(data)

            if data_dict['status'] != "www":
                stats['skipped'] += 1
                continue

            exhibition.title_de = data_dict['title_de']
            exhibition.title_en = data_dict['title_en'] or data_dict['title_de']
            exhibition.subtitle_de = data_dict['subtitle_de']
            exhibition.subtitle_en = data_dict['subtitle_en']

            exhibition.slug = get_unique_value(Exhibition, slugify(data_dict['title_de']))

            exhibition.start = parse_datetime(data_dict['start_date'])
            if data_dict['perma_exhibition'] == 1 or data_dict['end_date'] == "unlimited":
                exhibition.permanent = True
                exhibition.museum_prices = True
            else:
                exhibition.end = parse_datetime(data_dict['end_date'])
            exhibition.website_de = data_dict['link_de'].replace('&amp;', '&')
            exhibition.website_en = data_dict['link_en'].replace('&amp;', '&')
            if not exhibition.description_locked:
                exhibition.description_de = data_dict['description_de']
                exhibition.description_de_markup_type = "hw"
                exhibition.description_en = data_dict['description_en']
                exhibition.description_en_markup_type = "hw"
            exhibition.press_text_de = data_dict['description_de']
            exhibition.press_text_de_markup_type = "hw"
            exhibition.press_text_en = data_dict['description_en']
            exhibition.press_text_en_markup_type = "hw"
            if museum:
                exhibition.museum = museum
                exhibition.street_address = museum.street_address
                exhibition.street_address2 = museum.street_address2
                exhibition.postal_code = museum.postal_code
                exhibition.city = museum.city
                exhibition.country = museum.country
                exhibition.latitude = museum.latitude
                exhibition.longitude = museum.longitude
            else:
                exhibition.location_name = data_dict['location']['name']
                
            exhibition.museum_opening_hours = data_dict['opening_from_museum']

            prices = data_dict.get('tarife', [])
            if prices:
                if prices[0]['preis_voll']:
                    exhibition.admission_price = Decimal(prices[0]['preis_voll'].replace(",", ".").replace("-", "00"))
                if prices[0]['preis_erm']:
                    exhibition.reduced_price = Decimal(prices[0]['preis_erm'].replace(",", ".").replace("-", "00"))
                exhibition.admission_price_info_de = u". ".join((prices[0]['label_de'], prices[0]['description_de']))
                exhibition.admission_price_info_de_markup_type = "pt"
                exhibition.admission_price_info_en = u". ".join((prices[0]['label_en'], prices[0]['description_en']))
                exhibition.admission_price_info_en_markup_type = "pt"
                if prices[0]['shop_link']:
                    exhibition.shop_link_de = prices[0]['shop_link']
                    exhibition.shop_link_en = prices[0]['shop_link']

            exhibition.status = "import"
            exhibition.save()

            exhibition.organizer_set.all().delete()
            linked_institutions = data_dict.get('linked_institutions', {})
            if linked_institutions:
                for linked_inst_smb_id in linked_institutions.keys():
                    try:
                        organizing_museum = Museum.objects.get(pk=self.LINKED_INSTITUTION_MAPPER.get(int(linked_inst_smb_id), None))
                    except:
                        Organizer(
                            exhibition=exhibition,
                            organizer_title=linked_institutions[linked_inst_smb_id],
                        ).save()
                    else:
                        Organizer(
                            exhibition=exhibition,
                            organizing_museum=organizing_museum,
                        ).save()

            # set exhibition categories based on museum and organizing museums
            exhibition.categories.clear()
            if museum:
                for museum_cat in museum.categories.all():
                    try:
                        exhibition_cat = ExhibitionCategory.objects.get(title_de=museum_cat.title_de)
                    except:
                        continue
                    else:
                        exhibition.categories.add(exhibition_cat)
            for organizer in exhibition.organizer_set.exclude(organizing_museum=None):
                for museum_cat in organizer.organizing_museum.categories.all():
                    try:
                        exhibition_cat = ExhibitionCategory.objects.get(title_de=museum_cat.title_de)
                    except:
                        continue
                    else:
                        exhibition.categories.add(exhibition_cat)

            if data_dict['openings']:
                try:
                    season = Season.objects.filter(exhibition=exhibition)[0]
                except IndexError:
                    season = Season(exhibition=exhibition)

                # The value of "openings" is either an JSON array -> Python list, or a JSON object -> Python dict
                items = []
                if isinstance(data_dict['openings'], dict):
                    items = data_dict['openings'].items()
                elif isinstance(data_dict['openings'], list):
                    items = enumerate(data_dict['openings'])

                for day_index, times in items:
                    start_h = times['start_h']
                    if start_h == "24":
                        start_h = "0"
                    ende_h = times['ende_h']
                    if ende_h == "24":
                        ende_h = "0"
                    from_time = start_h + ':' + times['start_min']
                    till_time = ende_h + ':' + times['ende_min']
                    setattr(season, "%s_open" % weekdays[int(day_index)], parse_datetime(from_time).time())
                    setattr(season, "%s_close" % weekdays[int(day_index)], parse_datetime(till_time).time())
                season.save()
            else:
                Season.objects.filter(exhibition=exhibition).delete()


            # get biggest possible images
            img_teaser = (data_dict.get('img_teaser_963', []) or data_dict.get('img_teaser_637', []))
            if img_teaser and not skip_images and not exhibition.mediafile_set.count():
                for image_dict in img_teaser:
                    image_url = image_dict['path']
                    mf = MediaFile(exhibition=exhibition)
                    filename = image_url.split("/")[-1]
                    image_data = urllib2.urlopen(image_url)
                    image_mods.FileManager.save_file_for_object(
                        mf,
                        filename,
                        image_data.read(),
                        field_name="path",
                        subpath="exhibitions/%s/gallery/" % exhibition.slug,
                    )
                    mf.save()
                    try:
                        file_description = FileDescription.objects.filter(
                            file_path=mf.path,
                        ).order_by("pk")[0]
                    except:
                        file_description = FileDescription(file_path=mf.path)
                    
                    file_description.title_de = image_dict['description_de']
                    file_description.title_en = image_dict['description_en']
                    file_description.author = image_dict['copyright_de']
                    file_description.save()
                    time.sleep(1)

            if not mapper:
                mapper = ObjectMapper(
                    service=s_exhibitions,
                    external_id=external_id,
                )
                mapper.content_object = exhibition
                mapper.save()
                stats['added'] += 1
            else:
                stats['updated'] += 1
    
        if verbosity > 1:
            print u"Exibitions added: %d" % stats['added']
            print u"Exibitions updated: %d" % stats['updated']
            print u"Exibitions skipped: %d" % stats['skipped']
            print

    @staticmethod
    def parse_title_and_subtitle(text):
        lines = [line.strip() for line in text.split("<br />") if line.strip()]
        if not lines:
            return u"", u""
        # if there is just one line, the subtitle will be empty
        # if there are more than 2 lines, the 2nd line will be connected to the rest for the subtitle
        return lines[0], u" ".join(lines[1:])

    def cleanup_html(self, text):
        text = text.replace("<br />", ". ")
        text = text.replace("&ndash;", "-")
        text = text.replace("&bdquo;", '"')
        text = text.replace("&ldquo;", '"')
        return text

    def import_events_and_workshops(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        skip_images = options.get('skip_images')

        import time
        import urllib2
        import json
        from datetime import datetime, timedelta
        from dateutil.parser import parse as parse_datetime
        from decimal import Decimal

        from django.db import models
        from django.template.defaultfilters import slugify
        from django.conf import settings

        from filebrowser.models import FileDescription

        from base_libs.utils.misc import get_unique_value

        image_mods = models.get_app("image_mods")
        Museum = models.get_model("museums", "Museum")
        Event = models.get_model("events", "Event")
        EventCategory = models.get_model("events", "EventCategory")
        EventTime = models.get_model("events", "EventTime")
        Workshop = models.get_model("workshops", "Workshop")
        WorkshopType = models.get_model("workshops", "WorkshopType")
        WorkshopTime = models.get_model("workshops", "WorkshopTime")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Service = models.get_model("external_services", "Service")

        ### IMPORT EVENTS AND WORKSHOPS ###
        if verbosity > 1:
            print u"### IMPORTING EVENTS AND WORKSHOPS ###"

        s_exhibitions, created = Service.objects.get_or_create(
            sysname="smb_exhibitions_smart",
            defaults={
                'url': "http://ww2.smb.museum/smb/export/getExhibitionListFromSMart.php?format=json",
                'title': "SMB - Exhibitions SMart",
            },
        )

        s_events, created = Service.objects.get_or_create(
            sysname="smb_events_smart",
            defaults={
                'url': "http://ww2.smb.museum/smb/export/getEventListFromSMart.php?format=json",
                'title': "SMB - Events SMart",
            },
        )

        response = urllib2.urlopen(s_events.url)
        data = response.read()
        response.close()

        list_data_dict = json.loads(data)

        event_stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
        }
        workshop_stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
        }

        for external_id, event_dict in list_data_dict.items():

            # based on http://ww2.smb.museum/smb/export/getEventTypeListFromSMart.php?format=json
            event_type_ids = (event_dict.get('event_types_detail', {}) or {}).keys()
            if event_type_ids and int(event_type_ids[0]) in (45, 215, 216, 217, 218, 219, 137):

                Organizer = models.get_model("workshops", "Organizer")

                # get or create event
                mapper = None
                try:
                    # get workshop from saved mapper
                    mapper = s_events.objectmapper_set.get(
                        external_id=external_id,
                        content_type__app_label="workshops",
                        content_type__model="workshop",
                    )
                except models.ObjectDoesNotExist:
                    # or create a new workshop and then create a mapper
                    workshop = Workshop()
                else:
                    workshop = mapper.content_object
                    if not workshop:
                        # if workshop was deleted after import,
                        # don't import it again
                        workshop_stats['skipped'] += 1
                        continue
                    else:
                        if parse_datetime(event_dict['lastaction'], ignoretz=True) < datetime.now() - timedelta(days=1):
                            workshop_stats['skipped'] += 1
                            continue

                museum = None
                museum_guid = int(event_dict['location']['SMart_id'])
                try:
                    museum = Museum.objects.get(pk=self.MUSEUM_MAPPER[museum_guid])
                except:
                    pass

                if museum:
                    workshop.museum = museum
                    workshop.street_address = museum.street_address
                    workshop.street_address2 = museum.street_address2
                    workshop.postal_code = museum.postal_code
                    workshop.city = museum.city
                    workshop.country = museum.country
                    workshop.latitude = museum.latitude
                    workshop.longitude = museum.longitude

                response = urllib2.urlopen("http://ww2.smb.museum/smb/export/getEventFromSMartByTerminId.php?format=json&SMarttermin_id=%s" % min(event_dict['dates'].keys()))
                data = response.read()
                response.close()
                data_dict = json.loads(data)

                if data_dict['status'] != "www":
                    workshop_stats['skipped'] += 1
                    continue

                workshop.title_de, workshop.subtitle_de = self.cleanup_html(data_dict['title_de']), self.cleanup_html(data_dict['title_sub_de'])
                workshop.title_en, workshop.subtitle_en = self.cleanup_html(data_dict['title_en']), self.cleanup_html(data_dict['title_sub_en'])
                if not workshop.title_en:
                    workshop.title_en = workshop.title_de
                if not workshop.subtitle_en:
                    workshop.subtitle_en = workshop.subtitle_de

                workshop.slug = get_unique_value(Workshop, slugify(data_dict['title_de']))

                workshop.website_de = data_dict['link_de'].replace('&amp;', '&')
                workshop.website_en = data_dict['link_en'].replace('&amp;', '&')
                workshop.description_de = data_dict['description_de']
                workshop.description_de_markup_type = "hw"
                workshop.description_en = data_dict['description_en']
                workshop.description_en_markup_type = "hw"
                workshop.press_text_de = data_dict['description_de']
                workshop.press_text_de_markup_type = "hw"
                workshop.press_text_en = data_dict['description_en']
                workshop.press_text_en_markup_type = "hw"
                price_str = data_dict['kosten_de'].replace(",", ".").replace("-", "00").split(" ")[0]
                if price_str:
                    try:
                        workshop.admission_price = Decimal(price_str)
                    except:
                        pass
                workshop.admission_price_info_de = data_dict.get('admission_de', "")
                workshop.admission_price_info_de_markup_type = "pt"
                workshop.admission_price_info_en = data_dict.get('admission_en', "")
                workshop.admission_price_info_en_markup_type = "pt"
                workshop.shop_link_de = data_dict.get('shop_link', "")
                workshop.shop_link_en = data_dict.get('shop_link', "")
                workshop.meeting_place_de = data_dict['treffpunkt_de']
                workshop.meeting_place_en = data_dict['treffpunkt_en']
                workshop.booking_info_de = data_dict['registration_de']
                workshop.booking_info_de_markup_type = "pt"
                workshop.booking_info_en = data_dict['registration_en']
                workshop.booking_info_en_markup_type = "pt"

                # based on http://ww2.smb.museum/smb/export/getTargetGroupListFromSMart.php?format=json
                for target_group_id in (data_dict.get('event_targetgroup_detail', {}) or {}).keys():
                    target_group_id = int(target_group_id)
                    if target_group_id in (301, 302, 303):  # "Kinder"
                        workshop.is_for_primary_school = True
                    elif target_group_id == 304:  # "Jugendliche"
                        workshop.is_for_youth = True
                    elif target_group_id == 305:  # "Familien + Kinder 4-6"
                        workshop.is_for_preschool = True
                        workshop.is_for_families = True
                    elif target_group_id == 306:  # "Familien + Kinder 6-12"
                        workshop.is_for_primary_school = True
                        workshop.is_for_families = True
                    elif target_group_id == 212:
                        workshop.is_for_families = True
                    elif target_group_id == 204:
                        workshop.is_for_deaf = True
                    elif target_group_id == 205:
                        workshop.is_for_blind = True
                    elif target_group_id == 206:
                        workshop.is_for_wheelchaired = True
                    elif target_group_id == 207:
                        workshop.is_for_dementia_sufferers = True

                workshop.museum = museum

                exhibition_ids = data_dict.get('linked_exhibitions', {}).keys()
                if exhibition_ids:
                    # correct exhibition to link is the first one being not permanent or any first otherwise
                    correct_exhibition_id = exhibition_ids[0]
                    for e_id in exhibition_ids:
                        if data_dict['linked_exhibitions'][e_id]['perma_exhibition'] == "0":
                            correct_exhibition_id = e_id
                            break

                    try:
                        # get exhibition from saved mapper
                        exh_mapper = s_exhibitions.objectmapper_set.get(
                            external_id=correct_exhibition_id,
                            content_type__app_label="exhibitions",
                            content_type__model="exhibition",
                        )
                    except models.ObjectDoesNotExist:
                        pass
                    else:
                        workshop.exhibition = exh_mapper.content_object

                workshop.status = "import"
                workshop.save()

                workshop.types.clear()
                if int(event_dict['event_types_detail'].keys()[0]) == 137:
                    workshop.types.add(WorkshopType.objects.get(slug="workshop"))
                else:
                    workshop.types.add(WorkshopType.objects.get(slug="guided-tour"))

                if workshop.exhibition and not workshop.mediafile_set.count():
                    MediaFile = models.get_model("workshops", "MediaFile")

                    for exh_mf in workshop.exhibition.mediafile_set.all():
                        mf = MediaFile(workshop=workshop)
                        filename = exh_mf.path.filename
                        try:
                            image_data = open(settings.MEDIA_ROOT + "/" + exh_mf.path.path, "rb")
                        except IOError:
                            continue
                        image_mods.FileManager.save_file_for_object(
                            mf,
                            filename,
                            image_data.read(),
                            field_name="path",
                            subpath="workshops/%s/gallery/" % workshop.slug,
                        )
                        image_data.close()
                        mf.save()
                        exh_file_descriptions = FileDescription.objects.filter(
                            file_path=exh_mf.path,
                        ).order_by("pk")
                        if exh_file_descriptions:
                            try:
                                file_description = FileDescription.objects.filter(
                                    file_path=mf.path,
                                ).order_by("pk")[0]
                            except:
                                file_description = FileDescription(file_path=mf.path)

                            file_description.title_de = exh_file_descriptions[0].title_de
                            file_description.title_en = exh_file_descriptions[0].title_en
                            file_description.author = exh_file_descriptions[0].author
                            file_description.save()
                        time.sleep(1)

                workshop.organizer_set.all().delete()
                linked_institutions = data_dict.get('linked_institutions', {})
                if linked_institutions:
                    for linked_inst_smb_id in linked_institutions.keys():
                        try:
                            organizing_museum = Museum.objects.get(pk=self.LINKED_INSTITUTION_MAPPER.get(int(linked_inst_smb_id), None))
                        except:
                            Organizer(
                                workshop=workshop,
                                organizer_title=linked_institutions[linked_inst_smb_id],
                            ).save()
                        else:
                            Organizer(
                                workshop=workshop,
                                organizing_museum=organizing_museum,
                            ).save()

                workshop.workshoptime_set.all().delete()

                start = parse_datetime(data_dict['start'], ignoretz=True)
                if data_dict['end']:
                    end = parse_datetime(data_dict['end'], ignoretz=True)
                else:
                    end = start + timedelta(minutes=60)

                workshop_time = WorkshopTime(
                    workshop=workshop,
                    workshop_date=start.date(),
                    start=start.time(),
                    end=end.time(),
                )
                workshop_time.save()

                for event_time_id, event_time_dict in data_dict.get('more_dates', {}).items():
                    start = parse_datetime(event_time_dict['start'], ignoretz=True)
                    if event_time_dict['end']:
                        end = parse_datetime(event_time_dict['end'], ignoretz=True)
                    else:
                        end = start + timedelta(minutes=60)

                    workshop_time = WorkshopTime(
                        workshop=workshop,
                        workshop_date=start.date(),
                        start=start.time(),
                        end=end.time(),
                    )
                    workshop_time.save()

                workshop.update_closest_workshop_time()

                if not mapper:
                    mapper = ObjectMapper(
                        service=s_events,
                        external_id=external_id,
                    )
                    mapper.content_object = workshop
                    mapper.save()
                    if verbosity > 1:
                        workshop_stats['added'] += 1
                else:
                    if verbosity > 1:
                        workshop_stats['updated'] += 1
            else:

                Organizer = models.get_model("events", "Organizer")

                # get or create event
                mapper = None
                try:
                    # get event from saved mapper
                    mapper = s_events.objectmapper_set.get(
                        external_id=external_id,
                        content_type__app_label="events",
                        content_type__model="event",
                    )
                except models.ObjectDoesNotExist:
                    # or create a new article and then create a mapper
                    event = Event()
                else:
                    event = mapper.content_object
                    if not event:
                        # if event was deleted after import,
                        # don't import it again
                        event_stats['skipped'] += 1
                        continue
                    else:
                        if parse_datetime(event_dict['lastaction'], ignoretz=True) < datetime.now() - timedelta(days=1):
                            event_stats['skipped'] += 1
                            continue

                museum = None
                museum_guid = int(event_dict['location']['SMart_id'])
                try:
                    museum = Museum.objects.get(pk=self.MUSEUM_MAPPER[museum_guid])
                except:
                    pass

                if museum:
                    event.museum = museum
                    event.street_address = museum.street_address
                    event.street_address2 = museum.street_address2
                    event.postal_code = museum.postal_code
                    event.city = museum.city
                    event.country = museum.country
                    event.latitude = museum.latitude
                    event.longitude = museum.longitude

                response = urllib2.urlopen("http://ww2.smb.museum/smb/export/getEventFromSMartByTerminId.php?format=json&SMarttermin_id=%s" % min(event_dict['dates'].keys()))
                data = response.read()
                response.close()
                data_dict = json.loads(data)

                if data_dict['status'] != "www":
                    event_stats['skipped'] += 1
                    continue

                event.title_de, event.subtitle_de = self.cleanup_html(data_dict['title_de']), self.cleanup_html(data_dict['title_sub_de'])
                event.title_en, event.subtitle_en = self.cleanup_html(data_dict['title_en']), self.cleanup_html(data_dict['title_sub_en'])
                if not event.title_en:
                    event.title_en = event.title_de
                if not event.subtitle_en:
                    event.subtitle_en = event.subtitle_de

                event.slug = get_unique_value(Event, slugify(data_dict['title_de']))

                event.website_de = data_dict['link_de'].replace('&amp;', '&')
                event.website_en = data_dict['link_en'].replace('&amp;', '&')
                event.description_de = data_dict['description_de']
                event.description_de_markup_type = "hw"
                event.description_en = data_dict['description_en']
                event.description_en_markup_type = "hw"
                event.press_text_de = data_dict['description_de']
                event.press_text_de_markup_type = "hw"
                event.press_text_en = data_dict['description_en']
                event.press_text_en_markup_type = "hw"
                price_str = data_dict['kosten_de'].replace(",", ".").replace("-", "00").split(" ")[0]
                if price_str:
                    try:
                        event.admission_price = Decimal(price_str)
                    except:
                        pass
                event.admission_price_info_de = data_dict.get('admission_de', "")
                event.admission_price_info_de_markup_type = "pt"
                event.admission_price_info_en = data_dict.get('admission_en', "")
                event.admission_price_info_en_markup_type = "pt"
                event.shop_link_de = data_dict.get('shop_link', "")
                event.shop_link_en = data_dict.get('shop_link', "")
                event.meeting_place_de = data_dict['treffpunkt_de']
                event.meeting_place_en = data_dict['treffpunkt_en']
                event.booking_info_de = data_dict['registration_de']
                event.booking_info_de_markup_type = "pt"
                event.booking_info_en = data_dict['registration_en']
                event.booking_info_en_markup_type = "pt"

                # based on http://ww2.smb.museum/smb/export/getTargetGroupListFromSMart.php?format=json
                for target_group_id in (data_dict.get('event_targetgroup_detail', {}) or {}).keys():
                    target_group_id = int(target_group_id)
                    if target_group_id in (301, 302, 303, 304, 305, 306):  # "Kinder", "Jugendliche", "Familien + Kinder 4-6", "Familien + Kinder 6-12"
                        event.suitable_for_children = True

                event.museum = museum

                exhibition_ids = data_dict.get('linked_exhibitions', {}).keys()
                if exhibition_ids:
                    # correct exhibition to link is the first one being not permanent or any first otherwise
                    correct_exhibition_id = exhibition_ids[0]
                    for e_id in exhibition_ids:
                        if data_dict['linked_exhibitions'][e_id]['perma_exhibition'] == "0":
                            correct_exhibition_id = e_id
                            break
                    try:
                        # get exhibition from saved mapper
                        exh_mapper = s_exhibitions.objectmapper_set.get(
                            external_id=correct_exhibition_id,
                            content_type__app_label="exhibitions",
                            content_type__model="exhibition",
                        )
                    except models.ObjectDoesNotExist:
                        pass
                    else:
                        event.exhibition = exh_mapper.content_object

                event.status = "import"
                event.save()

                event.categories.clear()
                for event_cat_id in (event_dict.get('event_types_detail', {}) or {}).keys():
                    event_cat_id = int(event_cat_id)
                    if event_cat_id in (189, 220):
                        event.categories.add(EventCategory.objects.get(slug="fest-markt"))
                    elif event_cat_id == 47:
                        event.categories.add(EventCategory.objects.get(slug="film"))
                    elif event_cat_id == 111:
                        event.categories.add(EventCategory.objects.get(slug="konzert"))
                    elif event_cat_id in (48, 201, 223):
                        event.categories.add(EventCategory.objects.get(slug="tagung"))
                    elif event_cat_id in (138, 139, 221):
                        event.categories.add(EventCategory.objects.get(slug="theaterperformance"))
                    elif event_cat_id in (49, 169, 213):
                        event.categories.add(EventCategory.objects.get(slug="vortraglesunggesprach"))
                    elif event_cat_id in (110, 214, 222):
                        event.categories.add(EventCategory.objects.get(slug="sonstiges"))

                event.organizer_set.all().delete()
                linked_institutions = data_dict.get('linked_institutions', {})
                if linked_institutions:
                    for linked_inst_smb_id in linked_institutions.keys():
                        try:
                            organizing_museum = Museum.objects.get(pk=self.LINKED_INSTITUTION_MAPPER.get(int(linked_inst_smb_id), None))
                        except:
                            Organizer(
                                event=event,
                                organizer_title=linked_institutions[linked_inst_smb_id],
                            ).save()
                        else:
                            Organizer(
                                event=event,
                                organizing_museum=organizing_museum,
                            ).save()

                if event.exhibition and not event.mediafile_set.count():
                    MediaFile = models.get_model("events", "MediaFile")

                    for exh_mf in event.exhibition.mediafile_set.all():
                        mf = MediaFile(event=event)
                        filename = exh_mf.path.filename
                        try:
                            image_data = open(settings.MEDIA_ROOT + "/" + exh_mf.path.path, "rb")
                        except IOError:
                            continue
                        image_mods.FileManager.save_file_for_object(
                            mf,
                            filename,
                            image_data.read(),
                            field_name="path",
                            subpath="events/%s/gallery/" % event.slug,
                        )
                        image_data.close()
                        mf.save()
                        exh_file_descriptions = FileDescription.objects.filter(
                            file_path=exh_mf.path,
                        ).order_by("pk")
                        if exh_file_descriptions:
                            try:
                                file_description = FileDescription.objects.filter(
                                    file_path=mf.path,
                                ).order_by("pk")[0]
                            except:
                                file_description = FileDescription(file_path=mf.path)

                            file_description.title_de = exh_file_descriptions[0].title_de
                            file_description.title_en = exh_file_descriptions[0].title_en
                            file_description.author = exh_file_descriptions[0].author
                            file_description.save()
                        time.sleep(1)

                event.eventtime_set.all().delete()

                start = parse_datetime(data_dict['start'], ignoretz=True)
                if data_dict['end']:
                    end = parse_datetime(data_dict['end'], ignoretz=True)
                else:
                    end = start + timedelta(minutes=60)

                event_time = EventTime(
                    event=event,
                    event_date=start.date(),
                    start=start.time(),
                    end=end.time(),
                )
                event_time.save()

                for event_time_id, event_time_dict in data_dict.get('more_dates', {}).items():
                    start = parse_datetime(event_time_dict['start'], ignoretz=True)
                    if event_time_dict['end']:
                        end = parse_datetime(event_time_dict['end'], ignoretz=True)
                    else:
                        end = start + timedelta(minutes=60)

                    event_time = EventTime(
                        event=event,
                        event_date=start.date(),
                        start=start.time(),
                        end=end.time(),
                    )
                    event_time.save()

                event.update_closest_event_time()

                if not mapper:
                    mapper = ObjectMapper(
                        service=s_events,
                        external_id=external_id,
                    )
                    mapper.content_object = event
                    mapper.save()
                    if verbosity > 1:
                        event_stats['added'] += 1
                else:
                    if verbosity > 1:
                        event_stats['updated'] += 1
        if verbosity > 1:
            print u"Events added: %d" % event_stats['added']
            print u"Events updated: %d" % event_stats['updated']
            print u"Events skipped: %d" % event_stats['skipped']
            print
            print u"Workshops added: %d" % workshop_stats['added']
            print u"Workshops updated: %d" % workshop_stats['updated']
            print u"Workshops skipped: %d" % workshop_stats['skipped']
            print

