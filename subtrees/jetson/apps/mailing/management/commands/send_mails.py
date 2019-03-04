# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from optparse import make_option


class Command(NoArgsCommand):
    help = """Sends all unsent emails from the EmailMessage records"""

    def handle_noargs(self, **options):
        from jetson.apps.mailing.models import EmailMessage
        EmailMessage.objects.send_mails()
