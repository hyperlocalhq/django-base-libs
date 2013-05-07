# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from django.db import models
from django.conf import settings
from django.core.management import call_command
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(BaseCommand):
    help = "updates expired seasons"
    
    def handle(self, *args, **options):
        self.update_expired_seasons(*args, **options)
        
    def update_expired_seasons(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        
        from datetime import date
        
        from jetson.apps.mailing.recipient import Recipient
        from jetson.apps.mailing.views import send_email_using_template
        
        Museum = models.get_model("museums", "Museum")
        
        now = date.today()
        updated_museums_urls = []        
        for m in Museum.objects.all():
            for s in m.season_set.filter(end__lt=now):
                s.start = date(s.start.year + 1, s.start.month, s.start.day)
                s.end = date(s.end.year + 1, s.end.month, s.end.day)
                s.save()
                updated_museums_urls.append(m.get_url())
                
        # send an email
        sender_name, sender_email = settings.MANAGERS[0]
        send_email_using_template(
            recipients_list=[Recipient(email=settings.NOTIFY_ABOUT_SEASONS_TO_EMAIL)],
            email_template_slug="seasons_updated",
            obj_placeholders={
                'object_description': "<br />\n".join(updated_museums_urls),
            },
            sender_name = sender_name,
            sender_email = sender_email,
            delete_after_sending = False,
            )
        
