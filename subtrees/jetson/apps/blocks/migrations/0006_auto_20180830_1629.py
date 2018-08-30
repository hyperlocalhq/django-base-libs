# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0005_auto_20180619_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoblock',
            name='content_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', help_text='It can contain template tags and variables', null=True, verbose_name='Inhalt'),
        ),
        migrations.AlterField(
            model_name='infoblock',
            name='content_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', help_text='It can contain template tags and variables', null=True, verbose_name='Inhalt', blank=True),
        ),
    ]
