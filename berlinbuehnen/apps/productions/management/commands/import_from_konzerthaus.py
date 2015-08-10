# -*- coding: UTF-8 -*-

import requests
from xml.etree import ElementTree
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db import models
from django.utils.encoding import smart_str

from import_base import ImportFromHeimatBase

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand, ImportFromHeimatBase):
    option_list = NoArgsCommand.option_list + (
        make_option("--skip-images", action="store_true", dest="skip_images", default=False,
            help="Tells Django to NOT download images."),
    )
    help = "Imports productions and events from Konzerthaus Berlin"

    IMPORT_URL = " "
    DEFAULT_PUBLISHING_STATUS = "import"

    def handle_noargs(self, *args, **options):
        import re
        import os
        from datetime import time
        from dateutil.parser import parse as parse_datetime
        from django.conf import settings
        from django.utils.text import slugify
        from django.utils.encoding import smart_str, force_unicode
        from base_libs.utils.misc import get_unique_value
        from berlinbuehnen.apps.locations.models import Location, Stage
        from berlinbuehnen.apps.productions.models import Production, Event
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get("skip_images")

        Service = models.get_model("external_services", "Service")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Person = models.get_model("people", "Person")

        self.in_program_of = Location.objects.get(title_de=u"Konzerthaus Berlin")

        self.service, created = Service.objects.get_or_create(
            sysname="konzerthaus_berlin_prods",
            defaults={
                "url": self.IMPORT_URL,
                "title": "Konzerthaus Berlin Productions",
            },
        )

        self.stats = {
            "prods_added": 0,
            "prods_updated": 0,
            "prods_skipped": 0,
            "events_added": 0,
            "events_updated": 0,
            "events_skipped": 0,
        }

        with open(os.path.join(settings.PROJECT_PATH, "berlinbuehnen", "data", "Homepage-Konzerthaus.txt"), "rb") as f:
            all_file_data = force_unicode(f.read().decode("latin1"))
            all_file_data = re.compile(r"(\r\n|\r|\r)").sub("\n", all_file_data)
            for record in all_file_data.split("<-EOFIELD<-EOFILE"):

                production_dict = {}
                for field in record.strip().split("<-EOFIELD"):
                    if field:
                        field_name, field_value = field.strip().split(";", 1)
                        production_dict[field_name.strip()] = field_value.strip()

                if not production_dict.get("Veranstaltungs-Titel", False):
                    continue
                else:
                    print smart_str(production_dict["Veranstaltungs-Titel"])
                external_prod_id = production_dict["VeranstaltungsID"]

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
                        # if exhibition was deleted after import,
                        # don"t import it again
                        self.stats["prods_skipped"] += 1
                        continue

                prod.title_de = prod.title_en = production_dict["Veranstaltungs-Titel"]
                prod.subtitle_de = prod.subtitle_en = production_dict["Veranstaltungs-Untertitel"]
                prod.description_de = prod.description_en = production_dict["Beschreibung"]
                prod.slug = get_unique_value(Production, slugify(prod.title_de), instance_pk=prod.pk)

                if production_dict[u"Veröffentlichung Internet"] == "JA":
                    prod.status = "published"
                else:
                    prod.status = "draft"

                if production_dict["Status"] == "Fest gebucht":
                    prod.ticket_status = "sold_out"

                # production_dict["Projekt"] skipped

                prod.concert_program_de = production_dict["Werke-Sonderveranstaltungen"]
                if production_dict["Werke-Sonderveranstaltungen"] and production_dict["Werke"]:
                    prod.concert_program_de += "\n"
                prod.concert_program_de += production_dict["Werke"]

                prod.other_characteristics_de = production_dict["Label"]

                # production_dict["Reihe"] skipped

                production_dict["Kategorie"]

                # production_dict["Abo"] skipped

                prod.credits_de = production_dict["Sponsor"]

                # production_dict["KHO-ProdPlan"] skipped

                organizer, organizer_url, organizer_phone = production_dict["Veranstalter"].split("#")
                prod.organizers = organizer

                prod.tickets_website = production_dict["Ticketlink"]
                prod.price_information_de = prod.price_information_en = production_dict["Karteninfo"]

                prod.save()

                prod.in_program_of.add(self.in_program_of)

                prod.productioninvolvement_set.all().delete()
                position = 1
                for line in production_dict["Mitwirkende"].split("\n"):
                    first_and_last_name, subcategory, category = line.split("#")
                    if " " in first_and_last_name:
                        first_name, last_name = first_and_last_name.rsplit(" ", 1)
                    else:
                        first_name = ""
                        last_name = first_and_last_name

                    role_de = subcategory or category

                    p, created = Person.objects.get_first_or_create(
                        first_name=first_name,
                        last_name=last_name,
                    )
                    prod.productioninvolvement_set.create(
                        person=p,
                        involvement_role_de=role_de,
                        imported_sort_order=position,
                    )
                    position += 1


                try:
                    stage = Stage.objects.get(location=self.in_program_of, title_de=production_dict["Raum"])
                except Stage.DoesNotExist:
                    stage = Stage()
                    stage.location = self.in_program_of
                    stage.title_de = stage.title_en = production_dict["Raum"]
                stage.save()
                prod.play_stages.add(stage)

                if not mapper:
                    mapper = ObjectMapper(
                        service=self.service,
                        external_id=external_prod_id,
                    )
                    mapper.content_object = prod
                    mapper.save()
                    self.stats["prods_added"] += 1
                else:
                    self.stats["prods_updated"] += 1

                # save event
                event_mapper = None
                try:
                    # get exhibition from saved mapper
                    event_mapper = self.service.objectmapper_set.get(
                        external_id=external_prod_id,
                        content_type__app_label="productions",
                        content_type__model="event",
                    )
                except models.ObjectDoesNotExist:
                    # or create a new exhibition and then create a mapper
                    event = Event()
                else:
                    event = event_mapper.content_object
                    if not event:
                        # skip deleted events
                        self.stats["events_skipped"] += 1
                        continue

                event.production = prod

                date_str, start_time_str, end_time_str = production_dict["Termin"].split(", ")
                event.start_date = parse_datetime(date_str).date()
                event.start_time = time(*map(int, start_time_str.split(".")))

                if production_dict["Ausverkauft"] == "JA":
                    event.ticket_status = "sold_out"
                else:
                    event.ticket_status = "tickets_@_box_office"

                event.save()

                if not event_mapper:
                    event_mapper = ObjectMapper(
                        service=self.service,
                        external_id=external_prod_id,
                    )
                    event_mapper.content_object = event
                    event_mapper.save()
                    self.stats["events_added"] += 1
                else:
                    self.stats["events_updated"] += 1

        if self.verbosity >= NORMAL:
            print u"Productions added: %d" % self.stats["prods_added"]
            print u"Productions updated: %d" % self.stats["prods_updated"]
            print u"Productions skipped: %d" % self.stats["prods_skipped"]
            print u"Events added: %d" % self.stats["events_added"]
            print u"Events updated: %d" % self.stats["events_updated"]
            print u"Events skipped: %d" % self.stats["events_skipped"]
            print

