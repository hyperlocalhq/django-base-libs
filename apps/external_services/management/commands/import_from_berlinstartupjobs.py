# -*- coding: UTF-8 -*-
from optparse import make_option
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    help = """Imports job offers from Creativeset.net"""

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))

        from datetime import datetime, timedelta
        from time import strptime
        from rest.client import webcall
        from xml.dom.minidom import parseString
        from xml.dom.minidom import Node
        from dateutil.parser import parse as parse_datetime

        from django.db import models

        from base_libs.utils.misc import get_related_queryset
        from base_libs.utils.misc import html_to_plain_text
        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED
        from base_libs.templatetags.base_tags import decode_entities

        from jetson.apps.external_services.utils import get_first
        from jetson.apps.external_services.utils import get_value

        Address = models.get_model("location", "Address")
        JobOffer = models.get_model("marketplace", "JobOffer")
        JobSector = models.get_model("marketplace", "JobSector")
        JobType = models.get_model("marketplace", "JobType")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Service = models.get_model("external_services", "Service")
        URLType = models.get_model("optionset", "URLType")

        job_sector_online_it, created = JobSector.objects.get_or_create(
            slug="online-it",
            defaults={
                'title_en': u"Online & IT",
                'title_de': u"Online & IT",
            },
        )
        job_sector_graphic_design, created = JobSector.objects.get_or_create(
            slug="graphic-design",
            defaults={
                'title_en': u"Graphic Design",
                'title_de': u"Grafik Design",
            },
        )
        job_sector_corporate, created = JobSector.objects.get_or_create(
            slug="corporate-cd-ci-cc",
            defaults={
                'title_en': u"Corporate - CD / CI / CC",
                'title_de': u"Corporate - CD / CI / CC",
            },
        )
        job_sector_games, created = JobSector.objects.get_or_create(
            slug="games",
            defaults={
                'title_en': u"Games",
                'title_de': u"Games",
            },
        )
        job_sector_package_design, created = JobSector.objects.get_or_create(
            slug="package-design",
            defaults={
                'title_en': u"Package Design",
                'title_de': u"Package Design",
            },
        )
        job_sector_advertising, created = JobSector.objects.get_or_create(
            slug="advertising",
            defaults={
                'title_en': u"Advertising",
                'title_de': u"Werbung",
            },
        )
        job_sector_marketing, created = JobSector.objects.get_or_create(
            slug="marketing",
            defaults={
                'title_en': u"Marketing",
                'title_de': u"Marketing",
            },
        )
        job_sector_product_manager, created = JobSector.objects.get_or_create(
            slug="product-manager",
            defaults={
                'title_en': u"Product Manager",
                'title_de': u"Product Manager",
            },
        )
        job_sector_sales_support, created = JobSector.objects.get_or_create(
            slug="sales-support",
            defaults={
                'title_en': u"Sales & Support",
                'title_de': u"Sales & Support",
            },
        )
        job_sector_community_management, created = JobSector.objects.get_or_create(
            slug="community-management",
            defaults={
                'title_en': u"Community Management",
                'title_de': u"Community Management",
            },
        )
        job_sector_management, created = JobSector.objects.get_or_create(
            slug="management",
            defaults={
                'title_en': u"Management",
                'title_de': u"Management",
            },
        )
        job_sector_other, created = JobSector.objects.get_or_create(
            slug="other",
            defaults={
                'title_en': u"Other",
                'title_de': u"Other",
            },
        )

        job_type_full_time, created = JobType.objects.get_or_create(
            slug="full-time",
            defaults={
                'title_en': "Full-time",
                'title_de': "Vollzeit",
            },
        )
        job_type_internship, created = JobType.objects.get_or_create(
            slug="internship",
            defaults={
                'title_en': "Internship",
                'title_de': "Praktikum",
            },
        )

        FEEDS = (
            {
                'url': "http://berlinstartupjobs.com/engineering/feed/atom/",
                'job_sectors': (job_sector_online_it,),
                'job_type': job_type_full_time,
            },
            {
                'url': "http://berlinstartupjobs.com/design-ux/feed/atom/",
                'job_sectors': (job_sector_online_it, job_sector_graphic_design, job_sector_corporate, job_sector_games,
                                job_sector_package_design),
                'job_type': job_type_full_time,
            },
            {
                'url': "http://berlinstartupjobs.com/marketing/feed/atom/",
                'job_sectors': (job_sector_advertising, job_sector_marketing),
                'job_type': job_type_full_time,
            },
            {
                'url': "http://berlinstartupjobs.com/product-management/feed/atom/",
                'job_sectors': (job_sector_product_manager,),
                'job_type': job_type_full_time,
            },
            {
                'url': "http://berlinstartupjobs.com/sales/feed/atom/",
                'job_sectors': (job_sector_sales_support,),
                'job_type': job_type_full_time,
            },
            {
                'url': "http://berlinstartupjobs.com/internships/feed/atom/",
                'job_sectors': (),
                'job_type': job_type_internship,
            },
            {
                'url': "http://berlinstartupjobs.com/community-management/feed/atom/",
                'job_sectors': (job_sector_community_management,),
                'job_type': job_type_full_time,
            },
            {
                'url': "http://berlinstartupjobs.com/management/feed/atom/",
                'job_sectors': (job_sector_management,),
                'job_type': job_type_full_time,
            },
            {
                'url': "http://berlinstartupjobs.com/seeking-co-founders/feed/atom/",
                'job_sectors': (job_sector_other,),
                'job_type': job_type_full_time,
            },
            {
                'url': "http://berlinstartupjobs.com/contracting-positions/feed/atom/",
                'job_sectors': (job_sector_other,),
                'job_type': job_type_full_time,
            },
            {
                'url': "http://berlinstartupjobs.com/other/feed/atom/",
                'job_sectors': (job_sector_other,),
                'job_type': job_type_full_time,
            },
        )

        default_urltype, created = URLType.objects.get_or_create(
            slug="berlinstartupjobs",
            defaults={
                'title_en': "berlinstartupjobs.com",
                'title_de': "berlinstartupjobs.com",
            },
        )

        s, created = Service.objects.get_or_create(
            sysname="berlinstartupjobs",
            defaults={
                'url': "http://berlinstartupjobs.com/feed/atom/",
                'title': "berlinstartupjobs.com",
            },
        )

        for feed_settings in FEEDS:

            @webcall(url=feed_settings['url'])
            def get_berlinstartupjobs_data():
                pass

            data = get_berlinstartupjobs_data()

            try:
                xml_doc = parseString(data)
            except:
                return

            for node_job in xml_doc.getElementsByTagName("entry"):
                # get or create job offer
                external_id = get_value(node_job, "id")
                try:
                    change_date = parse_datetime(
                        get_value(node_job, "published"),
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

                job_offer.position, job_offer.offering_institution_title = get_value(node_job, "title").split(" // ")

                summary = get_value(node_job, "summary")
                if "[...]" in summary:
                    summary = summary.split("[...]")[0] + "[...]"

                job_offer.description = decode_entities(summary, decode_all=True)

                job_offer.job_type = feed_settings['job_type']

                job_offer.url0_link = get_first(node_job, "link").getAttribute("href")
                job_offer.url0_type = default_urltype
                job_offer.is_commercial = False

                if change_date:
                    job_offer.published_from = change_date
                else:
                    job_offer.published_from = parse_datetime(
                        get_value(node_job, "published"),
                        ignoretz=True,
                    )
                job_offer.published_till = job_offer.published_from + timedelta(days=7 * 6)
                job_offer.status = STATUS_CODE_PUBLISHED
                job_offer.save()

                if verbosity > NORMAL:
                    print job_offer.__dict__


                # add address
                Address.objects.set_for(
                    job_offer,
                    "postal_address",
                    country="DE",
                    city="Berlin",
                )

                # add job sectors
                job_offer.job_sectors.clear()
                for js in feed_settings['job_sectors']:
                    job_offer.job_sectors.add(js)

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
