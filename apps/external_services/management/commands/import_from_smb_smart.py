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
    
    def handle_noargs(self, **options):
        self.import_exhibitions(**options)
        
    def import_exhibitions(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        skip_images = options.get('skip_images')
        
        weekdays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

        import time
        import urllib2
        from datetime import datetime
        from datetime import timedelta
        from dateutil.parser import parse as parse_datetime
        
        from django.db import models
        from django.template.defaultfilters import slugify
        from django.conf import settings
        import json

        from filebrowser.models import FileDescription
        
        image_mods = models.get_app("image_mods")
        Museum = models.get_model("museums", "Museum")
        Exhibition = models.get_model("exhibitions", "Exhibition")
        Organizer = models.get_model("exhibitions", "Organizer")
        MediaFile = models.get_model("exhibitions", "MediaFile")
        Season = models.get_model("exhibitions", "Season")
        Event = models.get_model("events", "Event")
        EventTime = models.get_model("events", "EventTime")
        Workshop = models.get_model("workshops", "Workshop")
        WorkshopTime = models.get_model("workshops", "WorkshopTime")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Service = models.get_model("external_services", "Service")
        
        def parse_unix_timestamp(timestamp):
            return datetime.fromtimestamp(int(timestamp))

        MUSEUM_MAPPER = {
            43009: 62,
            43010: 129,
            43011: 130,
            31: 150,
            35: 77,
            37: 105,
            39: 107,
            40: 103,
            24: 9,
            25: 152,
            27: 157,
            28: 35,
            29: 8,
            32: 67,
            26: 177,
            30: 84,
            43: 79,
            48: 0,  # Institut für Museumsforschung
            2433: 0,  # Rathgen-Forschungslabor
            27774: 0,  # Zentralarchiv
            37096: 0,  # Archäologisches Zentrum
            43007: 0,  # Humboldt-Forum
            43008: 0,  # Generaldirektion
            45: 166,
            2976: 124,
            6124: 131,
        }

        ### IMPORT EXHIBITIONS ###
        if verbosity > 1:
            print u"### IMPORTING EXHIBITIONS ###"
        s_exhibitions, created = Service.objects.get_or_create(
            sysname="smb_exhibitions_smart",
            defaults={
                'url': "http://www.smb.museum/smb/export/getExhibitionListFromSMart.php?format=json",
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

            museum = None
            museum_guid = int(exhibition_dict['location']['SMart_id'])
            try:
                museum = Museum.objects.get(pk=MUSEUM_MAPPER[museum_guid])
            except:
                pass

            response = urllib2.urlopen("http://www.smb.museum/smb/export/getExhibitionFromSMart.php?format=json&SMart_id=%s" % external_id)
            data = response.read()
            response.close()
            data_dict = json.loads(data)

            if data_dict['status'] != "www":
                stats['skipped'] += 1
                continue

            exhibition.title_de = data_dict['title_de']
            exhibition.title_en = data_dict['title_en']
            exhibition.subtitle_de = data_dict['subtitle_de']
            exhibition.subtitle_en = data_dict['subtitle_en']
            exhibition.slug = slugify(data_dict['title_de'])
            exhibition.start = parse_datetime(data_dict['start_date'])
            if data_dict['perma_exhibition']:
                exhibition.permanent = True
            else:
                if data_dict['end_date'] != "unlimited":
                    exhibition.end = parse_datetime(data_dict['end_date'])
            # exhibition.website_de = data_dict['web_link_de'].replace('&amp;', '&')
            # exhibition.website_en = data_dict['web_link_en'].replace('&amp;', '&')
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
            
            # exhibition.free_entrance = bool(data_dict['generell_frei'])
            # if data_dict['preis_voll']:
            #     exhibition.admission_price = int(data_dict['preis_voll'])
            # if exhibition_dict['preis_erm']:
            #     exhibition.reduced_price = int(data_dict['preis_erm'])

            # exhibition.admission_price_info_de = """<p><a href="%s">Weitere Preisinformationen</a></p>""" % exhibition.website_de
            # exhibition.admission_price_info_de_markup_type = "hw"
            # exhibition.admission_price_info_en = """<p><a href="%s">More price information</a></p>""" % exhibition.website_en
            # exhibition.admission_price_info_en_markup_type = "hw"
            
            exhibition.status = "import"
            exhibition.save()
            
            # if exhibition_dict['organizers']:
            #     for organizer_id, organizer_title in exhibition_dict['organizers'].items():
            #         try:
            #             # get museum by title
            #             organizing_museum = Museum.objects.get(
            #                 title_de=organizer_title,
            #             )
            #         except:
            #             # save non-existing museum title as organizer title
            #             o = Organizer(exhibition=exhibition, organizer_title=organizer_title)
            #             o.save()
            #         else:
            #             if exhibition.museum != organizing_museum:
            #                 # save organizing museum for museum by title
            #                 o = Organizer(exhibition=exhibition, organizing_museum=organizing_museum)
            #                 o.save()
            
            if data_dict['opening_times']:
                season = Season(exhibition=exhibition)
                for day_index, times in data_dict['opening_times'].items():
                    from_time, till_time = times.split("-")
                    setattr(season, "%s_open" % weekdays[int(day_index)], parse_datetime(from_time).time())
                    setattr(season, "%s_close" % weekdays[int(day_index)], parse_datetime(till_time).time())
                season.save()


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
                    
                    file_description.description_de = image_dict['description_de']
                    file_description.description_en = image_dict['description_en']
                    file_description.copyright_limitations = image_dict['copyright_de']
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
        
        ### IMPORT EVENTS ###
        if verbosity > 1:
            print u"### IMPORTING EVENTS AND WORKSHOPS ###"
        
        s_events, created = Service.objects.get_or_create(
            sysname="smb_events_smart",
            defaults={
                'url': "http://www.smb.museum/smb/export/getEventListFromSMart.php?format=json",
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

            if event_dict['event_type_en'] == "guided tour":

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

                museum = None
                museum_guid = int(event_dict['location']['SMart_id'])
                try:
                    museum = Museum.objects.get(pk=MUSEUM_MAPPER[museum_guid])
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

                response = urllib2.urlopen("http://www.smb.museum/smb/export/getEventFromSMartByTerminId.php?format=json&SMarttermin_id=%s" % event_dict['dates'].keys()[0])
                data = response.read()
                response.close()
                data_dict = json.loads(data)

                if data_dict['status'] != "www":
                    workshop_stats['skipped'] += 1
                    continue

                workshop.title_de = data_dict['title_de']
                workshop.title_en = data_dict['title_en']
                workshop.slug = slugify(data_dict['title_de'])

                # event.website_de = data_dict['web_link_de'].replace('&amp;', '&')
                # event.website_en = data_dict['web_link_en'].replace('&amp;', '&')
                workshop.description_de = data_dict['description_de']
                workshop.description_de_markup_type = "hw"
                workshop.description_en = data_dict['description_en']
                workshop.description_en_markup_type = "hw"
                workshop.press_text_de = data_dict['description_de']
                workshop.press_text_de_markup_type = "hw"
                workshop.press_text_en = data_dict['description_en']
                workshop.press_text_en_markup_type = "hw"
                workshop.admission_price_info_de = data_dict['kosten_de']
                workshop.admission_price_info_de_markup_type = "hw"
                workshop.admission_price_info_en = data_dict['kosten_en']
                workshop.admission_price_info_en_markup_type = "hw"
                workshop.meeting_place_de = data_dict['treffpunkt_de']
                workshop.meeting_place_en = data_dict['treffpunkt_en']
                workshop.booking_info_de = data_dict['registration_de']
                workshop.booking_info_de_markup_type = "hw"
                workshop.booking_info_en = data_dict['registration_en']
                workshop.booking_info_en_markup_type = "hw"

                workshop.museum = museum

                exhibition_ids = data_dict.get('linked_exhibitions', {}).keys()
                if exhibition_ids:
                    try:
                        # get exhibition from saved mapper
                        exh_mapper = s_exhibitions.objectmapper_set.get(
                            external_id=exhibition_ids[0],
                            content_type__app_label="exhibitions",
                            content_type__model="exhibition",
                        )
                    except models.ObjectDoesNotExist:
                        pass
                    else:
                        workshop.exhibition = exh_mapper.content_object

                workshop.status = "import"
                workshop.save()

                if workshop.exhibition and not workshop.mediafile_set.count():
                    MediaFile = models.get_model("workshops", "MediaFile")

                    for exh_mf in workshop.exhibition.mediafile_set.all():
                        mf = MediaFile(workshop=workshop)
                        filename = exh_mf.path.filename
                        image_data = open(settings.MEDIA_ROOT + "/" + exh_mf.path.path, "rb")
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
                            file_path=mf.path,
                        ).order_by("pk")
                        if exh_file_descriptions:
                            try:
                                file_description = FileDescription.objects.filter(
                                    file_path=mf.path,
                                ).order_by("pk")[0]
                            except:
                                file_description = FileDescription(file_path=mf.path)

                            file_description.description_de = exh_file_descriptions[0].description_de
                            file_description.description_en = exh_file_descriptions[0].description_en
                            file_description.copyright_limitations = exh_file_descriptions[0].copyright_limitations
                            file_description.save()
                            time.sleep(1)

                workshop.workshoptime_set.all().delete()

                start = parse_datetime(data_dict['start'], ignoretz=True)
                if data_dict['end']:
                    end = parse_datetime(data_dict['end'], ignoretz=True)
                else:
                    end = start + timedelta(minutes=60)

                time = WorkshopTime(
                    workshop=workshop,
                    workshop_date=start.date(),
                    start=start.time(),
                    end=end.time(),
                )
                time.save()

                for event_time_id, event_time_dict in data_dict.get('more_dates', {}).items():
                    start = parse_datetime(event_time_dict['start'], ignoretz=True)
                    if event_time_dict['end']:
                        end = parse_datetime(event_time_dict['end'], ignoretz=True)
                    else:
                        end = start + timedelta(minutes=60)

                    time = WorkshopTime(
                        workshop=workshop,
                        workshop_date=start.date(),
                        start=start.time(),
                        end=end.time(),
                    )
                    time.save()

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

                museum = None
                museum_guid = int(event_dict['location']['SMart_id'])
                try:
                    museum = Museum.objects.get(pk=MUSEUM_MAPPER[museum_guid])
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

                response = urllib2.urlopen("http://www.smb.museum/smb/export/getEventFromSMartByTerminId.php?format=json&SMarttermin_id=%s" % event_dict['dates'].keys()[0])
                data = response.read()
                response.close()
                data_dict = json.loads(data)

                if data_dict['status'] != "www":
                    event_stats['skipped'] += 1
                    continue

                event.title_de = data_dict['title_de']
                event.title_en = data_dict['title_en']
                event.slug = slugify(data_dict['title_de'])

                # event.website_de = data_dict['web_link_de'].replace('&amp;', '&')
                # event.website_en = data_dict['web_link_en'].replace('&amp;', '&')
                event.description_de = data_dict['description_de']
                event.description_de_markup_type = "hw"
                event.description_en = data_dict['description_en']
                event.description_en_markup_type = "hw"
                event.press_text_de = data_dict['description_de']
                event.press_text_de_markup_type = "hw"
                event.press_text_en = data_dict['description_en']
                event.press_text_en_markup_type = "hw"
                event.admission_price_info_de = data_dict['kosten_de']
                event.admission_price_info_de_markup_type = "hw"
                event.admission_price_info_en = data_dict['kosten_en']
                event.admission_price_info_en_markup_type = "hw"
                event.meeting_place_de = data_dict['treffpunkt_de']
                event.meeting_place_en = data_dict['treffpunkt_en']
                event.booking_info_de = data_dict['registration_de']
                event.booking_info_de_markup_type = "hw"
                event.booking_info_en = data_dict['registration_en']
                event.booking_info_en_markup_type = "hw"

                event.museum = museum

                exhibition_ids = data_dict.get('linked_exhibitions', {}).keys()
                if exhibition_ids:
                    try:
                        # get exhibition from saved mapper
                        exh_mapper = s_exhibitions.objectmapper_set.get(
                            external_id=exhibition_ids[0],
                            content_type__app_label="exhibitions",
                            content_type__model="exhibition",
                        )
                    except models.ObjectDoesNotExist:
                        pass
                    else:
                        event.exhibition = exh_mapper.content_object

                event.status = "import"
                event.save()

                if event.exhibition and not event.mediafile_set.count():
                    MediaFile = models.get_model("events", "MediaFile")

                    for exh_mf in event.exhibition.mediafile_set.all():
                        mf = MediaFile(event=event)
                        filename = exh_mf.path.filename
                        image_data = open(settings.MEDIA_ROOT + "/" + exh_mf.path.path, "rb")
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
                            file_path=mf.path,
                        ).order_by("pk")
                        if exh_file_descriptions:
                            try:
                                file_description = FileDescription.objects.filter(
                                    file_path=mf.path,
                                ).order_by("pk")[0]
                            except:
                                file_description = FileDescription(file_path=mf.path)

                            file_description.description_de = exh_file_descriptions[0].description_de
                            file_description.description_en = exh_file_descriptions[0].description_en
                            file_description.copyright_limitations = exh_file_descriptions[0].copyright_limitations
                            file_description.save()
                            time.sleep(1)

                event.eventtime_set.all().delete()

                start = parse_datetime(data_dict['start'], ignoretz=True)
                if data_dict['end']:
                    end = parse_datetime(data_dict['end'], ignoretz=True)
                else:
                    end = start + timedelta(minutes=60)

                time = EventTime(
                    event=event,
                    event_date=start.date(),
                    start=start.time(),
                    end=end.time(),
                )
                time.save()

                for event_time_id, event_time_dict in data_dict.get('more_dates', {}).items():
                    start = parse_datetime(event_time_dict['start'], ignoretz=True)
                    if event_time_dict['end']:
                        end = parse_datetime(event_time_dict['end'], ignoretz=True)
                    else:
                        end = start + timedelta(minutes=60)

                    time = EventTime(
                        event=event,
                        event_date=start.date(),
                        start=start.time(),
                        end=end.time(),
                    )
                    time.save()

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

