# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
import csv

from ccb.apps.events.models import Event
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
        events = Event.objects.all()
        for event in events:
            print 'migrating event "{}"'.format(event.id)
            for term in event.get_creative_sectors():
                category_id = ts2cs[term.slug]
                print '\tmigrating term "{}" to category "{}"'.format(term.slug, category_id)
