# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = """Imports job offers from Kulturmanagement.net"""

    JOB_SECTOR_MAPPER = {
        # Sparte
        "1": 4,  # Bibliotheken & Archive -> Bildung & Öffentlicher Sektor
        "2": 5,  # Musik -> Musik & Bühne
        "3": 5,  # Darstellende Künste -> Musik & Bühne
        "4": 1,  # Museum & Kulturelles Erbe -> Museum & Kunst
        "5": 1,  # Kunstmarkt & Ausstellungshäuser -> Museum & Kunst
        "6": 19,  # Medien & Literatur -> Medien & Literatur
        "7": 2,  # Stiftung -> Stiftung & Nonprofit
        "8": [3, 4],  # Kulturpolitik & öffentliche Verwaltung -> Kulturwirtschaft, Bildung & Öffentlicher Sektor
        "9": 3,  # Kultur- und Kreativwirtschaft -> Kulturwirtschaft
        "10": 3,  # Soziokultur -> Kulturwirtschaft
        "11": 4,  # Hochschule & Forschung -> Bildung & Öffentlicher Sektor
        "12": 3,  # Kulturtourismus -> Kulturwirtschaft
        "13": 24,  # spartenübergreifend -> Andere
        "102": 4,  # Bildung & Gesellschaft -> Bildung & Öffentlicher Sektor
        "103": 24,  # Jobgelegenheit -> Andere
    }

    CATEGORY_MAPPER = {
        # Sparte
        #"1": ,  # Bibliotheken & Archive
        "2": 56,  # Musik -> Musik
        "3": 69,  # Darstellende Künste -> Tanz & Theater
        #"4": ,  # Museum & Kulturelles Erbe
        #"5": ,  # Kunstmarkt & Ausstellungshäuser
        "6": 43,  # Medien & Literatur -> Literatur & Verlage
        #"7": ,  # Stiftung
        #"8": ,  # Kulturpolitik & öffentliche Verwaltung
        #"9": ,  # Kultur- und Kreativwirtschaft
        #"10": ,  # Soziokultur
        #"11": ,  # Hochschule & Forschung
        #"12": ,  # Kulturtourismus
        #"13": ,  # spartenübergreifend
        #"102": ,  # Bildung & Gesellschaft
        #"103": ,  # Jobgelegenheit
    }

    JOB_TYPE_MAPPER = {
        # Anstellungart
        "41": 4,  # Vollzeit unbefristet -> Vollzeit
        "42": 2,  # Teilzeit befristet -> Befristet
        "43": 2,  # Vollzeit befristet -> Befristet
        "44": 6,  # Teilzeit unbefristet -> Teilzeit
        "114": 8,  # Honorarbasis -> Freie Mitarbeit

        # Beschäftigungsart
        # "48": ,  # Anstellung -> see Anstellungsart
        "49": 10,  # Volontariat/ Trainee -> Volontariat/Trainee
        "50": 1,  # Praktikum -> Praktikum
        "51": 5,  # Minijob -> N/A
        "52": 2,  # Kurzzeit -> Befristet
        "53": 8,  # freie Mitarbeit -> Freie Mitarbeit
        "54": 2,  # Werkvertrag -> Befristet
        "55": 5,  # Stipendium -> N/A
    }

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity', NORMAL))

        self.prepare()
        self.main()
        self.finalize()

    def prepare(self):
        from django.apps import apps

        JobType = apps.get_model("marketplace", "JobType")
        Service = apps.get_model("external_services", "Service")

        URL = "https://www.kulturmanagement.net/creative_city_jobs.xml"
        service, created = Service.objects.get_or_create(
            sysname="kulturmanagement",
            defaults={
                'url': URL,
                'title': "Kulturmanagement.net",
            },
        )
        if service.url != URL:
            service.url = URL
            service.save()

        self.service = service

        self.default_job_type, created = JobType.objects.get_or_create(
            slug="not-available",
            defaults={
                'title_en': "N/A",
                'title_de': "N/A",
            },
        )

        self.stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
            'deleted': 0,
        }

    def main(self):
        import requests
        from xml.dom.minidom import parseString

        from django.apps import apps

        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

        from jetson.apps.external_services.utils import get_value

        Address = apps.get_model("location", "Address")
        JobOffer = apps.get_model("marketplace", "JobOffer")
        JobSector = apps.get_model("marketplace", "JobSector")
        JobType = apps.get_model("marketplace", "JobType")
        Category = apps.get_model("structure", "Category")
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")

        service = self.service

        response = requests.get(service.url)
        if response.status_code != 200:
            self.stderr.write("Broken feed link: %s (status_code=%s)" % (service.url, response.status_code))
            return

        xml_doc = parseString(response.content)

        total = len(xml_doc.getElementsByTagName("Jobangebot"))

        for index, node_job in enumerate(xml_doc.getElementsByTagName("Jobangebot"), 1):
            # get or create job offer
            external_id = get_value(node_job, "Externe_Id")
            position = get_value(node_job, "Jobname")
            if self.verbosity > NORMAL:
                self.stdout.write("{}/{}. {} (external_id={})".format(index, total, position, external_id))
                self.stdout.flush()

            try:
                # get job offer from saved mapper
                mapper = service.objectmapper_set.get(
                    external_id=external_id,
                    content_type__app_label="marketplace",
                    content_type__model="joboffer",
                )
                job_offer = mapper.content_object
                self.stats['skipped'] += 1
            except ObjectMapper.MultipleObjectsReturned:
                # delete duplicates
                for mapper in service.objectmapper_set.filter(
                    external_id=external_id,
                    content_type__app_label="marketplace",
                    content_type__model="joboffer",
                ).order_by("object_id")[1:]:
                    if mapper.content_object:
                        mapper.content_object.delete()
                    mapper.delete()
                self.stats['skipped'] += 1
                continue
            except ObjectMapper.DoesNotExist:
                # or create a new job offer and then create a mapper
                job_offer = JobOffer()
                job_offer.position = position
                job_offer.description = "N/A"

                job_offer.url0_link = get_value(node_job, "Detaillink")
                job_offer.is_commercial = True

                job_offer.published_from = get_value(node_job, "Startzeit")
                job_offer.published_till = get_value(node_job, "Endzeit")
                job_offer.status = STATUS_CODE_PUBLISHED

                their_id = get_value(node_job, "Beschaeftigungsart")
                if their_id == "48":
                    their_id = get_value(node_job, "Anstellungsart")
                try:
                    job_type = JobType.objects.get(
                        pk=self.JOB_TYPE_MAPPER.get(their_id)
                    )
                except JobType.DoesNotExist:
                    job_type = self.default_job_type
                job_offer.job_type = job_type

                job_offer.save()

                job_sector_ids = self.JOB_SECTOR_MAPPER.get(get_value(node_job, "Sparte"), [])
                if not isinstance(job_sector_ids, list):
                    job_sector_ids = [job_sector_ids]
                for job_sector_id in job_sector_ids:
                    try:
                        job_sector = JobSector.objects.get(pk=job_sector_id)
                    except JobSector.DoesNotExist:
                        pass
                    else:
                        job_offer.job_sectors.add(job_sector)

                try:
                    category = Category.objects.get(
                        pk=self.CATEGORY_MAPPER.get(get_value(node_job, "Sparte"))
                    )
                except Category.DoesNotExist:
                    pass
                else:
                    job_offer.categories.add(category)

                Address.objects.set_for(
                    job_offer,
                    "postal_address",
                    country="DE",
                    city="Berlin",
                )

                mapper = ObjectMapper(
                    service=service,
                    external_id=external_id,
                )
                mapper.content_object = job_offer
                mapper.save()
                self.stats['added'] += 1

    def finalize(self):
        if self.verbosity >= NORMAL:
            self.stdout.write(u"=== Results ===\n")
            self.stdout.write(u"Jobs added: {}\n".format(self.stats['added']))
            # self.stdout.write(u"Jobs updated: {}\n".format(self.stats['updated']))
            self.stdout.write(u"Jobs skipped: {}\n".format(self.stats['skipped']))
            # self.stdout.write(u"Jobs deleted: {}\n".format(self.stats['deleted']))
            self.stdout.write("\nFinishing...\n")
            self.stdout.flush()
