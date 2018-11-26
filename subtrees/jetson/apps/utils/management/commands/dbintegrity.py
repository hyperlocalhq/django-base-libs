# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--fix',
            action='store_true',
            help='Fixes database integrity errors.',
        ),
        make_option(
            '--debug',
            action='store_true',
            help='Fixes database integrity errors.',
        ),
    )
    help = """Checks and Fixes the integrity of the database entries"""

    def handle_noargs(self, **options):
        should_fix = options.get('fix', False)
        verbosity = int(options.get('verbosity', NORMAL))
        debug = options.get('debug', False)

        from django.contrib.contenttypes.models import ContentType
        from django.conf import settings
        from django.db import models
        from django.db.models.query import CollectedObjects
        from django.core.serializers import serialize
        from django.db import models
        from django.forms.models import modelform_factory

        #####################################################
        if verbosity > SILENT:
            print "Checking for unused ContentType objects..."
        for ct in ContentType.objects.all():
            try:
                ct.model_class()._default_manager.count()
                if verbosity == VERBOSE:
                    print "%s is ok" % ct
            except:
                if verbosity > SILENT:
                    print "%s is BROKEN" % ct

                if debug:
                    import pdb
                    pdb.set_trace()

                if should_fix:
                    ct.delete()
                    if verbosity > SILENT:
                        print "(deleted)"

        #####################################################

        if verbosity > SILENT:
            print "Checking related objects..."

        for model in models.get_models():
            for obj in model._default_manager.select_related():
                try:
                    tmp = hasattr(obj, "object_id") and hasattr(
                        obj, "content_type"
                    ) and obj.content_object
                except:
                    print model, obj.pk
                try:
                    seen_objs = CollectedObjects()
                    obj._collect_sub_objects(seen_objs)
                except:
                    print model, obj.pk

        #####################################################

        if verbosity > SILENT:
            print "Checking json serialization..."

        for model in models.get_models():
            try:
                serialize("json", model._default_manager.all())
            except:
                print model
        #####################################################

        if verbosity > SILENT:
            print "Checking the validity of all values..."

        for model in models.get_models():
            form_class = modelform_factory(model)
            for obj in model._default_manager.all():
                form = form_class(instance=obj)  # get initial prepopulated
                form = form_class(data=form.initial, instance=obj)
                if not form.is_valid():
                    print model, obj.pk, dict(form.errors)
