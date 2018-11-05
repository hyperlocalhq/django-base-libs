# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0006_auto_20151218_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='categories',
            field=mptt.fields.TreeManyToManyField(related_name='creative_industry_bulletins', verbose_name='Categories', to='structure.Category', blank=True),
            preserve_default=True,
        ),
    ]
