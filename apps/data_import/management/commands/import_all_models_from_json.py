# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = """Batch import of all models from JSON files"""

    def handle(self, *args, **options):
        from django.core.management import call_command
        verbosity = int(options.get('verbosity', NORMAL))

        call_command('import_articles_from_json', verbosity=verbosity)
        call_command('import_bulletin_board_from_json', verbosity=verbosity)
        call_command('import_events_from_json', verbosity=verbosity)
        call_command('import_external_services_from_json', verbosity=verbosity)
        call_command('import_users_groups_people_from_json', verbosity=verbosity)
        call_command('import_institutions_and_groups_from_json', verbosity=verbosity)
        call_command('import_marketplace_from_json', verbosity=verbosity)
        call_command('import_media_gallery_from_json', verbosity=verbosity)
        call_command('import_resources_from_json', verbosity=verbosity)
        call_command('import_favorites_from_json', verbosity=verbosity)
        call_command('import_tracker_from_json', verbosity=verbosity)