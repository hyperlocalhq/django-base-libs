# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0002_category'),
        ('site_specific', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contextitem',
            name='categories',
            field=mptt.fields.TreeManyToManyField(to='structure.Category', verbose_name='Categories', blank=True),
            preserve_default=True,
        ),
    ]
