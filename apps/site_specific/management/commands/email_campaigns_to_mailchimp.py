# -*- coding: UTF-8 -*-
from optparse import make_option
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2

class Command(NoArgsCommand):
    help = """Imports articles from the article-import sources"""
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        
        from django.db import models
        
        MailingList = models.get_model("email_campaigns", "MailingList")
        InfoSubscription = models.get_model("email_campaigns", "InfoSubscription")
        MList = models.get_model("mailchimp", "MList")
        Subscription = models.get_model("mailchimp", "Subscription")

        for ml in MailingList.objects.all():
            new_ml = MList.objects.create(
                title_de=ml.title_de,
                title_en=ml.title_en,
                is_public=ml.is_public,
                site=ml.site,
                )
            for sub in ml.infosubscription_set.all():
                first_name = sub.subscriber_name
                last_name = ""
                if " " in sub.subscriber_name:
                    first_name, last_name = sub.subscriber_name.split(" ", 1)
                new_sub = Subscription(
                    subscriber=sub.subscriber,
                    first_name=first_name,
                    last_name=last_name,
                    email=sub.email,
                    ip=sub.ip,
                    mailinglist=new_ml,
                    creation_date=sub.creation_date,
                    modified_date=sub.modified_date,
                    status="subscribed",
                    )
                new_sub.save()
