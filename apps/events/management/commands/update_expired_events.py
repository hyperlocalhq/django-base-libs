# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from django.db import models
from django.conf import settings
from django.core.management import call_command
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = "updates expired events"

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        Event = models.get_model("events", "Event")
        Event.objects.update_expired()
