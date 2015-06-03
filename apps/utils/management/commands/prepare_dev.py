# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from django.db import models
from django.conf import settings
from django.core.management import call_command
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(NoArgsCommand):
    help = "Prepares site data for testing"
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        call_command('resetsuperuser', verbosity=verbosity)
        call_command('prepare_staging', verbosity=verbosity)
        
        Site = models.get_model("sites", "Site")
        SiteSettings = models.get_model("configuration", "SiteSettings")
        
        site = Site.objects.get_current()
        site.domain = settings.SESSION_COOKIE_DOMAIN #"127.0.0.1"
        site.save()
        
        # set google maps key for http://127.0.0.1:8000/
        if SiteSettings:
            site_settings = SiteSettings.objects.get_current()
            site_settings.gmaps_api_key = "ABQIAAAAJ4se-iHMqaoPrZ2Tn_GK5BTpH3CbXHjuCVmaTc5MkkU4wO1RRhS0j3YuhUPoa8hrxOW8qV0IebFnKg"
            site_settings.save()
        

