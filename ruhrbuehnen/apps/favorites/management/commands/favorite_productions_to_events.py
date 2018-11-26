# -*- coding: UTF-8 -*-
from django.utils.encoding import smart_str
from django.core.management.base import NoArgsCommand
from django.db import models

SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list
    help = "Switch favorite productions to favorite events."

    def handle_noargs(self, *args, **options):
        self.verbosity = int(options.get("verbosity", NORMAL))
        from django.contrib.contenttypes.models import ContentType

        Production = models.get_model("productions", "Production")
        Favorite = models.get_model("favorites", "Favorite")

        if self.verbosity >= NORMAL:
            print u"=== Switching favorite productions to favorite events ==="

        ct = ContentType.objects.get_for_model(Production)

        fav_count = Favorite.objects.filter(content_type=ct).count()
        for fav_index, favorite in enumerate(
            Favorite.objects.filter(content_type=ct), 1
        ):
            if self.verbosity >= NORMAL:
                prod = favorite.content_object
                if prod:
                    event = prod.get_nearest_occurrence()
                    if event:
                        favorite.content_object = event
                        favorite.save()
                        print "%d/%d %s changed" % (
                            fav_index, fav_count, smart_str(prod.title_de)
                        )
                    else:
                        favorite.delete()
                        print "%d/%d %s deleted" % (
                            fav_index, fav_count, smart_str(prod.title_de)
                        )
                else:
                    favorite.delete()
