# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('curated_lists', '0004_auto_20160701_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curatedlist',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='curatedlist',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
            preserve_default=True,
        ),
    ]
