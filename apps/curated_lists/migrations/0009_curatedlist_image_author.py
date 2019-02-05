# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curated_lists', '0008_auto_20181018_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='curatedlist',
            name='image_author',
            field=models.CharField(max_length=100, verbose_name='Image Credits', blank=True),
        ),
    ]
