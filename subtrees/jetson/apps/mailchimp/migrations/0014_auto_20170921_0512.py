# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0013_auto_20170808_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlist',
            name='language',
            field=models.CharField(blank=True, max_length=5, verbose_name='Language of the newsletter', choices=[('en', 'English'), ('de', 'German')]),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sender_email',
            field=models.EmailField(default='ccb-contact@kulturprojekte-berlin.de', max_length=254, verbose_name='Sender email'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sender_name',
            field=models.CharField(default='Creative City Berlin', max_length=255, verbose_name='Sender name'),
        ),
        migrations.AlterField(
            model_name='mailingcontentblock',
            name='content_type',
            field=models.CharField(blank=True, max_length=20, verbose_name=b'Content Type', choices=[('image_and_text', 'Image and text'), ('text', 'Text only'), ('news', 'News'), ('tenders_and_compet', 'Tenders and Competitions'), ('events', 'Events'), ('portfolios', 'Portfolios'), ('interviews', 'Magazine'), ('jobs_and_bulletins', 'Jobs and Bulletins'), ('people', 'Profiles')]),
        ),
    ]
