# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0003_remove_category_sort_order'),
        ('external_services', '0004_bulletinimportsource_default_bulletin_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleimportsource',
            name='default_categories',
            field=mptt.fields.TreeManyToManyField(help_text='Categories to apply to the imported articles by default.', to='structure.Category', null=True, verbose_name='Categories', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articleimportsource',
            name='default_creative_sectors',
            field=mptt.fields.TreeManyToManyField(related_name='cs_ais', db_column=b'default_cs', to='structure.Term', blank=True, help_text='Creative sectors to apply to the imported articles by default.', null=True, verbose_name='Creative sectors (deprecated)'),
            preserve_default=True,
        ),
    ]
