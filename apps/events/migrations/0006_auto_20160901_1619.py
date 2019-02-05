# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20160606_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='exceptions_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonstige \xd6ffnungszeiten (Deutsch)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='exceptions_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonstige \xd6ffnungszeiten (Deutsch)', blank=True),
            preserve_default=True,
        ),
    ]
