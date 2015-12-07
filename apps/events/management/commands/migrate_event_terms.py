# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from django.db.utils import IntegrityError
import csv

from ccb.apps.events.models import Event
from ccb.apps.site_specific.models import ContextItem
from jetson.apps.structure.models import Category

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        ts2cs = None
        with open('mapping/full_terms2categories.csv') as f:
            r = csv.DictReader(f, delimiter=';')
            ls = [(
                row['term slug'],
                row['category slug'],
            ) for row in r]
            ts2cs = dict(ls)
        print 'migrating terms...'
        events = Event.objects.order_by('id')
        problems = set()
        for event in events:
            print 'migrating event "{}"'.format(event.id)
            for term in event.get_creative_sectors():
                category_slug = ts2cs[term.slug]
                print '\tmigrating term "{}" to category "{}"'.format(term.slug, category_slug)
                try:
                    category = Category.objects.get(slug=category_slug)
                    event.categories.add(category)
                    ContextItem.objects.update_for(event)
                except IntegrityError:
                    print '\t** integrity error migrating person {} from term {} to category "{}" **'.format(
                        event.id,
                        term.slug,
                        category_slug,
                    )
                    problems.add((event.id, term.slug))
        print 'problems migrating the following events and terms: {}'.format(problems)
