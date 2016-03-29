# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = """Imports job offers from Creativeset.net"""

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))

        import requests
        from datetime import timedelta
        from xml.dom.minidom import parseString
        from dateutil.parser import parse as parse_datetime

        from django.apps import apps
        from django.db import IntegrityError

        from base_libs.utils.misc import html_to_plain_text
        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

        from jetson.apps.external_services.utils import get_value

        Address = apps.get_model("location", "Address")
        JobOffer = apps.get_model("marketplace", "JobOffer")
        JobType = apps.get_model("marketplace", "JobType")
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")
        Service = apps.get_model("external_services", "Service")
        URLType = apps.get_model("optionset", "URLType")

        s, created = Service.objects.get_or_create(
            sysname="creativeset",
            defaults={
                'url': "http://www.creativeset.net/feeds/rss_extended/de/jobs.xml",
                'title': "Creativeset.net",
            },
        )

        default_job_type, created = JobType.objects.get_or_create(
            slug="full-time",
            defaults={
                'title_en': "Full-time",
                'title_de': "Vollzeit",
            },
        )

        default_urltype, created = URLType.objects.get_or_create(
            slug="creativesetnet",
            defaults={
                'title_en': "Creativeset.net",
                'title_de': "Creativeset.net",
            },
        )

        response = requests.get(s.url)
        if response.status_code != 200:
            print "Broken feed link: %s (status_code=%s)" % (s.url, response.status_code)
            return

        xml_doc = parseString(response.content)

        for node_job in xml_doc.getElementsByTagName("item"):
            # get or create job offer
            external_id = get_value(node_job, "id")
            try:
                change_date = parse_datetime(
                    get_value(node_job, "changeDate"),
                    ignoretz=True,
                )
            except Exception:
                change_date = None
            city = get_value(node_job, "city")
            if city != "Berlin":
                continue
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
            job_offer.description = "\n\n".join((
                html_to_plain_text(get_value(node_job, "description")),
                html_to_plain_text(get_value(node_job, "company_description")),
                html_to_plain_text(get_value(node_job, "how_to_apply")),
            ))
            job_offer.offering_institution_title = get_value(node_job, "company_name")

            job_offer.url0_link = get_value(node_job, "link")
            job_offer.url0_type = default_urltype

            if change_date:
                job_offer.published_from = change_date
            else:
                job_offer.published_from = parse_datetime(
                    get_value(node_job, "pubDate"),
                    ignoretz=True,
                )
            published_till = get_value(node_job, "visible_until")
            if published_till:
                job_offer.published_till = parse_datetime(
                    published_till,
                    ignoretz=True,
                )
            else:
                job_offer.published_till = job_offer.published_from + timedelta(days=7 * 6)
            job_offer.status = STATUS_CODE_PUBLISHED

            # set job type

            job_offer.job_type = default_job_type
            for node_job_type in node_job.getElementsByTagName("experience"):
                try:
                    job_type = s.objectmapper_set.get(
                        external_id=get_value(node_job_type),
                        content_type__app_label="marketplace",
                        content_type__model="jobtype",
                    ).content_object
                except Exception:
                    pass
                else:
                    job_offer.job_type = job_type
                    break

            job_offer.save()

            # add job sectors

            job_offer.job_sectors.clear()
            for node_sector in node_job.getElementsByTagName("branch"):
                try:
                    job_sector = s.objectmapper_set.get(
                        external_id=get_value(node_sector, "name"),
                        content_type__app_label="marketplace",
                        content_type__model="jobsector",
                    ).content_object
                except Exception:
                    pass
                else:
                    try:
                        job_offer.job_sectors.add(job_sector)
                    except IntegrityError:
                        pass

            # add job qualifications

            job_offer.qualifications.clear()
            for node_qual in node_job.getElementsByTagName("experience"):
                try:
                    qualification = s.objectmapper_set.get(
                        external_id=get_value(node_qual),
                        content_type__app_label="marketplace",
                        content_type__model="jobqualification",
                    ).content_object
                except Exception:
                    pass
                else:
                    try:
                        job_offer.qualifications.add(qualification)
                    except IntegrityError:
                        pass

            # add address

            Address.objects.set_for(
                job_offer,
                "postal_address",
                country="DE",
                city="Berlin",
            )

            if verbosity > NORMAL:
                print job_offer.__dict__

            if not mapper:
                mapper = ObjectMapper(
                    service=s,
                    external_id=external_id,
                )
                mapper.content_object = job_offer
                mapper.save()

                if verbosity > NORMAL:
                    print mapper.__dict__
