# -*- coding: UTF-8 -*-

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Get the latest ideas from Jovoto"

    def handle_noargs(self, **options):
        from ccb.apps.external_services.jovoto.views import get_idea_list

        get_idea_list()
