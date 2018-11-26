# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20181015_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='sort_order',
            field=models.IntegerField(default=0, verbose_name='Sort Order'),
        ),
    ]
