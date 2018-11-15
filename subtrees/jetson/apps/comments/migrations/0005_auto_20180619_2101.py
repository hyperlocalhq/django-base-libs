# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20180301_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Begr\xfcndung'),
        ),
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Begr\xfcndung', blank=True),
        ),
    ]
