# -*- coding: UTF-8 -*-
from django.utils.encoding import smart_str
from django.core.management.base import NoArgsCommand
from django.apps import apps


class Command(NoArgsCommand):
    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3
    option_list = NoArgsCommand.option_list
    help = "Updates actual production start date and time."

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", self.NORMAL))

        Production = apps.get_model("productions", "Production")

        if self.verbosity >= self.NORMAL:
            self.stdout.write(
                u"=== Updating actual production start date and time ===\n"
            )

        prods_count = Production.objects.count()
        for prod_index, prod in enumerate(Production.objects.all(), 1):
            if self.verbosity >= self.NORMAL:
                self.stdout.write(
                    "%d/%d %s | %s\n" % (
                        prod_index,
                        prods_count,
                        smart_str(prod.title_de),
                        smart_str(prod.title_en),
                    )
                )
                prod.update_actual_date_and_time()
