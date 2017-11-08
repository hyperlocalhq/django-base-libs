# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_gallery', '0005_adding_photo_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='photo_author',
            field=models.CharField(max_length=100, verbose_name='Photo', blank=True),
        ),
    ]
