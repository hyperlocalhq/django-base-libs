# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = """Imports job offers from www.music-job.com"""

    def handle(self, *args, **options):
        return  # TODO: music job links are somewhat broken

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
        Category = apps.get_model("structure", "Category")

        s, created = Service.objects.get_or_create(
            sysname="musicjob",
            defaults={
                'url': "http://www.music-job.com/index.php?id=129&type=5003&tx_mnmboerse_pi2[stadt]=berlin",
                'title': "www.music-job.com",
            },
        )

        default_job_type, created = JobType.objects.get_or_create(
            slug="full-time",
            defaults={
                'title_en': "Full-time",
                'title_de': "Vollzeit",
            },
        )

        default_job_sector, created = JobSector.objects.get_or_create(
            slug="music-scene",
            defaults={
                'title_en': "Music & Scene",
                'title_de': "Musik & Bühne",
            },
        )

        default_categories = list(Category.objects.filter(
            slug__in=("musik",)
        ))

        if verbosity > NORMAL:
            self.stdout.write("Importing jobs from musicjob\n")
            self.stdout.flush()

        response = requests.get(s.url)
        try:
            xml_doc = parseString(response.content)
        except Exception:
            self.stderr.write("Error parsing XML\n")
            return

        for node_job in xml_doc.getElementsByTagName("item"):

            # get or create job offer
            external_id = get_value(node_job, "guid")
            if verbosity > NORMAL:
                self.stdout.write(" - {}\n".format(get_value(node_job, "title")))

            try:
                change_date = parse_datetime(
                    get_value(node_job, "pubDate"),
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

            job_offer.description = get_value(node_job, "description")
            job_offer.job_type = default_job_type

            job_offer.url0_link = get_value(node_job, "link")
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
            job_offer.job_sectors.add(default_job_sector)

            # add job categories

            job_offer.categories.clear()
            job_offer.categories.add(*default_categories)

            if not mapper:
                mapper = ObjectMapper(
                    service=s,
                    external_id=external_id,
                )
                mapper.content_object = job_offer
                mapper.save()
