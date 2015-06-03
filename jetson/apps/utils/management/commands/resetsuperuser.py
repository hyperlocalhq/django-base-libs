# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(NoArgsCommand):
    help = "Changes the superuser to demo/demo"
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        
        from django.contrib.auth.models import User
        
        superusers = User.objects.filter(
            is_superuser=True,
            ).order_by('date_joined')
        if superusers:
            u = superusers[0]
            u.username = "demo"
            u.is_active = True
            u.set_password("demo")
            u.save()
            if verbosity > SILENT:
                print "Superuser changed to demo/demo."
        else:
            User.objects.create_superuser("demo", "", "demo")
            if verbosity > SILENT:
                print "Superuser demo/demo created."

