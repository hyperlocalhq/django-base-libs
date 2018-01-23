# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from django.db import models
from django.conf import settings
from django.core.management import call_command
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(BaseCommand):
    help = "imports museums"
    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        Workshop = models.get_model("workshops", "Workshop")
        Workshop.objects.update_expired()
