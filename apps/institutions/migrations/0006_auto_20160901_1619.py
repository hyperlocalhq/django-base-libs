# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0005_institution_completeness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='exceptions_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonstige \xd6ffnungszeiten (Deutsch)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institution',
            name='exceptions_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonstige \xd6ffnungszeiten (Deutsch)', blank=True),
            preserve_default=True,
        ),
    ]
