# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.utils.encoding import force_text



class Command(BaseCommand):
    SILENT, NORMAL, VERBOSE = 0, 1, 2
    help = """Imports job offers from www.medianet-bb.de"""

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity', self.NORMAL))

        self.initialize()
        self.main()
        self.finalize()

    def initialize(self):
        from django.apps import apps
        JobSector = apps.get_model("marketplace", "JobSector")
        JobType = apps.get_model("marketplace", "JobType")
        JobQualification = apps.get_model("marketplace", "JobQualification")
        Service = apps.get_model("external_services", "Service")

        URL = "https://www.medianet-bb.de/wp-json/wp/v2/job"
        SERVICE_TITLE = "medianet"
        self.service, created = Service.objects.get_or_create(
            sysname="theaterjobs",
            defaults={
                'url': URL,
                'title': SERVICE_TITLE,
            },
        )
        if self.service.url != URL or self.service.title != SERVICE_TITLE:
            self.service.url = URL
            self.service.title = SERVICE_TITLE
            self.service.save()

        self.JOB_SECTOR_MAPPING = {
            13834: JobSector.objects.get(pk=3),   # Medien- und Kreativwirtschaft / Kultur ➔ Kulturwirtschaft
            13835: JobSector.objects.get(pk=9),   # Mediengestaltung / Grafikdesign ➔ Grafik Design
            13836: JobSector.objects.get(pk=11),  # Journalismus / PR / Öffentlichkeitsarbeit / Redaktion ➔ PR & Event
            13837: JobSector.objects.get(pk=10),  # Marketing / Mobile / SEO ➔ Marketing
            13838: JobSector.objects.get(pk=20),  # Projektmanagement / Office Management / Administration ➔ Product Manager
            13839: JobSector.objects.get(pk=19),  # Publishing / Buchhandel / Verlage / Druckbranche ➔ Medien & Literatur
            13840: JobSector.objects.get(pk=16),  # TV / Film / Radio / Fotografie ➔ TV / Film
            13841: JobSector.objects.get(pk=14),  # Games / Development / Gamedesign / Producer ➔ Games
            13842: JobSector.objects.get(pk=7),   # Softwareentwicklung / Data Analytics / Systemintegration ➔ Online & IT
            13843: JobSector.objects.get(pk=7),   # IT-Entwicklung / IT-Berater / IT Administration / Webdesign ➔ Online & IT
            13847: JobSector.objects.get(pk=22),  # Human Resources / Personalentwicklung ➔ Community Management
            13937: JobSector.objects.get(pk=11),  # Marketing / Kommunikation / Event ➔ PR & Event
            13946: JobSector.objects.get(pk=13),  # Business Development / Entrepreneurship ➔ Corporate - CD / CI / CC
            13953: JobSector.objects.get(pk=24),  # Buchhaltung ➔ Andere
            13973: JobSector.objects.get(pk=21),  # Vertrieb / Sales / Accounting / Management ➔ Sales & Support
            13983: JobSector.objects.get(pk=24),  # Medienrecht / Personalrecht ➔ Sales & Support
        }

        self.JOB_TYPE_MAPPING = {
            13777: JobType.objects.get(pk=1),   # Praktikum ➔ Praktikum
            13780: JobType.objects.get(pk=10),  # Trainee ➔ Volontariat/Trainee
            13781: JobType.objects.get(pk=3),   # Werkstudent ➔ Studentische Aushilfe
            13782: JobType.objects.get(pk=4),   # Festanstellung ➔ Vollzeit
        }

        self.JOB_QUALIFICATION_MAPPING = {
            13784: JobQualification.objects.get(pk=2), # Middle ➔ Middle
            13785: JobQualification.objects.get(pk=3), # Senior ➔ Senior
            13783: JobQualification.objects.get(pk=1), # Junior ➔ Junior
            13786: JobQualification.objects.get(pk=4), # Führungserfahrung ➔ N/A
        }

        self.index1 = 1

    def main(self):
        import requests

        response = requests.get(self.service.url)
        if response.status_code != requests.codes.OK:
            self.stderr.write('Error loading the {}. Status code: {}'.format(self.service.url, response.status_code))
            return

        self.total_jobs = int(response.headers['X-WP-Total'])
        self.total_pages = int(response.headers['X-WP-TotalPages'])

        data = response.json()
        self.save_page(data)

        for page in range(2, self.total_pages + 1):
            url = "https://www.medianet-bb.de/wp-json/wp/v2/job?page={}".format(page)
            response = requests.get(url)
            if response.status_code != requests.codes.OK:
                self.stderr.write('Error loading the {}. Status code: {}'.format(self.service.url, response.status_code))
                return
            data = response.json()
            self.save_page(data)

    def save_page(self, data):
        for job_dict in data:
            self.stdout.write('{}/{}. {}\n'.format(self.index1, self.total_jobs, job_dict['title']['rendered']))
            self.stdout.flush()
            self.save_job(job_dict)
            self.index1 += 1

    def save_job(self, job_dict):
        from dateutil.parser import parse as parse_datetime
        from datetime import timedelta
        from django.apps import apps
        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

        ObjectMapper = apps.get_model("external_services", "ObjectMapper")
        JobOffer = apps.get_model("marketplace", "JobOffer")
        Address = apps.get_model("location", "Address")

        external_id = job_dict['id']
        try:
            change_date = parse_datetime(job_dict['modified'], ignoretz=True)
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
                return
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
            return
        except ObjectMapper.DoesNotExist:
            # or create a new job offer and then create a mapper
            job_offer = JobOffer()

        job_offer.modified_date = change_date

        offering_institution_title, position = job_dict['title']['rendered'].split(': ', 1)

        job_offer.offering_institution_title = offering_institution_title
        job_offer.position = position
        job_offer.description = job_dict['content']['rendered']
        job_offer.job_type = self.JOB_TYPE_MAPPING.get(job_dict['beschaeftigungsarten'][0])

        job_offer.url0_link = job_dict['link']
        job_offer.is_commercial = False

        if change_date:
            job_offer.published_from = change_date
        else:
            job_offer.published_from = parse_datetime(job_dict['date'], ignoretz=True)

        job_offer.published_till = job_offer.published_from + timedelta(days=7 * 6)
        job_offer.status = STATUS_CODE_PUBLISHED
        job_offer.save()

        # add address

        Address.objects.set_for(
            job_offer,
            "postal_address",
            country="DE",
            city="Berlin",
        )

        # add job sectors

        job_offer.job_sectors.clear()
        job_offer.job_sectors.add([self.JOB_SECTOR_MAPPING[sector_id] for sector_id in job_dict['branche']])

        # add job qualifications

        job_offer.qualifications.clear()
        job_offer.qualifications.add([self.JOB_QUALIFICATION_MAPPING[qual_id] for qual_id in job_dict['berufserfahrungen']])

        if not mapper:
            mapper = ObjectMapper(
                service=self.service,
                external_id=external_id,
            )
            mapper.content_object = job_offer
            mapper.save()

    def finalize(self):
        pass