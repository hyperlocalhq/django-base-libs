# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_auto_20180301_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendedlogentry',
            name='change_message_de',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Nachricht \xe4ndern', blank=True),
        ),
        migrations.AlterField(
            model_name='extendedlogentry',
            name='change_message_en',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Nachricht \xe4ndern', blank=True),
        ),
    ]
