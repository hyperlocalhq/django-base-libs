# -*- coding: UTF-8 -*-
import os
import shutil
from optparse import make_option

from django.conf import settings
from django.utils.encoding import smart_str
from django.core.management.base import NoArgsCommand
from django.apps import apps


class Command(NoArgsCommand):
    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--skip-images',
            action='store_true',
            dest='skip_images',
            default=False,
            help='Tells Django to NOT download images.'
        ),
    )
    help = "Deletes all productions and events with their relationships"

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", self.NORMAL))
        self.skip_images = options.get('skip_images')

        Person = apps.get_model("people", "Person")
        Production = apps.get_model("productions", "Production")
        Event = apps.get_model("productions", "Event")
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")
        ContentType = apps.get_model("contenttypes", "ContentType")
        PerObjectGroup = apps.get_model("permissions", "PerObjectGroup")

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Deleting Productions ===\n")

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
                # delete permission roles
                PerObjectGroup.objects.filter(
                    object_id=prod.pk,
                    content_type=ContentType.objects.get_for_model(Production),
                ).delete()
                # delete production itself
                prod.delete()

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Deleting People ===\n")
        Person.objects.all().delete()

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Deleting Object Mappers ===\n")
        ObjectMapper.objects.filter(
            content_type=ContentType.objects.get_for_model(Production),
        ).delete()
        ObjectMapper.objects.filter(
            content_type=ContentType.objects.get_for_model(Event),
        ).delete()

        if not self.skip_images:
            if self.verbosity >= self.NORMAL:
                self.stdout.write(u"=== Deleting Media Files ===\n")
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, "productions"))
