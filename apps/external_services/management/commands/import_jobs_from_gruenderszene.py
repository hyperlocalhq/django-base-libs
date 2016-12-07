# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = """Imports job offers from www.music-job.com"""

    JOB_SECTOR_MAPPER = {
        1: 7,  # IT -> Online & IT
        2: 9,  # Grafik -> Graphic Design
        3: 10,  # Marketing -> Marketing
        4: 13,  # Business Development -> Corporate - CD / CI / CC
        5: 21,  # Sales -> Sales & Support
        6: 23,  # Projektmanagement -> Management
        7: 20,  # Produktmanagement -> Product Manager
        8: 11,  # PR & Media -> PR & Event
        9: 24,  # Legal -> Other
        10: 24,  # HR -> Other
        11: 2,  # Finance -> Funding & Non-profit
        12: 24,  # Operations -> Other
        13: 7,  # Co - Founder -> Online & IT
        14: 23,  # Management -> Management
        15: 24,  # Sonstige -> Other
        16: 19,  # Redaktion -> Media & Literature
        17: 7,  # Development -> Online & IT
        18: 22,  # Customer Care -> Community Management
    }

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))

        import re
        import requests
        from datetime import timedelta
        from xml.dom.minidom import parseString
        from dateutil.parser import parse as parse_datetime

        from django.apps import apps
        from django.utils.text import force_text

        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED
        from base_libs.utils.misc import html_to_plain_text

        from jetson.apps.external_services.utils import get_value

        Address = apps.get_model("location", "Address")
        JobOffer = apps.get_model("marketplace", "JobOffer")
        JobSector = apps.get_model("marketplace", "JobSector")
        JobType = apps.get_model("marketplace", "JobType")
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")
        Service = apps.get_model("external_services", "Service")

        URL = "http://www.gruenderszene.de/jobboerse/feed?template=gehalt.de&pagination=false&"
        s, created = Service.objects.get_or_create(
            sysname="gruenderszene_jobs",
            defaults={
                'url': URL,
                'title': "www.gruenderszene.de",
            },
        )
        if not created:
            s.url = URL
            s.save()

        def textify(html):
            html = re.sub(r'<a [^>]*?href="mailto:([^"]+)"[^>]*>\1</a>', r'\1', html)  # replace mailto links with just email
            html = re.sub(r'<a [^>]*?href="(https?://)([^"]+)"[^>]*>\2</a>', r'\1\2', html)  # replace website links with just URL
            html = html.replace('<li>', u'<li> • ')  # add bullets to lines wrapped with <li>
            text = html_to_plain_text(html)
            text = re.sub(r'( • .+)\n\n', r'\1\n', text)  # replace double new-line with single new-line for bulleted items
            text = re.sub(r'\n\s+\n', '\n\n', text)  # replace multiple newlines with maximal 2 newlines
            return text

        default_job_type, created = JobType.objects.get_or_create(
            slug="full-time",
            defaults={
                'title_en': "Full-time",
                'title_de': "Vollzeit",
            },
        )

        response = requests.get(s.url)
        if response.status_code != 200:
            raise Exception("Connection error")
        xml_doc = parseString(response.content)

        counter = 1
        for node_job in xml_doc.getElementsByTagName("job"):
            location = get_value(node_job, "location")
            if "Berlin" not in location and "flexibel" not in location:
                continue

            # get or create job offer
            external_id = get_value(node_job, "id")
            try:
                change_date = parse_datetime(
                    get_value(node_job, "date"),
                    ignoretz=True,
                )
            except Exception:
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
            except ObjectMapper.MultipleObjectsReturned:
                # delete duplicates
                for mapper in s.objectmapper_set.filter(
                    external_id=external_id,
                    content_type__app_label="marketplace",
                    content_type__model="joboffer",
                ).order_by("object_id")[1:]:
                    if mapper.content_object:
                        mapper.content_object.delete()
                    mapper.delete()
                continue
            except ObjectMapper.DoesNotExist:
                # or create a new job offer and then create a mapper
                job_offer = JobOffer()

            job_offer.modified_date = change_date

            job_offer.position = get_value(node_job, "title")
            job_offer.description = textify(get_value(node_job, "description"))
            job_offer.job_type = default_job_type
            job_offer.offering_institution_title = get_value(node_job, "company")

            job_offer.url0_link = get_value(node_job, "url")
            job_offer.is_commercial = False

            if change_date:
                job_offer.published_from = change_date
            else:
                job_offer.published_from = parse_datetime(
                    get_value(node_job, "date"),
                    ignoretz=True,
                )
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

            # add job sector

            job_offer.job_sectors.clear()
            for cat_id in get_value(node_job, "categories").strip().split(","):
                try:
                    job_sector = JobSector.objects.get(pk=self.JOB_SECTOR_MAPPER[int(cat_id)])
                except:
                    pass
                else:
                    job_offer.job_sectors.add(job_sector)

            if verbosity > NORMAL:
                self.stdout.write(u"{}. {}".format(counter, force_text(job_offer)))
            counter += 1

            if not mapper:
                mapper = ObjectMapper(
                    service=s,
                    external_id=external_id,
                )
                mapper.content_object = job_offer
                mapper.save()
