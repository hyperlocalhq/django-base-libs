# -*- coding: UTF-8 -*-
from django.utils.encoding import smart_str
from django.core.management.base import NoArgsCommand
from django.apps import apps


class Command(NoArgsCommand):
    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3
    option_list = NoArgsCommand.option_list
    help = "Attaches root categories to all productions that have child categories attached."

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", self.NORMAL))
        self.skip_images = options.get('skip_images')

        Production = apps.get_model("productions", "Production")

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Attaching root categories to productions ===\n")

        categories_added = 0
        prods_count = Production.objects.count()
        for prod_index, prod in enumerate(Production.objects.all(), 1):
            if self.verbosity >= self.NORMAL:
                self.stdout.write("%d/%d %s | %s\n" % (prod_index, prods_count, smart_str(prod.title_de), smart_str(prod.title_en)))
                for cat in list(prod.categories.exclude(parent=None)):
                    prod.categories.add(cat.parent)
                    categories_added += 1

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"Categories added: %s\n" % categories_added)