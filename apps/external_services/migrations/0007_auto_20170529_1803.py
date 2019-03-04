# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('external_services', '0006_auto_20161011_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleimportsource',
            name='default_categories',
            field=mptt.fields.TreeManyToManyField(help_text='Categories to apply to the imported articles by default.', to='structure.Category', verbose_name='Categories', blank=True),
        ),
        migrations.AlterField(
            model_name='articleimportsource',
            name='default_creative_sectors',
            field=mptt.fields.TreeManyToManyField(related_name='cs_ais', db_column=b'default_cs', to='structure.Term', blank=True, help_text='Creative sectors to apply to the imported articles by default.', verbose_name='Creative sectors (deprecated)'),
        ),
        migrations.AlterField(
            model_name='articleimportsource',
            name='default_sites',
            field=models.ManyToManyField(help_text='Sites to apply to the imported articles by default.', related_name='site_article_import_sources', verbose_name='Sites', to='sites.Site', blank=True),
        ),
        migrations.AlterField(
            model_name='bulletinimportsource',
            name='default_categories',
            field=mptt.fields.TreeManyToManyField(help_text='Categories to apply to the imported bulletins by default.', to='structure.Category', verbose_name='Categories', blank=True),
        ),
    ]
