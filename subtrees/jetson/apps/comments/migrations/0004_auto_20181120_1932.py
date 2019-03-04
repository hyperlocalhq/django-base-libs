# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20170529_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='reason'),
        ),
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='reason', blank=True),
        ),
    ]
