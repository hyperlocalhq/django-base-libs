# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_adding_photo_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='photo_author',
            field=models.CharField(max_length=100, verbose_name='Photo Credits', blank=True),
        ),
    ]
