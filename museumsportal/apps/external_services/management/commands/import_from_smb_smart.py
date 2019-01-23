# -*- coding: UTF-8 -*-
from optparse import make_option
from django.core.management.base import NoArgsCommand

from base_libs.utils.misc import strip_html

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells the script NOT to download images.'),
        make_option('--update-all', action='store_true', dest='update_all', default=False,
            help='Tells the script to update all information no matter the last modification date.'),
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
        33568: 219,     # Humboldt-Box
        34: 0,          # Kulturforum
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
    DEFAULT_EXHIBITION_STATUS = 'published'
    DEFAULT_EVENT_STATUS = 'published'
    DEFAULT_WORKSHOP_STATUS = 'published'

    def handle_noargs(self, **options):
        self.verbosity = int(options.get('verbosity', NORMAL))
        self.skip_images = options.get('skip_images')
        self.update_all = options.get('update_all')

        self.initialize()
        self.import_exhibitions()
        self.import_events_and_workshops()
        self.finalize()

    def initialize(self):
        from django.db import models
        Service = models.get_model("external_services", "Service")

        URL_EXHIBITIONS = "https://smart.smb.museum/export/getExhibitionListFromSMart.php?format=json"
        self.service_exhibitions, created = Service.objects.get_or_create(
            sysname="smb_exhibitions_smart",
            defaults={
                'url': URL_EXHIBITIONS,
                'title': "SMB - Exhibitions SMart",
            },
        )
        if self.service_exhibitions.url != URL_EXHIBITIONS:
            self.service_exhibitions.url = URL_EXHIBITIONS
            self.service_exhibitions.save()
        self.URL_EXHIBITION = "https://smart.smb.museum/export/getExhibitionFromSMart.php?format=json&SMart_id={}"

        URL_EVENTS = "https://smart.smb.museum/export/getEventListFromSMart.php?format=json"
        self.service_events, created = Service.objects.get_or_create(
            sysname="smb_events_smart",
            defaults={
                'url': URL_EVENTS,
                'title': "SMB - Events SMart",
            },
        )
        if self.service_events.url != URL_EVENTS:
            self.service_events.url = URL_EVENTS
            self.service_events.save()
        self.URL_EVENT = "https://smart.smb.museum/export/getEventFromSMartByTerminId.php?format=json&SMarttermin_id={}"

        self.stats = {
            'exhibitions_added': 0,
            'exhibitions_updated': 0,
            'exhibitions_skipped': 0,

            'events_added': 0,
            'events_updated': 0,
            'events_skipped': 0,

            'workshops_added': 0,
            'workshops_updated': 0,
            'workshops_skipped': 0,
        }

    def import_exhibitions(self):
        from datetime import datetime
        weekdays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

        import requests
        from datetime import datetime, timedelta
        from dateutil.parser import parse as parse_datetime
        from decimal import Decimal
        
        from django.db import models
        from base_libs.utils.betterslugify import better_slugify

        from base_libs.utils.misc import get_unique_value

        image_mods = models.get_app("image_mods")
        Museum = models.get_model("museums", "Museum")
        Exhibition = models.get_model("exhibitions", "Exhibition")
        ExhibitionCategory = models.get_model("exhibitions", "ExhibitionCategory")
        Organizer = models.get_model("exhibitions", "Organizer")
        MediaFile = models.get_model("exhibitions", "MediaFile")
        Season = models.get_model("exhibitions", "Season")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")

        ### IMPORT EXHIBITIONS ###
        if self.verbosity > 1:
            self.stdout.write("### IMPORTING EXHIBITIONS ###\n")
            self.stdout.flush()

        response = requests.get(self.service_exhibitions.url)
        if response.status_code != requests.codes.OK:
            self.stderr.write(u"Error status {} when trying to access {}\n".format(response.status_code, self.service_exhibitions.url))
            return

        list_data_dict = response.json()

        for external_id, exhibition_dict in list_data_dict.items():

            if self.verbosity > 1:
                self.stdout.write(u"- {} (id={})\n".format(exhibition_dict['title_de'], external_id))
                self.stdout.flush()

            # get or create exhibition
            mapper = None
            try:
                # get exhibition from saved mapper
                mapper = self.service_exhibitions.objectmapper_set.get(
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
                    self.stats['exhibitions_skipped'] += 1
                    continue
                else:
                    if not self.update_all:
                        if parse_datetime(exhibition_dict['lastaction'], ignoretz=True) < datetime.now() - timedelta(days=1):
                            self.stats['exhibitions_skipped'] += 1
                            continue

            museum = None
            museum_guid = int(exhibition_dict['location'].get('SMart_id', 0))
            try:
                museum = Museum.objects.get(pk=self.MUSEUM_MAPPER.get(museum_guid, 0))
            except Museum.DoesNotExist:
                pass

            url = self.URL_EXHIBITION.format(external_id)
            response = requests.get(url)
            if response.status_code != requests.codes.OK:
                self.stderr.write(
                    u"Error status {} when trying to access {}\n".format(response.status_code, url))
                continue

            data_dict = response.json()

            if data_dict['status_text'] != "www":
                self.stats['exhibitions_skipped'] += 1
                continue

            exhibition.title_de = data_dict['title_de']
            exhibition.title_en = data_dict['title_en'] or data_dict['title_de']
            exhibition.subtitle_de = data_dict['subtitle_de']
            exhibition.subtitle_en = data_dict['subtitle_en']

            exhibition.slug = get_unique_value(Exhibition, better_slugify(data_dict['title_de'], remove_stopwords=False), instance_pk=exhibition.pk)

            if data_dict['start_date']:
                exhibition.start = parse_datetime(data_dict['start_date'])
            else:
                exhibition.start = datetime.today()
            if data_dict['perma_exhibition'] == 1 or data_dict['end_date'] == "unlimited":
                exhibition.permanent = True
                exhibition.museum_prices = True
            else:
                exhibition.end = parse_datetime(data_dict['end_date'])
            exhibition.website_de = data_dict['link_de'].replace('&amp;', '&')
            exhibition.website_en = data_dict['link_en'].replace('&amp;', '&')
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

            if exhibition.status not in ("published", "trashed", "not_listed"):
                exhibition.status = self.DEFAULT_EXHIBITION_STATUS
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
                season.exceptions_de = data_dict.get('opening_info_de', '')
                season.exceptions_en = data_dict.get('opening_info_en', '')
                season.exceptions_de_markup_type = 'pt'
                season.exceptions_en_markup_type = 'pt'
                season.save()
            else:
                Season.objects.filter(exhibition=exhibition).delete()

            if not self.skip_images:
                # get biggest possible images
                image_ids_to_keep = []
                # the image versions are saved as img_teaser_<id> or img_<id>
                images_keys = [key for key in data_dict.keys() if key.startswith("img_")]
                img_teaser = []
                if images_keys:
                    img_teaser = data_dict[images_keys[-1]]  # take the last size
                for image_dict in img_teaser:
                    image_url = image_dict.get('path_xl') or image_dict.get('path')

                    image_external_id = "exh-{}-{}".format(exhibition.pk, image_url)
                    image_mapper = None
                    try:
                        # get image model instance from saved mapper
                        image_mapper = self.service_exhibitions.objectmapper_set.get(
                            external_id=image_external_id,
                            content_type__app_label="exhibitions",
                            content_type__model="mediafile",
                        )
                    except models.ObjectDoesNotExist:
                        # or create a new exhibition and then create a mapper
                        mf = MediaFile(exhibition=exhibition)
                    else:
                        mf = image_mapper.content_object
                        if mf:
                            image_ids_to_keep.append(mf.pk)
                            file_description = self.save_file_description(mf.path, image_dict)
                        else:
                            if self.update_all:
                                # restore image
                                mf = MediaFile(exhibition=exhibition)
                            else:
                                # skip deleted images
                                continue
                        if not self.update_all:
                            continue

                    filename = image_url.split("/")[-1]
                    image_response = requests.get(image_url)
                    if image_response.status_code != requests.codes.OK:
                        self.stderr.write(
                            u"Error status {} when trying to access {}\n".format(
                                image_response.status_code,
                                image_url,
                            )
                        )
                        continue
                    image_mods.FileManager.delete_file_for_object(
                        mf,
                        field_name="path",
                    )
                    image_mods.FileManager.save_file_for_object(
                        mf,
                        filename,
                        image_response.content,
                        field_name="path",
                        subpath="exhibitions/%s/gallery/" % exhibition.slug,
                    )
                    mf.save()
                    image_ids_to_keep.append(mf.pk)

                    file_description = self.save_file_description(mf.path, image_dict)

                    if not image_mapper:
                        image_mapper = ObjectMapper(
                            service=self.service_exhibitions,
                            external_id=image_external_id,
                        )
                    image_mapper.content_object = mf
                    image_mapper.save()

                for mf in exhibition.mediafile_set.exclude(id__in=image_ids_to_keep):
                    if mf.path:
                        # remove the file from the file system
                        image_mods.FileManager.delete_file(mf.path.name)
                    # delete image mapper
                    self.service_exhibitions.objectmapper_set.filter(
                        object_id=mf.pk,
                        content_type__app_label="exhibitions",
                        content_type__model="mediafile",
                    ).delete()
                    # delete image model instance
                    mf.delete()

                sort_order = 0
                for mf in exhibition.mediafile_set.all():
                    exhibition.mediafile_set.filter(pk=mf.pk).update(sort_order=sort_order)
                    sort_order += 1


            if not mapper:
                mapper = ObjectMapper(
                    service=self.service_exhibitions,
                    external_id=external_id,
                )
                mapper.content_object = exhibition
                mapper.save()
                self.stats['exhibitions_added'] += 1
            else:
                self.stats['exhibitions_updated'] += 1

        if self.verbosity > 1:
            self.stdout.write("\n")
            self.stdout.flush()

    def save_file_description(self, path, d):
        from filebrowser.models import FileDescription
        try:
            file_description = FileDescription.objects.filter(
                file_path=path,
            ).order_by("pk")[0]
        except IndexError:
            file_description = FileDescription(file_path=path)

        title = d['description_de']
        if len(title) > 300:
            title = title[:299] + u'…'
        file_description.title_de = title

        title = d['description_de']
        if len(title) > 300:
            title = title[:299] + u'…'
        file_description.title_en = title

        file_description.author = Command.prefix_with_c(d['copyright_de'])
        file_description.save()
        return file_description

    @staticmethod
    def parse_title_and_subtitle(text):
        lines = [line.strip() for line in text.split("<br />") if line.strip()]
        if not lines:
            return u"", u""
        # if there is just one line, the subtitle will be empty
        # if there are more than 2 lines, the 2nd line will be connected to the rest for the subtitle
        return lines[0], u" ".join(lines[1:])

    @staticmethod
    def prefix_with_c(text):
        if text and not text.startswith(u'©'):
            text = u'© {}'.format(text)
        return text

    def cleanup_html(self, text):
        import re
        text = re.sub(r'<br ?/?>\s+', '. ', text)
        text = text.replace("&ndash;", "-")
        text = text.replace("&bdquo;", '"')
        text = text.replace("&ldquo;", '"')
        return text

    def save_workshop(self, external_id, data_dict):
        import requests
        from datetime import datetime, timedelta
        from dateutil.parser import parse as parse_datetime
        from decimal import Decimal

        from django.db import models
        from django.conf import settings

        from base_libs.utils.betterslugify import better_slugify
        from base_libs.utils.misc import strip_html
        from base_libs.utils.misc import get_unique_value

        from filebrowser.models import FileDescription

        image_mods = models.get_app("image_mods")
        Museum = models.get_model("museums", "Museum")
        Workshop = models.get_model("workshops", "Workshop")
        WorkshopType = models.get_model("workshops", "WorkshopType")
        WorkshopTime = models.get_model("workshops", "WorkshopTime")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Organizer = models.get_model("workshops", "Organizer")
        MediaFile = models.get_model("workshops", "MediaFile")

        # get or create event
        mapper = None
        try:
            # get workshop from saved mapper
            mapper = self.service_events.objectmapper_set.get(
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
                self.stats['workshops_skipped'] += 1
                return
            else:
                if not self.update_all:
                    if parse_datetime(data_dict['lastaction'], ignoretz=True) < datetime.now() - timedelta(days=1):
                        self.stats['workshops_skipped'] += 1
                        return

        location_dict = data_dict['location']
        museum_guid = int(location_dict.get('SMart_id', 0))
        try:
            museum = Museum.objects.get(pk=self.MUSEUM_MAPPER.get(museum_guid, 0))
        except Museum.DoesNotExist:
            workshop.museum = None
            workshop.location_title = location_dict.get('name', '')
            workshop.street_address = location_dict.get('street', '')
            workshop.postal_code, workshop.city = location_dict.get('town', ' ').split(' ')
            workshop.country = 'de'
        else:
            workshop.museum = museum
            workshop.street_address = museum.street_address
            workshop.street_address2 = museum.street_address2
            workshop.postal_code = museum.postal_code
            workshop.city = museum.city
            workshop.country = museum.country
            workshop.latitude = museum.latitude
            workshop.longitude = museum.longitude

        url = self.URL_EVENT.format(min(data_dict['dates'].keys()))
        response = requests.get(url)
        if response.status_code != requests.codes.OK:
            self.stderr.write(
                u"Error status {} when trying to access {}\n".format(response.status_code, url))
            return

        data_dict = response.json()

        if data_dict['status'] != "www":
            self.stats['workshops_skipped'] += 1
            return

        workshop.title_de, workshop.subtitle_de = self.cleanup_html(data_dict['title_de']), self.cleanup_html(
            data_dict['title_sub_de'])
        workshop.title_en, workshop.subtitle_en = self.cleanup_html(data_dict['title_en']), self.cleanup_html(
            data_dict['title_sub_en'])

        if not workshop.title_en:
            workshop.title_en = workshop.title_de
        if not workshop.subtitle_en:
            workshop.subtitle_en = workshop.subtitle_de

        workshop.slug = get_unique_value(Workshop, better_slugify(data_dict['title_de'], remove_stopwords=False), instance_pk=workshop.pk)

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

        workshop.admission_price = None
        if price_str:
            try:
                workshop.admission_price = Decimal(price_str)
            except:
                pass

        price_de_str = price_en_str = ''
        if not workshop.admission_price:
            price_de_str = self.cleanup_html(data_dict['kosten_de'])
            price_en_str = self.cleanup_html(data_dict['kosten_en']) or self.cleanup_html(data_dict['kosten_de'])

        workshop.admission_price_info_de = u"{} {}".format(
            price_de_str,
            strip_html(self.cleanup_html(data_dict['kosten_text_de']))
        ).strip()
        workshop.admission_price_info_en = u"{} {}".format(
            price_en_str,
            strip_html(self.cleanup_html(data_dict['kosten_text_en']) or self.cleanup_html(data_dict['kosten_text_de']))
        ).strip()
        workshop.admission_price_info_de_markup_type = "pt"
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
                exh_mapper = self.service_exhibitions.objectmapper_set.get(
                    external_id=correct_exhibition_id,
                    content_type__app_label="exhibitions",
                    content_type__model="exhibition",
                )
            except models.ObjectDoesNotExist:
                pass
            else:
                workshop.exhibition = exh_mapper.content_object

        if workshop.status not in ("published", "trashed", "not_listed"):
            workshop.status = self.DEFAULT_WORKSHOP_STATUS
        if not workshop.description_locked:
            workshop.description_locked = False
        if not workshop.free_admission:
            workshop.free_admission = False
        if not workshop.has_group_offer:
            workshop.has_group_offer = False
        if not workshop.is_for_preschool:
            workshop.is_for_preschool = False
        if not workshop.is_for_primary_school:
            workshop.is_for_primary_school = False
        if not workshop.is_for_youth:
            workshop.is_for_youth = False
        if not workshop.is_for_families:
            workshop.is_for_families = False
        if not workshop.is_for_wheelchaired:
            workshop.is_for_wheelchaired = False
        if not workshop.is_for_deaf:
            workshop.is_for_deaf = False
        if not workshop.is_for_blind:
            workshop.is_for_blind = False
        if not workshop.is_for_learning_difficulties:
            workshop.is_for_learning_difficulties = False
        if not workshop.is_for_dementia_sufferers:
            workshop.is_for_dementia_sufferers = False
        workshop.save()

        workshop.types.clear()
        if int(data_dict['event_types_detail'].keys()[0]) == 137:
            workshop.types.add(WorkshopType.objects.get(slug="workshop"))
        else:
            workshop.types.add(WorkshopType.objects.get(slug="guided-tour"))

        if not self.skip_images:
            # get biggest possible images
            image_ids_to_keep = []
            # the image versions are saved as img_<id>
            images_keys = [key for key in data_dict.keys() if key.startswith("img_")]
            img_teaser = []
            if images_keys:
                img_teaser = data_dict[images_keys[-1]]  # take the last size
                # sometimes the image teaser is a dict, sometimes a list of dicts
                if isinstance(img_teaser, dict):
                    img_teaser = [img_teaser]
            for image_dict in img_teaser:
                image_url = image_dict.get('path_xl') or image_dict.get('path')

                image_external_id = "wrk-{}-{}".format(workshop.pk, image_url)
                image_mapper = None
                try:
                    # get image model instance from saved mapper
                    image_mapper = self.service_exhibitions.objectmapper_set.get(
                        external_id=image_external_id,
                        content_type__app_label="workshops",
                        content_type__model="mediafile",
                    )
                except models.ObjectDoesNotExist:
                    # or create a new exhibition and then create a mapper
                    mf = MediaFile(workshop=workshop)
                else:
                    mf = image_mapper.content_object
                    if mf:
                        image_ids_to_keep.append(mf.pk)
                        file_description = self.save_file_description(mf.path, image_dict)
                    else:
                        if self.update_all:
                            # restore image
                            mf = MediaFile(workshop=workshop)
                        else:
                            # skip deleted images
                            continue
                    if not self.update_all:
                        continue

                filename = image_url.split("/")[-1]
                image_response = requests.get(image_url)
                if image_response.status_code != requests.codes.OK:
                    self.stderr.write(
                        u"Error status {} when trying to access {}\n".format(
                            image_response.status_code,
                            image_url,
                        )
                    )
                    continue
                image_mods.FileManager.delete_file_for_object(
                    mf,
                    field_name="path",
                )
                image_mods.FileManager.save_file_for_object(
                    mf,
                    filename,
                    image_response.content,
                    field_name="path",
                    subpath="workshops/%s/gallery/" % workshop.slug,
                )
                mf.save()
                image_ids_to_keep.append(mf.pk)

                file_description = self.save_file_description(mf.path, image_dict)

                if not image_mapper:
                    image_mapper = ObjectMapper(
                        service=self.service_exhibitions,
                        external_id=image_external_id,
                    )
                image_mapper.content_object = mf
                image_mapper.save()

            if img_teaser:
                for mf in workshop.mediafile_set.exclude(id__in=image_ids_to_keep):
                    if mf.path:
                        # remove the file from the file system
                        image_mods.FileManager.delete_file(mf.path.name)
                    # delete image mapper
                    self.service_exhibitions.objectmapper_set.filter(
                        object_id=mf.pk,
                        content_type__app_label="workshops",
                        content_type__model="mediafile",
                    ).delete()
                    # delete image model instance
                    mf.delete()

            if not img_teaser and workshop.exhibition and not workshop.mediafile_set.count():
                # copy the images from exhibition just once without updating, if images don't exist in the feed
                for exhibition_mf in workshop.exhibition.mediafile_set.all():
                    mf = MediaFile(workshop=workshop)
                    filename = exhibition_mf.path.filename
                    try:
                        image_data = open(settings.MEDIA_ROOT + "/" + exhibition_mf.path.path, "rb")
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

                    try:
                        exhibition_mf_description = FileDescription.objects.filter(
                            file_path=exhibition_mf.path,
                        ).order_by("pk")[0]
                    except IndexError:
                        pass
                    else:
                        self.save_file_description(mf.path, {
                            'description_de': exhibition_mf_description.title_de,
                            'description_en': exhibition_mf_description.title_en,
                            'copyright_de': Command.prefix_with_c(exhibition_mf_description.author),
                        })

            sort_order = 0
            for mf in workshop.mediafile_set.all():
                workshop.mediafile_set.filter(pk=mf.pk).update(sort_order=sort_order)
                sort_order += 1

        workshop.organizer_set.all().delete()
        linked_institutions = data_dict.get('linked_institutions', {})
        if linked_institutions:
            for linked_inst_smb_id in linked_institutions.keys():
                try:
                    organizing_museum = Museum.objects.get(
                        pk=self.LINKED_INSTITUTION_MAPPER.get(int(linked_inst_smb_id), None))
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
            end = None
            if event_time_dict['end']:
                try:
                    end = parse_datetime(event_time_dict['end'], ignoretz=True)
                except ValueError:  # sometimes the end date is malformed
                    pass
            if not end:
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
                service=self.service_events,
                external_id=external_id,
            )
            mapper.content_object = workshop
            mapper.save()
            if self.verbosity > 1:
                self.stats['workshops_added'] += 1
        else:
            if self.verbosity > 1:
                self.stats['workshops_updated'] += 1

    def save_event(self, external_id, data_dict):
        import requests
        from datetime import datetime, timedelta
        from dateutil.parser import parse as parse_datetime
        from decimal import Decimal

        from django.db import models
        from base_libs.utils.betterslugify import better_slugify
        from django.conf import settings

        from filebrowser.models import FileDescription
        from base_libs.utils.misc import get_unique_value

        image_mods = models.get_app("image_mods")
        Museum = models.get_model("museums", "Museum")
        Event = models.get_model("events", "Event")
        EventCategory = models.get_model("events", "EventCategory")
        EventTime = models.get_model("events", "EventTime")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Organizer = models.get_model("events", "Organizer")
        MediaFile = models.get_model("events", "MediaFile")

        # get or create event
        mapper = None
        try:
            # get event from saved mapper
            mapper = self.service_events.objectmapper_set.get(
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
                self.stats['events_skipped'] += 1
                return
            else:
                if not self.update_all:
                    if parse_datetime(data_dict['lastaction'], ignoretz=True) < datetime.now() - timedelta(days=1):
                        self.stats['events_skipped'] += 1
                        return

        location_dict = data_dict['location']
        museum_guid = int(location_dict.get('SMart_id', 0))
        try:
            museum = Museum.objects.get(pk=self.MUSEUM_MAPPER.get(museum_guid, 0))
        except Museum.DoesNotExist:
            event.museum = None
            event.location_title = location_dict.get('name', '')
            event.street_address = location_dict.get('street', '')
            event.postal_code, event.city = location_dict.get('town', ' ').split(' ')
            event.country = 'de'
        else:
            event.museum = museum
            event.street_address = museum.street_address
            event.street_address2 = museum.street_address2
            event.postal_code = museum.postal_code
            event.city = museum.city
            event.country = museum.country
            event.latitude = museum.latitude
            event.longitude = museum.longitude

        url = self.URL_EVENT.format(min(data_dict['dates'].keys()))
        response = requests.get(url)
        if response.status_code != requests.codes.OK:
            self.stderr.write(
                u"Error status {} when trying to access {}\n".format(response.status_code, url))
            return

        data_dict = response.json()

        if data_dict['status'] != "www":
            self.stats['events_skipped'] += 1
            return

        event.title_de, event.subtitle_de = self.cleanup_html(data_dict['title_de']), self.cleanup_html(
            data_dict['title_sub_de'])
        event.title_en, event.subtitle_en = self.cleanup_html(data_dict['title_en']), self.cleanup_html(
            data_dict['title_sub_en'])
        if not event.title_en:
            event.title_en = event.title_de
        if not event.subtitle_en:
            event.subtitle_en = event.subtitle_de

        event.slug = get_unique_value(Event, better_slugify(data_dict['title_de'], remove_stopwords=False), instance_pk=event.pk)

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

        event.admission_price = None
        if price_str:
            try:
                event.admission_price = Decimal(price_str)
            except:
                pass

        price_de_str = price_en_str = ''
        if not event.admission_price:
            price_de_str = self.cleanup_html(data_dict['kosten_de'])
            price_en_str = self.cleanup_html(data_dict['kosten_en']) or self.cleanup_html(data_dict['kosten_de'])

        event.admission_price_info_de = u"{} {}".format(
            price_de_str,
            strip_html(self.cleanup_html(data_dict['kosten_text_de']))
        ).strip()
        event.admission_price_info_en = u"{} {}".format(
            price_en_str,
            strip_html(self.cleanup_html(data_dict['kosten_text_en']) or self.cleanup_html(data_dict['kosten_text_de']))
        ).strip()
        event.admission_price_info_de_markup_type = "pt"
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
            if target_group_id in (
            301, 302, 303, 304, 305, 306):  # "Kinder", "Jugendliche", "Familien + Kinder 4-6", "Familien + Kinder 6-12"
                event.suitable_for_children = True

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
                exh_mapper = self.service_exhibitions.objectmapper_set.get(
                    external_id=correct_exhibition_id,
                    content_type__app_label="exhibitions",
                    content_type__model="exhibition",
                )
            except models.ObjectDoesNotExist:
                pass
            else:
                event.exhibition = exh_mapper.content_object

        if event.status not in ("published", "trashed", "not_listed"):
            event.status = self.DEFAULT_EVENT_STATUS
        if not event.description_locked:
            event.description_locked = False
        if not event.featured:
            event.featured = False
        if not event.free_admission:
            event.free_admission = False
        if not event.suitable_for_children:
            event.suitable_for_children = False
        event.save()

        event.categories.clear()
        for event_cat_id in (data_dict.get('event_types_detail', {}) or {}).keys():
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
                    organizing_museum = Museum.objects.get(
                        pk=self.LINKED_INSTITUTION_MAPPER.get(int(linked_inst_smb_id), None))
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

        if not self.skip_images:
            # get biggest possible images
            image_ids_to_keep = []
            # the image versions are saved as img_<id>
            images_keys = [key for key in data_dict.keys() if key.startswith("img_")]
            img_teaser = []
            if images_keys:
                img_teaser = data_dict[images_keys[-1]]  # take the last size
                # sometimes the image teaser is a dict, sometimes a list of dicts
                if isinstance(img_teaser, dict):
                    img_teaser = [img_teaser]
            for image_dict in img_teaser:
                image_url = image_dict.get('path_xl') or image_dict.get('path')

                image_external_id = "ev-{}-{}".format(event.pk, image_url)
                image_mapper = None
                try:
                    # get image model instance from saved mapper
                    image_mapper = self.service_exhibitions.objectmapper_set.get(
                        external_id=image_external_id,
                        content_type__app_label="events",
                        content_type__model="mediafile",
                    )
                except models.ObjectDoesNotExist:
                    # or create a new exhibition and then create a mapper
                    mf = MediaFile(event=event)
                else:
                    mf = image_mapper.content_object
                    if mf:
                        image_ids_to_keep.append(mf.pk)
                        file_description = self.save_file_description(mf.path, image_dict)
                    else:
                        if self.update_all:
                            # restore image
                            mf = MediaFile(event=event)
                        else:
                            # skip deleted images
                            continue
                    if not self.update_all:
                        continue

                filename = image_url.split("/")[-1]
                image_response = requests.get(image_url)
                if image_response.status_code != requests.codes.OK:
                    self.stderr.write(
                        u"Error status {} when trying to access {}\n".format(
                            image_response.status_code,
                            image_url,
                        )
                    )
                    continue
                image_mods.FileManager.delete_file_for_object(
                    mf,
                    field_name="path",
                )
                image_mods.FileManager.save_file_for_object(
                    mf,
                    filename,
                    image_response.content,
                    field_name="path",
                    subpath="events/%s/gallery/" % event.slug,
                )
                mf.save()
                image_ids_to_keep.append(mf.pk)

                file_description = self.save_file_description(mf.path, image_dict)

                if not image_mapper:
                    image_mapper = ObjectMapper(
                        service=self.service_exhibitions,
                        external_id=image_external_id,
                    )
                image_mapper.content_object = mf
                image_mapper.save()

            if img_teaser:
                for mf in event.mediafile_set.exclude(id__in=image_ids_to_keep):
                    if mf.path:
                        # remove the file from the file system
                        image_mods.FileManager.delete_file(mf.path.name)
                    # delete image mapper
                    self.service_exhibitions.objectmapper_set.filter(
                        object_id=mf.pk,
                        content_type__app_label="events",
                        content_type__model="mediafile",
                    ).delete()
                    # delete image model instance
                    mf.delete()

            if not img_teaser and event.exhibition and not event.mediafile_set.count():
                for exhibition_mf in event.exhibition.mediafile_set.all():
                    mf = MediaFile(event=event)
                    filename = exhibition_mf.path.filename
                    try:
                        image_data = open(settings.MEDIA_ROOT + "/" + exhibition_mf.path.path, "rb")
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

                    try:
                        exhibition_mf_description = FileDescription.objects.filter(
                            file_path=exhibition_mf.path,
                        ).order_by("pk")[0]
                    except IndexError:
                        pass
                    else:
                        self.save_file_description(mf.path, {
                            'description_de': exhibition_mf_description.title_de,
                            'description_en': exhibition_mf_description.title_en,
                            'copyright_de': Command.prefix_with_c(exhibition_mf_description.author),
                        })

            sort_order = 0
            for mf in event.mediafile_set.all():
                event.mediafile_set.filter(pk=mf.pk).update(sort_order=sort_order)
                sort_order += 1


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
            end = None
            if event_time_dict['end']:
                try:
                    end = parse_datetime(event_time_dict['end'], ignoretz=True)
                except ValueError:
                    pass
            if not end:
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
                service=self.service_events,
                external_id=external_id,
            )
            mapper.content_object = event
            mapper.save()
            if self.verbosity > 1:
                self.stats['events_added'] += 1
        else:
            if self.verbosity > 1:
                self.stats['events_updated'] += 1

    def import_events_and_workshops(self):
        import requests

        ### IMPORT EVENTS AND WORKSHOPS ###
        if self.verbosity > 1:
            self.stdout.write("### IMPORTING EVENTS AND WORKSHOPS ###\n")
            self.stdout.flush()

        response = requests.get(self.service_events.url)
        if response.status_code != requests.codes.OK:
            self.stderr.write(u"Error status {} when trying to access {}\n".format(response.status_code, self.service_events.url))
            return

        list_data_dict = response.json()

        for external_id, data_dict in list_data_dict.items():

            if self.verbosity > 1:
                self.stdout.write(u"- {} (id={})\n".format(self.cleanup_html(data_dict['title_de']), external_id))
                self.stdout.flush()

            # based on http://ww2.smb.museum/smb/export/getEventTypeListFromSMart.php?format=json
            event_type_ids = (data_dict.get('event_types_detail', {}) or {}).keys()
            if event_type_ids and int(event_type_ids[0]) in (45, 215, 216, 217, 218, 219, 137):
                self.save_workshop(external_id, data_dict)
            else:
                self.save_event(external_id, data_dict)

        if self.verbosity > 1:
            self.stdout.write("\n")
            self.stdout.flush()

    def finalize(self):
        if self.verbosity > 1:
            self.stdout.write("-------------------\nFinished.\n-------------------\n")
            self.stdout.write("Exibitions added: {}\n".format(self.stats['exhibitions_added']))
            self.stdout.write("Exibitions updated: {}\n".format(self.stats['exhibitions_updated']))
            self.stdout.write("Exibitions skipped: {}\n\n".format(self.stats['exhibitions_skipped']))

            self.stdout.write("Events added: {}\n".format(self.stats['events_added']))
            self.stdout.write("Events updated: {}\n".format(self.stats['events_updated']))
            self.stdout.write("Events skipped: {}\n\n".format(self.stats['events_skipped']))

            self.stdout.write("Workshops added: {}\n".format(self.stats['workshops_added']))
            self.stdout.write("Workshops updated: {}\n".format(self.stats['workshops_updated']))
            self.stdout.write("Workshops skipped: {}\n\n".format(self.stats['workshops_skipped']))
