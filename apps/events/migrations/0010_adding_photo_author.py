# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20170223_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='photo_author',
            field=models.CharField(max_length=100, verbose_name='Photo', blank=True),
        ),
    ]
