# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from ccb.apps.events.models import Event
from jetson.apps.structure.models import Category

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        print 'migrating terms...'
