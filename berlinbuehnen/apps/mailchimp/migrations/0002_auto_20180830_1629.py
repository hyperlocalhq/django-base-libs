# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingcontentblock',
            name='content_type',
            field=models.CharField(blank=True, max_length=40, verbose_name=b'Content Type', choices=[('authorship', 'Image authorship'), ('locations', 'Theaters'), ('productions', 'Productions'), ('festivals', 'Festivals'), ('educational_departments', 'Educational Departments'), ('educational_projects', 'Educational Projects'), ('article', 'News'), ('banner', 'Banner'), ('image_and_text', 'Image and Text'), ('headline', 'Headline'), ('text', 'Text only'), ('page_teaser', 'Page Teaser'), ('theater_of_the_week', 'Theater of the week')]),
        ),
    ]
