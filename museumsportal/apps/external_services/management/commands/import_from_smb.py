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
        
        import re
        import urllib2
        import json
        from datetime import datetime
        from datetime import timedelta
        from time import strptime
        from rest.client import webcall
        from dateutil.parser import parse as parse_datetime
        
        from django.db import models
        from django.template.defaultfilters import slugify

        from filebrowser.models import FileDescription
        
        from base_libs.utils.misc import get_related_queryset
        
        image_mods = models.get_app("image_mods")
        Museum = models.get_model("museums", "Museum")
        Exhibition = models.get_model("exhibitions", "Exhibition")
        Organizer = models.get_model("exhibitions", "Organizer")
        MediaFile = models.get_model("exhibitions", "MediaFile")
        Season = models.get_model("exhibitions", "Season")
        Event = models.get_model("events", "Event")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Service = models.get_model("external_services", "Service")
        
        def parse_unix_timestamp(timestamp):
            return datetime.fromtimestamp(int(timestamp))

        ### IMPORT EXHIBITIONS ###
        if verbosity > 1:
            print u"### IMPORTING EXHIBITIONS ###"
        s_exhibitions, created = Service.objects.get_or_create(
            sysname="smb_exhibitions",
            defaults={
                'url': "http://www.smb.museum/smb/export/export_exhibition_list.php?format=json",
                'title': "Staatliche Museen zu Berlin Exhibitions",
                },
            )
        response = urllib2.urlopen(s_exhibitions.url)
        data = response.read()
        response.close()
        
        data_dict = json.loads(data)

        stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
            }
        for external_id, exhibition_dict in data_dict.items():

            museum = None
            museum_guid, museum_title = exhibition_dict['location'].items()[0]
            try:
                # get museum from saved mapper
                museum = s_exhibitions.objectmapper_set.get(
                    external_id=museum_guid,
                    content_type__app_label="museums",
                    content_type__model="museum",
                    ).content_object
            except models.ObjectDoesNotExist:
                try:
                    # get museum by title
                    museum = Museum.objects.get(
                        title_de=museum_title,
                        )
                except:
                    # save non-existing museum title as location name
                    pass
                else:
                    # save museum mapper for museum by title
                    museum_mapper = ObjectMapper(
                        service=s_exhibitions,
                        external_id=museum_guid,
                        )
                    museum_mapper.content_object = museum
                    museum_mapper.save()
            
            mapper = None
            try:
                # get event from saved mapper
                mapper = s_exhibitions.objectmapper_set.get(
                    external_id=external_id,
                    content_type__app_label="exhibitions",
                    content_type__model="exhibition",
                    )
                stats['skipped'] += 1
                continue
            except models.ObjectDoesNotExist:
                # or create a new article and then create a mapper
                exhibition = Exhibition()
            else:
                exhibition = mapper.content_object
                if not exhibition:
                    # if exhibition was deleted after import,
                    # don't import it again
                    stats['skipped'] += 1
                    continue

            exhibition.title_de = exhibition_dict['name_de']
            exhibition.title_en = exhibition_dict['name_en']
            exhibition.slug = slugify(exhibition_dict['name_de'])
            exhibition.start = parse_datetime(exhibition_dict['start'])
            if exhibition_dict['dauerausstellung']:
                exhibition.permanent = True
            else:
                exhibition.end = parse_datetime(exhibition_dict['end'])
            exhibition.website_de = exhibition_dict['web_link_de'].replace('&amp;', '&')
            exhibition.website_en = exhibition_dict['web_link_en'].replace('&amp;', '&')
            exhibition.description_de = exhibition_dict['description_de']
            exhibition.description_de_markup_type = "hw"
            exhibition.description_en = exhibition_dict['description_en']
            exhibition.description_en_markup_type = "hw"
            exhibition.press_text_de = exhibition_dict['description_de']
            exhibition.press_text_de_markup_type = "hw"
            exhibition.press_text_en = exhibition_dict['description_en']
            exhibition.press_text_en_markup_type = "hw"
            exhibition.status = "import"
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
                exhibition.location_name = museum_title
                
            exhibition.museum_opening_hours = exhibition_dict['opening_from_museum']
            
            exhibition.free_entrance = bool(exhibition_dict['generell_frei'])
            if exhibition_dict['preis_voll']:
                exhibition.admission_price = int(exhibition_dict['preis_voll'])
            if exhibition_dict['preis_erm']:
                exhibition.reduced_price = int(exhibition_dict['preis_erm'])
            exhibition.admission_price_info_de = """<p><a href="%s">Weitere Preisinformationen</a></p>""" % exhibition.website_de
            exhibition.admission_price_info_de_markup_type = "hw"
            exhibition.admission_price_info_en = """<p><a href="%s">More price information</a></p>""" % exhibition.website_en
            exhibition.admission_price_info_en_markup_type = "hw"
            
            exhibition.save()
            
            if exhibition_dict['organizers']:
                for organizer_id, organizer_title in exhibition_dict['organizers'].items():
                    try:
                        # get museum by title
                        organizing_museum = Museum.objects.get(
                            title_de=organizer_title,
                            )
                    except:
                        # save non-existing museum title as organizer title
                        o = Organizer(exhibition=exhibition, organizer_title=organizer_title)
                        o.save()
                    else:
                        if exhibition.museum != organizing_museum:
                            # save organizing museum for museum by title
                            o = Organizer(exhibition=exhibition, organizing_museum=organizing_museum)
                            o.save()
            
            if exhibition_dict['opening_times']:
                season = Season(exhibition=exhibition)
                for day_index, times in exhibition_dict['opening_times'].items():
                    from_time, till_time = times.split("-")
                    setattr(season, "%s_open" % weekdays[int(day_index)], parse_datetime(from_time).time())
                    setattr(season, "%s_close" % weekdays[int(day_index)], parse_datetime(till_time).time())
                season.save()
            
            if exhibition_dict['image_path']:
                image_url = exhibition_dict['image_path']
                if image_url and not skip_images:
                    mf = MediaFile(exhibition=exhibition)
                    filename = image_url.split("/")[-1]
                    image_data = urllib2.urlopen(image_url)
                    image_mods.FileManager.save_file_for_object(
                        mf,
                        filename,
                        image_data.read(),
                        field_name="path",
                        subpath = "exhibitions/%s/gallery/" % exhibition.slug,
                        )
                    mf.save()
                    try:
                        file_description = FileDescription.objects.filter(
                            file_path=mf.path,
                            ).order_by("pk")[0]
                    except:
                        file_description = FileDescription(file_path=mf.path)
                    
                    file_description.description_de = exhibition_dict['image_de'].replace('&amp;#169;', u'©')
                    file_description.description_en = exhibition_dict['image_en'].replace('&amp;#169;', u'©')
                    file_description.save()
            
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
        
        return # DEBUG
        
        ### IMPORT EVENTS ###
        if verbosity > 1:
            print u"### IMPORTING EVENTS ###"
        
        s_events, created = Service.objects.get_or_create(
            sysname="smb_events",
            defaults={
                'url': "http://www.smb.museum/smb/export/export_event_list.php?format=json",
                'title': "Staatliche Museen zu Berlin Events",
                },
            )
        
        @webcall(url=s_events.url)
        def get_events_data():
            pass

        data = get_events_data()
        
        data_dict = json.loads(data)

        stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
            }
            
        for external_id, event_dict in data_dict.items():

            museum_guid = museum_node.getAttribute("id")
            try:
                # get museum from saved mapper
                inst = s_museums.objectmapper_set.get(
                    external_id=museum_guid,
                    content_type__app_label="institutions",
                    content_type__model="institution",
                    ).content_object
            except models.ObjectDoesNotExist:
                # don't import events of unknown museums
                continue

            if not inst:
                continue
                
            inst_contact = inst.get_primary_contact()
            
            change_date = parse_datetime(
                get_value(node_event, "dtstamp"),
                ignoretz=True,
                )

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
                    continue
                if event.modified_date and event.modified_date > change_date or event.creation_date > change_date:
                    if verbosity > 1:
                        print u" > %s (pk=%s, uid=%s) skipped" % (event, event.pk, external_id)
                        stats['skipped'] += 1
                    continue

            event.status = status_imported
            event.venue = inst
            event.organizing_institution = inst
            event.save()
            
            event.creative_sectors.add(cs_art)

            event.eventtime_set.all().delete()
            
            for node_date in node_event.getElementsByTagName("date"):
                start = parse_datetime(
                    get_value(node_date, "start"),
                    ignoretz=True,
                    )
                end = start + timedelta(minutes=int(get_value(node_date, "minutes")))
                
                time = EventTime(
                    event=event,
                    start_yyyy=start.year,
                    start_mm=start.month,
                    start_dd=start.day,
                    start_hh=start.hour,
                    start_ii=start.minute,
                    end_yyyy=end.year,
                    end_mm=end.month,
                    end_dd=end.day,
                    end_hh=end.hour,
                    end_ii=end.minute,
                    is_all_day=False,
                    )
                time.save()
            
            event.related_events.clear()
            exhibition_node = get_first(node_event, "exhibition")
            if exhibition_node:
                exhibition_id = exhibition_node.getAttribute("id")
                try:
                    # get event from saved mapper
                    exh_mapper = s_exhibitions.objectmapper_set.get(
                        external_id=exhibition_id,
                        content_type__app_label="events",
                        content_type__model="event",
                        )
                except models.ObjectDoesNotExist:
                    pass
                else:
                    event.related_events.add(exh_mapper.content_object)
                
            if not mapper:
                mapper = ObjectMapper(
                    service=s_events,
                    external_id=external_id,
                    )
                mapper.content_object = event
                mapper.save()
                if verbosity > 1:
                    print u" > %s (pk=%s, uid=%s) added" % (event, event.pk, external_id)
                    stats['added'] += 1
            else:
                if verbosity > 1:
                    print u" > %s (pk=%s, uid=%s) updated" % (event, event.pk, external_id)
                    stats['updated'] += 1

        if verbosity > 1:
            print u"Events added: %d" % stats['added']
            print u"Events updated: %d" % stats['updated']
            print u"Events skipped: %d" % stats['skipped']
            print

