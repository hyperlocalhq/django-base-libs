# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
import csv

from ccb.apps.institutions.models import Institution
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
        institutions = Institution.objects.order_by('id')
        for institution in institutions:
            print 'migrating institution "{}"'.format(institution.id)
            for term in institution.get_creative_sectors():
                category_slug = ts2cs[term.slug]
                category = Category.objects.get(slug=category_slug)
                institution.categories.add(category)
                ContextItem.objects.update_for(institution)
                print '\tmigrating term "{}" to category "{}"'.format(term.slug, category_slug)
