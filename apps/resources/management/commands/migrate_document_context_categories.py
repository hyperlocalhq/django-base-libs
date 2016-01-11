# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
import csv

from ccb.apps.resources.models import Document
from ccb.apps.site_specific.models import ContextItem
from jetson.apps.structure.models import Category

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        ccs2cs = None
        with open('mapping/full_contextcategories2categories.csv') as f:
            r = csv.DictReader(f, delimiter=';')
            ls = [(
                row['context category slug'],
                row['category slug'],
            ) for row in r]
            ccs2cs = dict(ls)
        print 'migrating context categories...'
        documents = Document.objects.order_by('id')
        missing_slugs = set()
        for document in documents:
            print 'migrating document "{}"'.format(document.id)
            for context_category in document.get_context_categories():
                try:
                    category_slug = ccs2cs[context_category.slug]
                    print '\tmigrating context category "{}" to category "{}"'.format(
                        context_category.slug,
                        category_slug
                    )
                    category = Category.objects.get(slug=category_slug)
                    document.categories.add(category)
                    ContextItem.objects.update_for(document)
                except KeyError:
                    print '\t** context category "{}" not found in mapping **'.format(context_category.slug)
                    missing_slugs.add(context_category.slug)
        print "couldn't migrate these context categories: {}".format(missing_slugs)
