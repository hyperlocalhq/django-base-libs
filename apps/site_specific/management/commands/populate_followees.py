# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    help = """Populates followees from favorites and individual relations"""

    def handle_noargs(self, **options):
        from actstream.actions import follow
        from django.contrib.contenttypes.models import ContentType
        from ccb.apps.site_specific.models import ContextItem
        from ccb.apps.people.models import Person
        from ccb.apps.institutions.models import Institution
        from ccb.apps.favorites.models import Favorite
        from jetson.apps.individual_relations.models import IndividualRelation
        verbosity = int(options.get('verbosity', NORMAL))

        institution_ct = ContentType.objects.get_for_model(Institution)
        person_ct = ContentType.objects.get_for_model(Person)
        contextitem_ct = ContentType.objects.get_for_model(ContextItem)

        for favorite in Favorite.objects.all():
            if favorite.content_type == contextitem_ct:
                contextitem = favorite.content_object
                if contextitem:
                    if contextitem.content_type == person_ct:
                        follow(favorite.user, contextitem.content_object.user, actor_only=False)
                        print(u"{} follows {}".format(favorite.user, contextitem.content_object.user))
                    elif contextitem.content_type == institution_ct:
                        follow(favorite.user, contextitem.content_object, actor_only=False)
                        print(u"{} follows {}".format(favorite.user, contextitem.content_object))

        for relation in IndividualRelation.objects.all():
            if relation.status == "confirmed":
                follow(relation.user, relation.to_user, actor_only=False)
                print(u"{} follows {}".format(relation.user, relation.to_user))
