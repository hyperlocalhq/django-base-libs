# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='sender_email',
            field=models.EmailField(default='berlin-buehnen@kulturprojekte-berlin.de', max_length=254, verbose_name='Sender email'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sender_name',
            field=models.CharField(default='Ruhr B\xfchnen', max_length=255, verbose_name='Sender name'),
        ),
        migrations.AlterField(
            model_name='mailingcontentblock',
            name='content_type',
            field=models.CharField(blank=True, max_length=40, verbose_name=b'Content Type', choices=[('authorship', 'Image authorship'), ('locations', 'Theaters'), ('productions', 'Productions'), ('festivals', 'Festivals'), ('educational_departments', 'Educational Departments'), ('educational_projects', 'Educational Projects'), ('article', 'News'), ('banner', 'Banner'), ('image_and_text', 'Image and Text'), ('headline', 'Headline'), ('text', 'Text only'), ('page_teaser', 'Page Teaser'), ('theater_of_the_week', 'Theater of the week')]),
        ),
    ]
