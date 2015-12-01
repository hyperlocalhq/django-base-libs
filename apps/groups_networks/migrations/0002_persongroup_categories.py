# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0003_remove_category_sort_order'),
        ('groups_networks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persongroup',
            name='categories',
            field=mptt.fields.TreeManyToManyField(to='structure.Category', verbose_name='categories', blank=True),
            preserve_default=True,
        ),
    ]
