# -*- coding: UTF-8 -*-
from optparse import make_option

from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
                    help='Tells Django to NOT download images.'),
    )
    help = """Imports events from Museumsportal Berlin"""

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        skip_images = options.get('skip_images')

        import re
        import urllib2
        from datetime import timedelta
        from rest.client import webcall
        from xml.dom.minidom import parseString
        from dateutil.parser import parse as parse_datetime

        from django.db import models
        from django.template.defaultfilters import slugify

        from base_libs.utils.misc import get_related_queryset

        from jetson.apps.external_services.utils import get_first
        from jetson.apps.external_services.utils import get_value

        image_mods = models.get_app("image_mods")
        Address = models.get_model("location", "Address")
        Institution = models.get_model("institutions", "Institution")
        InstitutionalContact = models.get_model("institutions", "InstitutionalContact")
        Event = models.get_model("events", "Event")
        EventTime = models.get_model("events", "EventTime")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Service = models.get_model("external_services", "Service")

        old_to_new_museum_id_mapper = (
            (1321, 277),  # Deutsches Technikmuseum
        )

        (
            (1611, 8),
            (1131, 9),
            (1136, 10),
            (1146, 11),
            (1141, 12),
            (1151, 13),
            (1156, 14),
            (3126, 15),
            (1161, 16),
            (1166, 17),
            (1176, 18),
            (1171, 19),
            (1181, 20),
            (1186, 21),
            (1196, 23),
            (1201, 24),
            (1206, 25),
            (2076, 26),
            (5654, 27),
            (1211, 28),
            (2046, 29),
            (1216, 30),
            (1221, 31),
            (5632, 32),
            (2036, 33),
            (1226, 34),
            (1586, 35),
            (1231, 36),
            (1236, 37),
            (1241, 38),
            (3116, 39),
            (1251, 41),
            (1256, 42),
            (1261, 43),
            (1266, 44),
            (1271, 45),
            (5656, 46),
            (1276, 47),
            (1281, 48),
            (1286, 49),
            (1291, 50),
            (1296, 51),
            (1301, 52),
            (1326, 53),
            (1306, 54),
            (1736, 55),
            (1311, 57),
            (1316, 58),
            (1321, 59),
            (1336, 61),
            (1376, 62),
            (1341, 63),
            (1346, 64),
            (1351, 65),
            (1356, 66),
            (1361, 67),
            (1366, 68),
            (1381, 70),
            (1386, 71),
            (5620, 72),
            (1391, 73),
            (1396, 74),
            (1401, 75),
            (1406, 76),
            (1411, 77),
            (5636, 78),
            (1416, 79),
            (1421, 80),
            (1426, 81),
            (1431, 82),
            (1436, 83),
            (3156, 84),
            (1441, 85),
            (1446, 86),
            (1451, 87),
            (1456, 88),
            (1461, 89),
            (1466, 90),
            (1126, 91),
            (1476, 92),
            (1481, 93),
            (1486, 94),
            (1491, 95),
            (1501, 96),
            (1516, 99),
            (1531, 102),
            (1536, 103),
            (1541, 104),
            (1546, 105),
            (1551, 106),
            (1556, 107),
            (1971, 109),
            (1561, 110),
            (1566, 111),
            (1571, 112),
            (1576, 113),
            (1581, 114),
            (5634, 115),
            (1591, 116),
            (1596, 117),
            (1601, 118),
            (1606, 119),
            (1616, 120),
            (1621, 122),
            (1636, 125),
            (1641, 126),
            (1646, 127),
            (1651, 128),
            (1656, 129),
            (1661, 130),
            (1666, 131),
            (5638, 132),
            (1681, 134),
            (1686, 135),
            (1696, 136),
            (1701, 137),
            (1711, 138),
            (1716, 139),
            (1471, 140),
            (5626, 141),
            (1706, 142),
            (1721, 143),
            (1726, 144),
            (1731, 145),
            (1741, 147),
            (1746, 148),
            (1751, 149),
            (1756, 150),
            (1761, 151),
            (1771, 152),
            (5628, 153),
            (1781, 154),
            (1786, 155),
            (2016, 209),
            (1791, 156),
            (1851, 157),
            (1841, 158),
            (1796, 159),
            (1801, 160),
            (1806, 161),
            (1811, 162),
            # (1816, 163),
            (1821, 165),
            (1826, 166),
            # (1831, 167),
            (1836, 168),
            (3136, 169),
            (1846, 170),
            (1856, 171),
            (1861, 172),
            (1866, 173),
            (1871, 174),
            (1876, 175),
            (3146, 176),
            (1881, 177),
            (1886, 178),
            (1896, 179),
            (1901, 180),
            (1906, 181),
            (1911, 182),
            (1916, 183),
            (1921, 184),
            (1926, 185),
            (1931, 186),
            (1936, 187),
            (1941, 188),
            (1946, 189),
            (1951, 190),
            (1956, 191),
            (1961, 192),
            (1891, 193),
            (1966, 194),
            (1976, 195),
            (3106, 196),
            # (1981, 197),
            (1986, 198),
            (1991, 199),
            # (1996, 200),
            (1371, 201),
            # (2001, 202),
            (1671, 203),
            (2006, 204),
            (2026, 205),
            (2011, 206),
            (5630, 207),
            (2021, 210),
            (2031, 211),
            (2041, 212),
            (2051, 213),
            (1496, 215),
            (2061, 216),
            (2066, 217),
            # ---
            (3126, 16),
            (1171, 20),
            (1186, 22),
            (2036, 34),
            (3116, 40),
            (1261, 44),
            (5656, 47),
            (1281, 49),
            (1291, 51),
            (1736, 56),
            (1316, 59),
            (5638, 133),
            (1731, 146),
            (1751, 150),
            (1771, 153),
            (1791, 157),
            (1806, 162),
            (1816, 164),
            (1831, 168),
            (1981, 198),
            (1996, 201),
            (2001, 203),
        )

        def parse_phone(full_number):
            country = "49"
            full_number = re.sub(r"^\+49\D*", "", full_number)
            full_number = re.sub(r"\(|\)", "", full_number)
            parts = re.split(r"\D*", full_number, 1)
            if len(parts) == 2:
                area, number = parts
                if area[0] == "0":
                    area = area[1:]
            else:
                area = ""
                number = parts[0]
            if len(number) > 15:
                return "", "", ""
            return country, area, number

        ### IMPORT MUSEUMS ###
        if verbosity > 1:
            print u"### IMPORTING MUSEUMS ###"

        s_museums, created = Service.objects.get_or_create(
            sysname="museumsportal_berlin_museums",
            defaults={
                'url': "https://eingabe.museumsportal-berlin.de/mp_art/export_museums.php",
                'title': "Museumsportal Berlin Museums",
            },
        )
        if created:
            ### initial setup ###
            old_service = Service.objects.get(
                sysname="museumsportal_berlin",
            )
            for old_external_id, new_external_id in old_to_new_museum_id_mapper:
                try:
                    # get institution from saved mapper
                    old_mapper = old_service.objectmapper_set.get(
                        external_id=str(old_external_id),
                        content_type__app_label="institutions",
                        content_type__model="institution",
                    )
                except models.ObjectDoesNotExist:
                    pass
                else:
                    if old_mapper.content_object:
                        mapper = ObjectMapper(
                            service=s_museums,
                            external_id=str(new_external_id),
                        )
                        mapper.content_object = old_mapper.content_object
                        mapper.save()

        @webcall(url=s_museums.url)
        def get_museums_data():
            pass

        data = get_museums_data()

        xml_doc = parseString(data)

        status_imported = "import"

        inst_type_museum = get_related_queryset(Institution, "institution_types").get(
            slug="museum",
        )
        cs_art = get_related_queryset(Institution, "creative_sectors").get(
            sysname="art",
        )
        phone_type = get_related_queryset(InstitutionalContact, "phone0_type").get(
            slug="phone",
        )
        fax_type = get_related_queryset(InstitutionalContact, "phone0_type").get(
            slug="fax",
        )

        stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
        }
        for node_museum in xml_doc.getElementsByTagName("museum"):
            external_id = get_value(node_museum, "uid")
            change_date = parse_datetime(
                get_value(node_museum, "dtstamp"),
                ignoretz=True,
            )

            # get or create event
            mapper = None
            try:
                # get event from saved mapper
                mapper = s_museums.objectmapper_set.get(
                    external_id=external_id,
                    content_type__app_label="institutions",
                    content_type__model="institution",
                )
            except models.ObjectDoesNotExist:
                # or create a new article and then create a mapper
                institution = Institution()
            else:
                institution = mapper.content_object
                if not institution:
                    # if event was deleted after import,
                    # don't import it again
                    continue
                if institution.modified_date and institution.modified_date > change_date or institution.creation_date > change_date:
                    if verbosity > 1:
                        print u" > %s (pk=%s, uid=%s) skipped" % (institution, institution.pk, external_id)
                        stats['skipped'] += 1
                    continue

            for node_title in node_museum.getElementsByTagName("title"):
                if node_title.getAttribute("xml:lang") == "de":
                    institution.title = get_value(node_title)

            existing = Institution.objects.filter(slug=slugify(institution.title))
            if existing:
                institution.pk = existing[0].pk

            for node_subtitle in node_museum.getElementsByTagName("subtitle"):
                if node_subtitle.getAttribute("xml:lang") == "de":
                    institution.title2 = get_value(node_subtitle)
            for node_description in node_museum.getElementsByTagName("description"):
                setattr(
                    institution,
                    "description_%s" % node_description.getAttribute("xml:lang"),
                    get_value(node_description),
                )

            opening_times = get_value(
                node_museum,
                "opentime",
            )
            # parse this format: "Mo:10:00-18:00#Di:-#Mi:10:00-18:00#Do:10:00-20:00#Fr:10:00-18:00#Sa:10:00-18:00#So:10:00-18:00"
            weekday_map = {
                'Mo': "mon",
                'Di': "tue",
                'Mi': "wed",
                'Do': "thu",
                'Fr': "fri",
                'Sa': "sat",
                'So': "sun",
            }
            if opening_times:
                for day_opening_times in opening_times.split("#"):
                    day, opening_times = day_opening_times.split(":", 1)
                    opening, closing = opening_times.split("-")
                    if opening:
                        setattr(
                            institution,
                            "%s_open" % weekday_map[day],
                            opening,
                        )
                        setattr(
                            institution,
                            "%s_close" % weekday_map[day],
                            closing,
                        )

            if not institution.status or institution.status == "draft":
                institution.status = status_imported
            institution.save()
            institution.institution_types.add(inst_type_museum)
            institution.creative_sectors.add(cs_art)

            image_url = get_value(node_museum, "image_path")
            if image_url and not skip_images:
                filename = image_url.split("/")[-1]
                image_data = urllib2.urlopen(image_url)
                image_mods.FileManager.save_file_for_object(
                    institution,
                    filename,
                    image_data.read(),
                    subpath="avatar/"
                )

            contacts = institution.institutionalcontact_set.order_by('-is_primary', 'id')
            if contacts:
                contact = contacts[0]
            else:
                contact = InstitutionalContact(institution=institution)

            contact.url0_link = get_value(
                node_museum,
                "website",
            )

            phone = get_value(node_museum, "phone")
            if phone:
                contact.phone0_type = phone_type
                (contact.phone0_country, contact.phone0_area, contact.phone0_number) = parse_phone(phone)

            fax = get_value(node_museum, "fax")
            if phone:
                contact.phone1_type = fax_type
                (contact.phone1_country, contact.phone1_area, contact.phone1_number) = parse_phone(fax)

            phone = get_value(node_museum, "service_phone")
            if phone:
                contact.phone2_type = phone_type
                (contact.phone2_country, contact.phone2_area, contact.phone2_number) = parse_phone(phone)

            contact.is_primary = True
            contact.save()

            Address.objects.set_for(
                contact,
                "postal_address",
                country="DE",
                district=get_value(node_museum, "address-district"),
                city=get_value(node_museum, "address-town"),
                postal_code=get_value(node_museum, "address-zip"),
                street_address=get_value(node_museum, "address-street"),
            )

            if not mapper:
                mapper = ObjectMapper(
                    service=s_museums,
                    external_id=external_id,
                )
                mapper.content_object = institution
                mapper.save()
                if verbosity > 1:
                    if existing:
                        print u" > %s (pk=%s, uid=%s) updated" % (institution, institution.pk, external_id)
                        stats['updated'] += 1
                    else:
                        print u" > %s (pk=%s, uid=%s) added" % (institution, institution.pk, external_id)
                        stats['added'] += 1
            else:
                if verbosity > 1:
                    print u" > %s (pk=%s, uid=%s) updated" % (institution, institution.pk, external_id)
                    stats['updated'] += 1
        if verbosity > 1:
            print u"Museums added: %d" % stats['added']
            print u"Museums updated: %d" % stats['updated']
            print u"Museums skipped: %d" % stats['skipped']
            print

        ### IMPORT EXHIBITIONS ###
        if verbosity > 1:
            print u"### IMPORTING EXHIBITIONS ###"
        s_exhibitions, created = Service.objects.get_or_create(
            sysname="museumsportal_berlin_exhibitions",
            defaults={
                'url': "https://eingabe.museumsportal-berlin.de/mp_art/export_exhibitions.php",
                'title': "Museumsportal Berlin Exhibitions",
            },
        )

        @webcall(url=s_exhibitions.url)
        def get_museumsportal_data():
            pass

        data = get_museumsportal_data()

        xml_doc = parseString(data)

        event_type = get_related_queryset(Event, "event_type").get(
            slug="exhibition",
        )

        stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
        }
        for node_event in xml_doc.getElementsByTagName("vevent"):
            external_id = get_value(node_event, "uid")

            museum_guid = get_first(node_event, "location").getAttribute("location_id")
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
                mapper = s_exhibitions.objectmapper_set.get(
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

            event.event_type = event_type
            event.status = status_imported
            event.venue = inst
            event.organizing_institution = inst
            for node_title in node_event.getElementsByTagName("summary"):
                if node_title.getAttribute("xml:lang") in ("en", "de"):
                    setattr(
                        event,
                        "title_%s" % node_title.getAttribute("xml:lang"),
                        get_value(node_title),
                    )
            if not event.title:
                event.title_en = event.title_de
            for node_description in node_event.getElementsByTagName("x-ce-description"):
                if node_description.getAttribute("xml:lang") in ("en", "de"):
                    setattr(
                        event,
                        "description_%s" % node_description.getAttribute("xml:lang"),
                        get_value(node_description),
                    )
            event.url0_link = get_value(
                node_event,
                "x-ce-url",
            )
            opening_times = get_value(
                node_event,
                "x-ce-opentime",
            )
            # parse this format: "Mo:10:00-18:00#Di:-#Mi:10:00-18:00#Do:10:00-20:00#Fr:10:00-18:00#Sa:10:00-18:00#So:10:00-18:00"
            weekday_map = {
                'Mo': "mon",
                'Di': "tue",
                'Mi': "wed",
                'Do': "thu",
                'Fr': "fri",
                'Sa': "sat",
                'So': "sun",
            }
            if opening_times:
                for day_opening_times in opening_times.split("#"):
                    day, opening_times = day_opening_times.split(":", 1)
                    opening, closing = opening_times.split("-")
                    if opening:
                        setattr(
                            event,
                            "%s_open" % weekday_map[day],
                            opening,
                        )
                        setattr(
                            event,
                            "%s_close" % weekday_map[day],
                            closing,
                        )

            event.save()

            image_url = get_value(node_event, "image_path")
            if image_url and not skip_images:
                filename = image_url.split("/")[-1]
                image_data = urllib2.urlopen(image_url)
                image_mods.FileManager.save_file_for_object(
                    event,
                    filename,
                    image_data.read(),
                    subpath="avatar/"
                )

            event.creative_sectors.add(cs_art)

            if inst_contact:
                Address.objects.set_for(
                    event,
                    "postal_address",
                    country=inst_contact.get("country", "DE"),
                    district=inst_contact['district'],
                    city=inst_contact['city'],
                    postal_code=inst_contact['postal_code'],
                    street_address=inst_contact['street_address'],
                    street_address2=inst_contact['street_address2'],
                )

            start = parse_datetime(
                get_value(node_event, "dtstart"),
                ignoretz=True,
            )
            end = parse_datetime(
                get_value(node_event, "dtend"),
                ignoretz=True,
            )
            time = EventTime(
                event=event,
                start_yyyy=start.year,
                start_mm=start.month,
                start_dd=start.day,
                end_yyyy=end.year,
                end_mm=end.month,
                end_dd=end.day,
                is_all_day=True,
            )
            time.save()

            if not mapper:
                mapper = ObjectMapper(
                    service=s_exhibitions,
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
            print u"Exibitions added: %d" % stats['added']
            print u"Exibitions updated: %d" % stats['updated']
            print u"Exibitions skipped: %d" % stats['skipped']
            print

        ### IMPORT EVENTS ###
        if verbosity > 1:
            print u"### IMPORTING EVENTS ###"
        event_type_mapper = {
            '51': 'festival',
            '1': 'guided-tour',
            '36': 'concert',
            '31': 'reading',
            '16': 'guided-tour',
            '3': 'guided-tour',
            '11': 'guided-tour',
            '21': 'guided-tour',
            '91': 'guided-tour',
            '56': 'convention',
            '41': 'performance',
            '86': 'vernissage',
            '66': 'lecture',
            '71': 'workshop',
        }

        s_events, created = Service.objects.get_or_create(
            sysname="museumsportal_berlin_events",
            defaults={
                'url': "https://eingabe.museumsportal-berlin.de/mp_art/export_events.php",
                'title': "Museumsportal Berlin Events",
            },
        )

        @webcall(url=s_events.url)
        def get_events_data():
            pass

        data = get_events_data()

        xml_doc = parseString(data)

        stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
        }

        for node_event in xml_doc.getElementsByTagName("vevent"):
            external_id = get_value(node_event, "uid")

            museum_node = get_first(node_event, "location")
            if not museum_node:
                # don't import events of unknown museums
                continue
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
            for node_title in node_event.getElementsByTagName("summary"):
                if node_title.getAttribute("xml:lang") in ("en", "de"):
                    setattr(
                        event,
                        "title_%s" % node_title.getAttribute("xml:lang"),
                        get_value(node_title),
                    )
            if not event.title:
                event.title_en = event.title_de
            for node_description in node_event.getElementsByTagName("x-ce-description"):
                if node_description.getAttribute("xml:lang") in ("en", "de"):
                    setattr(
                        event,
                        "description_%s" % node_description.getAttribute("xml:lang"),
                        get_value(node_description),
                    )
            fees_list_en = []
            fees_list_de = []
            normal_price = get_value(node_event, "x-ce-ticket-price")
            if normal_price:
                fees_list_en.append(u"Normal price: %s €" % normal_price)
                fees_list_de.append(u"Normaler Preis: %s €" % normal_price)
            reduced_price = get_value(node_event, "x-ce-ticket-price-reduced")
            if reduced_price:
                fees_list_en.append(u"Normal price: %s €" % reduced_price)
                fees_list_de.append(u"Ermäßigter Preis: %s €" % reduced_price)
            for node_infotext in node_event.getElementsByTagName("x-ce-ticket-infotext"):
                infotext = get_value(node_infotext)
                if infotext:
                    if node_infotext.getAttribute("xml:lang") == "en":
                        fees_list_en.append(get_value(node_infotext))
                    else:
                        fees_list_de.append(get_value(node_infotext))
            for node_infotext in node_event.getElementsByTagName("x-ce-booking-infotext"):
                infotext = get_value(node_infotext)
                if infotext:
                    if node_infotext.getAttribute("xml:lang") == "en":
                        fees_list_en.append(get_value(node_infotext))
                    else:
                        fees_list_de.append(get_value(node_infotext))
            event.fees_en = "\n".join(fees_list_en)
            event.fees_de = "\n".join(fees_list_de)

            event.event_type = event_type
            category_node = get_first(node_event, "x-ce-category")
            if category_node:
                event_type_id = category_node.getAttribute("id")
                if event_type_id in event_type_mapper:
                    event.event_type = get_related_queryset(
                        Event,
                        "event_type",
                    ).get(
                        slug=event_type_mapper[event_type_id],
                    )

            event.save()

            event.creative_sectors.add(cs_art)

            if inst_contact:
                Address.objects.set_for(
                    event,
                    "postal_address",
                    country=inst_contact.get("country", "DE"),
                    district=inst_contact['district'],
                    city=inst_contact['city'],
                    postal_code=inst_contact['postal_code'],
                    street_address=inst_contact['street_address'],
                    street_address2=inst_contact['street_address2'],
                )

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
