# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('logins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='welcomemessage',
            name='content_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt'),
        ),
        migrations.AlterField(
            model_name='welcomemessage',
            name='content_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt', blank=True),
        ),
    ]
