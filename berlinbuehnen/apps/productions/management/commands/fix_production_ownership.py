# -*- coding: UTF-8 -*-
from optparse import make_option

from django.utils.encoding import smart_str
from django.core.management.base import NoArgsCommand
from django.db import models

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells Django to NOT download images.'),
    )
    help = "Fixes productions ownership"

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        Production = models.get_model("productions", "Production")

        if self.verbosity >= NORMAL:
            print u"=== Fixing Production Ownerships ==="

        prods_count = Production.objects.count()
        for prod_index, prod in enumerate(Production.objects.all(), 1):
            if self.verbosity >= NORMAL:
                print "%d/%d %s | %s" % (prod_index, prods_count, smart_str(prod.title_de), smart_str(prod.title_en))
                for location in prod.in_program_of.all():
                    for owner in location.get_owners():
                        prod.set_owner(owner)
                # for location in prod.play_locations.all():
                #     for owner in location.get_owners():
                #         prod.set_owner(owner)
                # for event in prod.event_set.all():
                #     for location in event.play_locations.all():
                #         for owner in location.get_owners():
                #             prod.set_owner(owner)

