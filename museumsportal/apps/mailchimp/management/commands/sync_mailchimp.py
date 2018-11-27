# -*- coding: UTF-8 -*-
from optparse import make_option
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(NoArgsCommand):
    help = """Imports articles from the article-import sources"""
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        
        from django.db import models
        MList = models.get_model("mailchimp", "MList")
        
        from museumsportal.apps.mailchimp.utils import sync_mc_list

        for ml in MList.objects.all():
            sync_mc_list(ml)

