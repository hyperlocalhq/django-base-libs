# -*- coding: UTF-8 -*-
from optparse import make_option
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(NoArgsCommand):
    help = """Imports job offers from Creativeset.net"""
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        
        import urllib2
        from datetime import datetime, timedelta
        from time import strptime
        from xml.dom.minidom import parseString
        from xml.dom.minidom import Node
        from dateutil.parser import parse as parse_datetime
        
        from django.db import models

        from base_libs.utils.misc import get_related_queryset
        from base_libs.utils.misc import html_to_plain_text
        from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED
        
        from jetson.apps.external_services.utils import get_first
        from jetson.apps.external_services.utils import get_value
        
        Address = models.get_model("location", "Address")
        JobOffer = models.get_model("marketplace", "JobOffer")
        JobSector = models.get_model("marketplace", "JobSector")
        JobType = models.get_model("marketplace", "JobType")
        ObjectMapper = models.get_model("external_services", "ObjectMapper")
        Service = models.get_model("external_services", "Service")
        URLType = models.get_model("optionset", "URLType")
        
        s, created = Service.objects.get_or_create(
            sysname="musicjob",
            defaults={
                'url': "http://www.music-job.com/index.php?id=129&type=5003&tx_mnmboerse_pi2[stadt]=berlin",
                'title': "www.music-job.com",
                },
            )
        
        default_job_type, created = JobType.objects.get_or_create(
            slug="full-time",
            defaults = {
                'title_en': "Full-time",
                'title_de': "Vollzeit",
                },
            )
        
        default_urltype, created = URLType.objects.get_or_create(
            slug="musicjob",
            defaults = {
                'title_en': "music-job.com",
                'title_de': "music-job.com",
                },
            )
        
        default_job_sector, created = JobSector.objects.get_or_create(
            slug="music-scene",
            defaults = {
                'title_en': "Music & Scene",
                'title_de': "Musik & Bühne",
                },
            )
        
        response = urllib2.urlopen(s.url)
        data = response.read()
        
        xml_doc = parseString(data)
        
        for node_job in xml_doc.getElementsByTagName("item"):
        
            # get or create job offer
            external_id = get_value(node_job, "guid")
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
            job_offer.url0_type = default_urltype
            job_offer.is_commercial = False
            
            if change_date:
                job_offer.published_from = change_date
            else:
                job_offer.published_from = parse_datetime(
                    get_value(node_job, "pubDate"),
                    ignoretz=True,
                    )
            job_offer.published_till = job_offer.published_from + timedelta(days=7*6)
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
        

