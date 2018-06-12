# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    help = """Imports job offers from jobwrk.com"""

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))

        import requests
        from datetime import timedelta
        from xml.dom.minidom import parseString
        from dateutil.parser import parse as parse_datetime

        from django.apps import apps
        from django.db import transaction
        from django.db import models
        from django.utils.html import strip_tags

        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

        from jetson.apps.external_services.utils import get_value

        Address = apps.get_model("location", "Address")
        JobOffer = apps.get_model("marketplace", "JobOffer")
        JobType = apps.get_model("marketplace", "JobType")
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")
        Service = apps.get_model("external_services", "Service")
        URLType = apps.get_model("optionset", "URLType")

        stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
            'deleted': 0,
        }

        URL = "https://jobwrk.com/job_feed?job_region=269"
        s, created = Service.objects.get_or_create(
            sysname="jobwrk_jobs",
            defaults={
                'url': URL,
                'title': "JOBWRK",
            },
        )
        if s.url != URL:
            s.url = URL
            s.save()

        JOB_TYPES = {
            u'Festanstellung': JobType.objects.get(slug="full-time"),
            u'Freie Mitarbeit': JobType.objects.get(slug="freelance"),
            u'Sonstiges': JobType.objects.get(slug="not-available"),
        }

        default_urltype, created = URLType.objects.get_or_create(
            slug="jobwrk",
            defaults={
                'title_de': "JOBWRK",
            },
        )

        if verbosity > NORMAL:
            self.stdout.write("Reading the feed at {}\n".format(s.url))
            self.stdout.flush()

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

        if verbosity > NORMAL:
            self.stdout.write("Parsing XML document...\n")
            self.stdout.flush()

        xml_doc = parseString(data)

        total = len(xml_doc.getElementsByTagName("item"))

        if verbosity > NORMAL:
            self.stdout.write("Saving job offers...\n")
            self.stdout.flush()

        for index, node_job in enumerate(xml_doc.getElementsByTagName("item"), 1):

            # get or create job offer
            external_id = get_value(node_job, "guid")
            position = get_value(node_job, "title")

            if verbosity > NORMAL:
                self.stdout.write("{}/{}. {} (external_id={})".format(index, total, position, external_id))
                self.stdout.flush()

            try:
                change_date = parse_datetime(
                    get_value(node_job, "pubDate"),
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
                if not job_offer:
                    stats['skipped'] += 1
                    continue
                #if job_offer.modified_date > change_date:
                #    stats['skipped'] += 1
                #    continue
                stats['updated'] += 1
            except models.ObjectDoesNotExist:
                # or create a new job offer and then create a mapper
                job_offer = JobOffer()
                stats['added'] += 1

            job_offer.modified_date = change_date

            job_offer.position = position
            job_offer.description = strip_tags(get_value(node_job, "description")).replace("\n", "\n\n")
            job_offer.job_type = JOB_TYPES.get(
                get_value(node_job, "job_listing:job_type"),
                JOB_TYPES['Sonstiges'],
            )

            job_offer.url0_link = get_value(node_job, "link")
            job_offer.url0_type = default_urltype
            job_offer.is_commercial = False

            if change_date:
                job_offer.published_from = change_date
            else:
                job_offer.published_from = parse_datetime(
                    get_value(node_job, "pubDate"),
                    ignoretz=True,
                )
            job_offer.published_till = job_offer.published_from + timedelta(days=7 * 6)
            job_offer.status = STATUS_CODE_PUBLISHED
            #job_offer.offering_institution_title = get_value(node_job, "company")

            job_offer.save()

            # add address

            Address.objects.set_for(
                job_offer,
                "postal_address",
                country="DE",
                city="Berlin",
            )

            if not mapper:
                mapper = ObjectMapper(
                    service=s,
                    external_id=external_id,
                )
                mapper.content_object = job_offer
                mapper.save()

            transaction.commit()

        if verbosity >= NORMAL:
            self.stdout.write(u"=== Results ===\n")
            self.stdout.write(u"Jobs added: {}\n".format(stats['added']))
            self.stdout.write(u"Jobs updated: {}\n".format(stats['updated']))
            self.stdout.write(u"Jobs skipped: {}\n".format(stats['skipped']))
            self.stdout.write(u"Jobs deleted: {}\n".format(stats['deleted']))
            self.stdout.write("\nFinishing...\n")
            self.stdout.flush()
