# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0003_remove_category_sort_order'),
        ('articles', '0003_auto_20150923_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='categories',
            field=mptt.fields.TreeManyToManyField(to='structure.Category', verbose_name='Categories', blank=True),
            preserve_default=True,
        ),
    ]
