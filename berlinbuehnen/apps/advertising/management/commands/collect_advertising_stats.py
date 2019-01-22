# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from optparse import make_option

class Command(NoArgsCommand):
    help = """Collects ad impressions and clicks"""
    def handle_noargs(self, **options):
        from berlinbuehnen.apps.advertising.models import AdBase
        for ad in AdBase.objects.all():
            ad.collect_impressions()
            ad.collect_clicks()
            ad.save()
