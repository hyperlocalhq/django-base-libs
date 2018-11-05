# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0002_auto_20160606_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatpage',
            name='content_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Content', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flatpage',
            name='content_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Content', blank=True),
            preserve_default=True,
        ),
    ]
