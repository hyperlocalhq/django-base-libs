import sys
from optparse import make_option

from django.db import models
from django.conf import settings
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--daily',
            action='store_true',
            dest='daily',
            default=False,
            help='Tells Django to send daily notification digest.'
        ),
        make_option(
            '--weekly',
            action='store_true',
            dest='weekly',
            default=False,
            help='Tells Django to send weekly notification digest.'
        ),
    )
    help = "Send daily or weekly notification digests."

    def handle_noargs(self, **options):

        verbosity = int(options.get('verbosity', 1))
        daily = options.get('daily')
        weekly = options.get('weekly')

        Digest = models.get_model("notification", "Digest")

        if daily and weekly or not (daily or weekly):
            print "Choose --daily OR --weekly"
            return

        if daily:
            for digest in Digest.objects.filter(
                frequency="daily", is_sent=False
            ):
                digest.send()
        elif weekly:
            for digest in Digest.objects.filter(
                frequency="weekly", is_sent=False
            ):
                digest.send()
