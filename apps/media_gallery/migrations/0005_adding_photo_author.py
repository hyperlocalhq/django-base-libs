# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_gallery', '0004_auto_20160606_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediagallery',
            name='photo_author',
            field=models.CharField(max_length=100, verbose_name='Photo', blank=True),
        ),
    ]
