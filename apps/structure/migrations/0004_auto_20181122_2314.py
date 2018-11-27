# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0003_remove_category_sort_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contextcategory',
            name='body_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='body', blank=True),
        ),
        migrations.AlterField(
            model_name='contextcategory',
            name='body_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='body', blank=True),
        ),
        migrations.AlterField(
            model_name='contextcategory',
            name='creative_sectors',
            field=mptt.fields.TreeManyToManyField(to='structure.Term', verbose_name=b'Available creative sectors', blank=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='body_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='body', blank=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='body_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='body', blank=True),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='body_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='body', blank=True),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='body_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='body', blank=True),
        ),
    ]
