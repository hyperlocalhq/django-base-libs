# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    help = """Updates the statuses of expired bulletins"""

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        from django.db import models
        Bulletin = models.get_model("bulletin_board", "Bulletin")
        Bulletin.expired_objects.update_status()
