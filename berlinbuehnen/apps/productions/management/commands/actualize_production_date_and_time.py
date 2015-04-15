# -*- coding: UTF-8 -*-

import os
import shutil
from optparse import make_option

from django.conf import settings
from django.utils.encoding import smart_str
from django.core.management.base import NoArgsCommand
from django.db import models

from import_base import ImportFromHeimatBase

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand, ImportFromHeimatBase):
    option_list = NoArgsCommand.option_list
    help = "Updates actual production start date and time."

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))

        Production = models.get_model("productions", "Production")

        if self.verbosity >= NORMAL:
            print u"=== Updating actual production start date and time ==="

        prods_count = Production.objects.count()
        for prod_index, prod in enumerate(Production.objects.all(), 1):
            if self.verbosity >= NORMAL:
                print "%d/%d %s | %s" % (prod_index, prods_count, smart_str(prod.title_de), smart_str(prod.title_en))
                prod.update_actual_date_and_time()
