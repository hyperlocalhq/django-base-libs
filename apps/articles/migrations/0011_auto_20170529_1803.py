# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_auto_20160606_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='creative_sectors',
            field=mptt.fields.TreeManyToManyField(related_name='creative_sector_articles', verbose_name='Creative sectors (deprecated)', to='structure.Term', blank=True),
        ),
    ]
