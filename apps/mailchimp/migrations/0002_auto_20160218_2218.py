# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingcontentblock',
            name='content_type',
            field=models.CharField(blank=True, max_length=20, verbose_name=b'Content Type', choices=[(b'image_and_text', b'Image and text'), (b'text', b'Text only'), (b'news', b'News'), (b'tenders_and_competitions', b'Tenders and Competitions'), (b'events', b'Events'), (b'portfolios', b'Portfolios'), (b'interviews', b'Magazine'), (b'jobs_and_bulletins', b'Jobs and Bulletins'), (b'people', b'Profiles')]),
            preserve_default=True,
        ),
    ]
