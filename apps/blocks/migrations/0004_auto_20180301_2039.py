# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0003_auto_20160901_1619'),
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
