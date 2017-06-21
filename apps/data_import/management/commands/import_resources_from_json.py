# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = """Imports resources from a JSON file"""

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))

        self.stdout.write("Importing resources\n")