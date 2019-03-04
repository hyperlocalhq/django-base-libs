# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_adding_photo_credits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='photo_author',
            field=models.CharField(max_length=100, verbose_name='Photo Credits', blank=True),
        ),
    ]
