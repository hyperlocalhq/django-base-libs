# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('media_gallery', '0007_mediagallery_show_cover_image_in_portfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='mediagallery',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='mediagallery',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
    ]
