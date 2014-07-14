# -*- coding: UTF-8 -*-

from django.core.management.base import NoArgsCommand

try:
    set
except NameError:
    from sets import Set as set   # Python 2.3 fallback

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Get the latest ideas from Jovoto"

    def handle_noargs(self, **options):
        from ccb.apps.external_services.jovoto.views import get_idea_list
        get_idea_list()
