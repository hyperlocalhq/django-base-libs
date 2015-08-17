# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from optparse import make_option

class Command(NoArgsCommand):
    help = """Collects ad impressions and clicks"""
    def handle_noargs(self, **options):
        from datetime import datetime, timedelta
        from berlinbuehnen.apps.advertising.models import AdImpression, AdClick
        four_months_ago = datetime.now() - timedelta(days=31 * 4)

        qs = AdImpression.objects.filter(impression_date__lt=four_months_ago)
        print "Ad impressions deleted: %s" % qs.count()
        qs.delete()

        qs = AdClick.objects.filter(click_date__lt=four_months_ago)
        print "Ad clicks deleted: %s" % qs.count()
        qs.delete()
