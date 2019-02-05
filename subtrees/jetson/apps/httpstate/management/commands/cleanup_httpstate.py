import datetime
from django.core.management.base import NoArgsCommand
from django.utils.timezone import now as tz_now


class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to clean out old data from the database (only expired sessions at the moment)."

    def handle_noargs(self, **options):
        from jetson.apps.httpstate.models import HttpState
        HttpState.objects.filter(expire_date__lt=tz_now()).delete()
