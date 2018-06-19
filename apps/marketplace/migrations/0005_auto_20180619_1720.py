# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_auto_20160926_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joboffer',
            name='url0_link',
            field=base_libs.models.fields.URLField(max_length=500, verbose_name='URL', blank=True),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='url1_link',
            field=base_libs.models.fields.URLField(max_length=500, verbose_name='URL', blank=True),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='url2_link',
            field=base_libs.models.fields.URLField(max_length=500, verbose_name='URL', blank=True),
        ),
    ]
