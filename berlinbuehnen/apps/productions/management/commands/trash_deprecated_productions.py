# -*- coding: UTF-8 -*-
from optparse import make_option

from django.utils.encoding import smart_str
from django.core.management.base import NoArgsCommand
from django.apps import apps

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--skip-images', action='store_true', dest='skip_images', default=False,
            help='Tells Django to NOT download images.'),
    )
    help = "Deletes all productions and events with their relationships"

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))
        self.skip_images = options.get('skip_images')

        Service = apps.get_model("external_services", "Service")

        self.culturebase_service = Service.objects.get(sysname="culturebase_prods")

        self.trash_deprecated_for_service(Service.objects.get(sysname="culturebase_dob_prods"))
        self.trash_deprecated_for_service(Service.objects.get(sysname="culturebase_radialsystem_prods"))
        self.trash_deprecated_for_service(Service.objects.get(sysname="culturebase_sob_prods"))

    def trash_deprecated_for_service(self, service):

        if self.verbosity >= NORMAL:
            print u"=== Eliminating Old %s ===" % service.title

        mapper_count = service.objectmapper_set.filter(content_type__model="production").count()
        for mapper_index, new_mapper in enumerate(service.objectmapper_set.filter(content_type__model="production"), 1):
            print "%d/%d %s" % (mapper_index, mapper_count, smart_str(new_mapper.content_object))
            new_production = new_mapper.content_object
            old_mappers = self.culturebase_service.objectmapper_set.filter(
                content_type__model="production",
                external_id=new_mapper.external_id,
            )
            if not old_mappers or not old_mappers[0].content_object:
                continue
            old_production = old_mappers[0].content_object
            for owner in old_production.get_owners():
                new_production.set_owner(owner)
            old_production.status = "trashed"
            old_production.save()
