# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.contenttypes.models import ContentType

from ccb.apps.media_gallery.models import MediaGallery
from ccb.apps.institutions.models import Institution


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        print 'migrating institution categories...'
        institutions = Institution.objects.order_by('id')
        problems = set()
        for institution in institutions:
            print 'migrating categories for institution "{}" with id {}'.format(institution.title.encode('utf8'), institution.id)
            try:
                with transaction.atomic():
                    galleries = MediaGallery.objects.filter(
                        object_id=institution.id,
                        content_type=ContentType.objects.get_for_model(institution),
                    )
                    categories = institution.categories.filter(level=0)
                    for gallery in galleries:
                        print '\tmigrating institution categories to gallery "{}"'.format(gallery)
                        for category in categories:
                            print '\t\tadding category {} with level {} to gallery "{}"'.format(
                                category, category.level, gallery
                            )
                            gallery.categories.add(category)
                            # ContextItem.objects.update_for(gallery)
            except IntegrityError:
                print '** integrity error migrating categories for institution "{}" with id {} **'.format(
                    institution.title.encode('utf8'), institution.id,
                )
                problems.add((institution.id))
        if problems:
            print 'problems migrating the categories for the following institutions: {}'.format(problems)
