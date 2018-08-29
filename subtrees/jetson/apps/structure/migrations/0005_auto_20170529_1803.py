# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0004_auto_20160901_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contextcategory',
            name='creative_sectors',
            field=mptt.fields.TreeManyToManyField(to='structure.Term', verbose_name='Available creative sectors', blank=True),
        ),
    ]
