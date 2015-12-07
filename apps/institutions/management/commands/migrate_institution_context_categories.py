# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from ccb.apps.institutions.models import Institution
from jetson.apps.structure.models import Category

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        print 'migrating context categories...'
