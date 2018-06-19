# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(NoArgsCommand):
    help = "Prepares site data for testing"
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        
        SiteSettings = models.get_model("configuration", "SiteSettings")
        
        site = Site.objects.get_current()
        if SiteSettings:
            ss, created = SiteSettings.objects.get_or_create(site=site)
            ss.extra_head = ""
            ss.extra_body = ""
            ss.save()
        
        domain = getattr(settings, 'STAGING_DOMAIN', "")
        if domain:
            site.domain = domain
            site.save()
