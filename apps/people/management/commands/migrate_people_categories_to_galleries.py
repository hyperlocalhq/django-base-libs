# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.contenttypes.models import ContentType
import csv

from ccb.apps.media_gallery.models import MediaGallery
from ccb.apps.people.models import Person
from ccb.apps.site_specific.models import ContextItem
from jetson.apps.structure.models import Category


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        print 'migrating person categories...'
        people = Person.objects.order_by('id')
        problems = set()
        for person in people:
            print 'migrating categories for person "{}" with id {}'.format(person.user.username, person.id)
            try:
                with transaction.atomic():
                    galleries = MediaGallery.objects.filter(
                        object_id=person.id,
                        content_type=ContentType.objects.get_for_model(person),
                    )
                    categories = person.categories.filter(level=0)
                    for gallery in galleries:
                        print '\tmigrating person categories to gallery: {}'.format(gallery)
                        for category in categories:
                            print '\t\tadding category {} with level {} to gallery {}'.format(
                                category, category.level, gallery
                            )
                            gallery.categories.add(category)
                            # ContextItem.objects.update_for(gallery)
            except IntegrityError:
                print '** integrity error migrating categories for person {} **'.format(
                    person.id,
                )
                problems.add((person.id))
        if problems:
            print 'problems migrating the categories for the following people: {}'.format(problems)
