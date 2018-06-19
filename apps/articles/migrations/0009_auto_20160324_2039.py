# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_article_alternative_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='alternative_title',
            field=models.CharField(default=b'', max_length=200, verbose_name='Alternative Title, used by the CCB Magazine', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='creative_sectors',
            field=mptt.fields.TreeManyToManyField(related_name='creative_sector_articles', null=True, verbose_name='Creative sectors (deprecated)', to='structure.Term', blank=True),
            preserve_default=True,
        ),
    ]
