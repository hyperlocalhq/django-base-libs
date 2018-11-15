# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0003_remove_category_sort_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contextcategory',
            name='body_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Text', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contextcategory',
            name='body_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Text', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='term',
            name='body_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Text', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='term',
            name='body_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Text', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='body_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Text', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='body_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Text', blank=True),
            preserve_default=True,
        ),
    ]
