# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    SILENT, NORMAL, VERBOSE = 0, 1, 2
    help = """Imports job offers from www.games-career.com"""

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity', self.NORMAL))
        
        self.initialize()
        self.main()
        self.finalize()
    
    def initialize(self):
        from django.apps import apps
        JobSector = apps.get_model("marketplace", "JobSector")
        JobType = apps.get_model("marketplace", "JobType")
        Service = apps.get_model("external_services", "Service")
        Category = apps.get_model("structure", "Category")

        self.stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
        }

        URL = "https://www.games-career.com/jobRobot/kulturprojekte.xml"
        SERVICE_TITLE = "Games-Career"
        self.service, created = Service.objects.get_or_create(
            sysname="games_career",
            defaults={
                'url': URL,
                'title': SERVICE_TITLE,
            },
        )
        if self.service.url != URL or self.service.title != SERVICE_TITLE:
            self.service.url = URL
            self.service.title = SERVICE_TITLE
            self.service.save()

        self.JOB_TYPES = {
            u'Full-time': JobType.objects.get(slug="full-time"),
            u'Internship': JobType.objects.get(slug="internship"),
            u'Traineeship': JobType.objects.get(slug="trainee"),
            u'Part-time': JobType.objects.get(slug="part-time"),
            u'*': JobType.objects.get(slug="not-available"),
        }

        self.default_job_sector, created = JobSector.objects.get_or_create(
            slug="games",
            defaults={
                'title_en': "Games",
                'title_de': "Games",
            },
        )

        self.default_categories = list(Category.objects.filter(
            slug__in=("games-interactive",)
        ))

    def main(self):
        import requests
        from datetime import datetime
        from datetime import timedelta
        from xml.dom.minidom import parseString
        from dateutil.parser import parse as parse_datetime

        from django.apps import apps

        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

        from jetson.apps.external_services.utils import get_value, get_child_text

        Address = apps.get_model("location", "Address")
        JobOffer = apps.get_model("marketplace", "JobOffer")
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")

        if self.verbosity >= self.NORMAL:
            self.stdout.write("Importing jobs from musicjob\n")
            self.stdout.flush()

        response = requests.get(self.service.url)
        try:
            xml_doc = parseString(response.content)
        except Exception:
            self.stderr.write("Error parsing XML\n")
            return

        total = len(xml_doc.getElementsByTagName("joboffer"))

        for index1, node_job in enumerate(xml_doc.getElementsByTagName("joboffer"), 1):

            # get or create job offer
            external_id = get_value(node_job, "id").strip()
            position = get_value(node_job, "position").strip()

            if self.verbosity >= self.NORMAL:
                self.stdout.write(u"{}/{}. {} (external_id={})".format(index1, total, position, external_id))
                self.stdout.flush()

            city = get_value(node_job, "city").strip()
            if city != "Berlin":
                self.stats['skipped'] += 1
                continue

            try:
                change_date = parse_datetime(
                    get_value(node_job, "date_published"),
                    ignoretz=True,
                )
            except Exception:
                change_date = None
            mapper = None
            try:
                # get job offer from saved mapper
                mapper = self.service.objectmapper_set.get(
                    external_id=external_id,
                    content_type__app_label="marketplace",
                    content_type__model="joboffer",
                )
                job_offer = mapper.content_object
                if job_offer.modified_date > change_date:
                    self.stats['skipped'] += 1
                    continue
                self.stats['updated'] += 1
            except ObjectMapper.MultipleObjectsReturned:
                # delete duplicates
                for mapper in self.service.objectmapper_set.filter(
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
                self.stats['added'] += 1

            job_offer.modified_date = change_date

            job_offer.position = position
            job_offer.offering_institution_title = get_value(node_job, "company").strip()
            job_offer.contact_person_name = get_value(node_job, "contact").strip()

            job_offer.description = get_value(node_job, "description").strip()

            job_offer.job_type = self.JOB_TYPES.get(get_value(node_job, "type").strip()) or self.JOB_TYPES['*']

            job_offer.url0_link = get_value(node_job, "link")
            job_offer.is_commercial = False

            job_offer.published_from = change_date or datetime.now()
            job_offer.published_till = job_offer.published_from + timedelta(days=7 * 6)
            job_offer.status = STATUS_CODE_PUBLISHED
            job_offer.save()

            # add address

            Address.objects.set_for(
                job_offer,
                "postal_address",
                postal_code=get_value(node_job, "postalcode").strip(),
                country="DE",
                city="Berlin",
            )

            # add job sector

            job_offer.job_sectors.clear()
            job_offer.job_sectors.add(self.default_job_sector)

            # add job categories

            job_offer.categories.clear()
            job_offer.categories.add(*self.default_categories)

            if not mapper:
                mapper = ObjectMapper(
                    service=self.service,
                    external_id=external_id,
                )
                mapper.content_object = job_offer
                mapper.save()

    def finalize(self):
        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Results ===\n")
            self.stdout.write(u"Jobs added: {}\n".format(self.stats['added']))
            self.stdout.write(u"Jobs updated: {}\n".format(self.stats['updated']))
            self.stdout.write(u"Jobs skipped: {}\n".format(self.stats['skipped']))
