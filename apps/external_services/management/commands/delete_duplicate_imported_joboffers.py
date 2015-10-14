# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    def handle(self, *args, **options):
        pass

    help = """Deletes duplicate job offers"""

    def handle_noargs(self, **options):

        from django.db import models

        Service = models.get_model("external_services", "Service")

        for s in Service.objects.filter(sysname__in=(
            "berlinstartupjobs", "creativeset", "kulturmanagement", "museumsbund", "musicjob", "theaterjobs")
        ):
            print(s.title)
            unique_external_ids = set(s.objectmapper_set.filter(
                content_type__app_label="marketplace",
                content_type__model="joboffer",
            ).values_list("external_id", flat=True))

            for external_id in unique_external_ids:
                for mapper in s.objectmapper_set.filter(
                    external_id=external_id,
                    content_type__app_label="marketplace",
                    content_type__model="joboffer",
                ).order_by("object_id")[1:]:
                    print "External_id: %s; Id: %s" % (external_id, mapper.object_id)
                    if mapper.content_object:
                        mapper.content_object.delete()
                    mapper.delete()
