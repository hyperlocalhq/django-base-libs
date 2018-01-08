# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    help = """Imports job offers from dasauge.com"""

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))

        import requests
        from datetime import timedelta
        from xml.dom.minidom import parseString
        from dateutil.parser import parse as parse_datetime

        from django.apps import apps

        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

        from jetson.apps.external_services.utils import get_value

        Address = apps.get_model("location", "Address")
        JobOffer = apps.get_model("marketplace", "JobOffer")
        JobSector = apps.get_model("marketplace", "JobSector")
        JobType = apps.get_model("marketplace", "JobType")
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")
        Service = apps.get_model("external_services", "Service")
        URLType = apps.get_model("optionset", "URLType")

        s, created = Service.objects.get_or_create(
            sysname="dasauge_jobs",
            defaults={
                'url': "https://api.dasauge.net/jobfeed/?key=10888a51c8246e86fed6d5626d992f620f39c357&location=10115&distance=90",
                'title': "dasauge.de",
            },
        )

        JOB_TYPES = {
            u'Fest': JobType.objects.get(slug="full-time"),
            u'Praktikum': JobType.objects.get(slug="internship"),
            u'Freelancer': JobType.objects.get(slug="freelance"),
        }

        default_urltype, created = URLType.objects.get_or_create(
            slug="dasauge",
            defaults={
                'title_de': "dasauge.de",
            },
        )
        default_job_sectors = list(JobSector.objects.filter(
            slug__in=("graphic-design", "advertising"),
        ))

        try:
            response = requests.get(
                s.url,
                allow_redirects=True,
                verify=False,
                headers={
                    'User-Agent': 'Creative City Berlin',
                }
            )
        except:
            self.stderr.write("ERROR: {}\n".format(s.url))
            return
        if response.status_code != requests.codes.ok:
            self.stderr.write("ERROR: {}\n".format(s.url))
            return
        data = response.content

        xml_doc = parseString(data)

        for node_job in xml_doc.getElementsByTagName("item"):

            # get or create job offer
            external_id = get_value(node_job, "url")
            try:
                change_date = parse_datetime(
                    get_value(node_job, "edited"),
                    ignoretz=True,
                )
            except:
                change_date = None
            mapper = None
            try:
                # get job offer from saved mapper
                mapper = s.objectmapper_set.get(
                    external_id=external_id,
                    content_type__app_label="marketplace",
                    content_type__model="joboffer",
                )
                job_offer = mapper.content_object
                if job_offer.modified_date > change_date:
                    continue
            except:
                # or create a new job offer and then create a mapper
                job_offer = JobOffer()

            job_offer.modified_date = change_date

            job_offer.position = get_value(node_job, "title")
            job_offer.description = get_value(node_job, "details")
            job_offer.job_type = JOB_TYPES.get(get_value(node_job, "type"), None)

            job_offer.url0_link = get_value(node_job, "url")
            job_offer.url0_type = default_urltype
            job_offer.is_commercial = False

            if change_date:
                job_offer.published_from = change_date
            else:
                job_offer.published_from = parse_datetime(
                    get_value(node_job, "edited"),
                    ignoretz=True,
                )
            job_offer.published_till = job_offer.published_from + timedelta(days=7 * 6)
            job_offer.status = STATUS_CODE_PUBLISHED
            job_offer.offering_institution_title = get_value(node_job, "company")

            job_offer.save()

            # job_offer.job_sectors.clear()
            job_offer.job_sectors.add(*default_job_sectors)

            # add address

            Address.objects.set_for(
                job_offer,
                "postal_address",
                country="DE",
                city=get_value(node_job, "town"),
            )

            if verbosity > NORMAL:
                self.stdout.write(" - {} (id={})".format(job_offer, job_offer.pk))

            if not mapper:
                mapper = ObjectMapper(
                    service=s,
                    external_id=external_id,
                )
                mapper.content_object = job_offer
                mapper.save()
