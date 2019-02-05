# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0008_auto_20180321_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
    ]
