# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = """Imports job offers from Kulturmanagement.net"""

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        import requests
        from xml.dom.minidom import parseString

        from django.db import models

        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

        from jetson.apps.external_services.utils import get_value

        Address = models.get_model("location", "Address")
        JobOffer = models.get_model("marketplace", "JobOffer")
        JobType = models.get_model("marketplace", "JobType")
        JobQualification = models.get_model("marketplace", "JobQualification")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Service = models.get_model("external_services", "Service")
        URLType = models.get_model("optionset", "URLType")

        s, created = Service.objects.get_or_create(
            sysname="kulturmanagement",
            defaults={
                'url': "http://www.kulturmanagement.net/user_config/KmNet/packages/LANCE_Basics/exporter/export_creative_city.php",
                'title': "Kulturmanagement.net",
            },
        )

        default_job_type, created = JobType.objects.get_or_create(
            slug="not-available",
            defaults={
                'title_en': "N/A",
                'title_de': "N/A",
            },
        )

        default_urltype, created = URLType.objects.get_or_create(
            slug="kulturmanagementnet",
            defaults={
                'title_en': "Kulturmanagement.net",
                'title_de': "Kulturmanagement.net",
            },
        )

        response = requests.get(s.url)
        if response.status_code != 200:
            print "Broken feed link: %s (status_code=%s)" % (s.url, response.status_code)
            return

        xml_doc = parseString(response.content)

        for node_job in xml_doc.getElementsByTagName("Jobangebot"):
            # get or create job offer
            external_id = get_value(node_job, "Externe_Id")
            try:
                # get job offer from saved mapper
                mapper = s.objectmapper_set.get(
                    external_id=external_id,
                    content_type__app_label="marketplace",
                    content_type__model="joboffer",
                )
                job_offer = mapper.content_object
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
                job_offer.position = get_value(node_job, "Jobname")
                job_offer.description = "N/A"

                job_offer.url0_link = get_value(node_job, "Detaillink")
                job_offer.url0_type = default_urltype
                if "v__exdet" in job_offer.url0_link:
                    job_offer.is_commercial = True

                job_offer.published_from = get_value(node_job, "Startzeit")
                job_offer.published_till = get_value(node_job, "Endzeit")
                job_offer.status = STATUS_CODE_PUBLISHED

                try:
                    job_type = s.objectmapper_set.get(
                        external_id=get_value(node_job, "Anstellungsart"),
                        content_type__app_label="marketplace",
                        content_type__model="jobtype",
                    ).content_object
                except Exception:
                    job_offer.job_type = default_job_type
                else:
                    job_offer.job_type = job_type

                job_offer.save()

                try:
                    job_sector = s.objectmapper_set.get(
                        external_id=get_value(node_job, "Sparte"),
                        content_type__app_label="marketplace",
                        content_type__model="jobsector",
                    ).content_object
                except Exception:
                    pass
                else:
                    job_offer.job_sectors.add(job_sector)

                Address.objects.set_for(
                    job_offer,
                    "postal_address",
                    country="DE",
                    city="Berlin",
                )

                if verbosity > NORMAL:
                    print job_offer.__dict__

                mapper = ObjectMapper(
                    service=s,
                    external_id=external_id,
                )
                mapper.content_object = job_offer
                mapper.save()

                if verbosity > NORMAL:
                    print mapper.__dict__
