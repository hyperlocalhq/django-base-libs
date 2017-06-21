# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from django.db import transaction
from django.db.utils import IntegrityError
import csv

from kb.apps.articles.models import Article
from kb.apps.site_specific.models import ContextItem
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
        articles = Article.objects.order_by('id')
        problems = set()
        for article in articles:
            print 'migrating article "{}"'.format(article.id)
            try:
                with transaction.atomic():
                    for term in article.get_creative_sectors():
                        category_slug = ts2cs[term.slug]
                        print '\tmigrating term "{}" to category "{}"'.format(term.slug, category_slug)
                        category = Category.objects.get(slug=category_slug)
                        article.categories.add(category)
                        ContextItem.objects.update_for(article)
            except IntegrityError:
                print '** integrity error migrating article {} **'.format(
                    article.id,
                )
                problems.add((article.id))
        if problems:
            print 'problems migrating the following articles: {}'.format(problems)
