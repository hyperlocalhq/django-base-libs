# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('site_specific', '0005_remove_contextitem_location_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contextitem',
            name='locality_type',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Locality type', blank=True, to='location.LocalityType', null=True),
            preserve_default=True,
        ),
    ]
