# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groups_networks', '0002_persongroup_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persongroup',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='persongroup',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
    ]
