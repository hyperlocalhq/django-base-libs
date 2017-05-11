# -*- coding: UTF-8 -*-
from django.utils.encoding import smart_str
from django.core.management.base import NoArgsCommand
from django.db import models

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Attaches root categories to all productions that have child categories attached."

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        Production = models.get_model("productions", "Production")

        if self.verbosity >= NORMAL:
            print u"=== Attaching root categories to productions ==="

        categories_added = 0
        prods_count = Production.objects.count()
        for prod_index, prod in enumerate(Production.objects.all(), 1):
            if self.verbosity >= NORMAL:
                print "%d/%d %s | %s" % (prod_index, prods_count, smart_str(prod.title_de), smart_str(prod.title_en))
                for cat in list(prod.categories.exclude(parent=None)):
                    prod.categories.add(cat.parent)
                    categories_added += 1

        if self.verbosity >= NORMAL:
            print u"Categories added: %s" % categories_added