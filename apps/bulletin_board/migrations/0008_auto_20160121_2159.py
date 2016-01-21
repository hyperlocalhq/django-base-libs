# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0007_auto_20160110_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='locality_type',
            field=mptt.fields.TreeForeignKey(related_name='locality_bulletin', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Locality type', blank=True, to='location.LocalityType', null=True),
            preserve_default=True,
        ),
    ]
