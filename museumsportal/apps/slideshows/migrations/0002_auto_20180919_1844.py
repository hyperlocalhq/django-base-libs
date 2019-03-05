# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('slideshows', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='highlight',
            field=models.BooleanField(default=False, verbose_name='Highlight'),
        ),
        migrations.AlterField(
            model_name='slide',
            name='subtitle_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Untertitel', blank=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='subtitle_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Untertitel', blank=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='subtitle_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Untertitel', blank=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='subtitle_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Untertitel', blank=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='subtitle_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Untertitel', blank=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='subtitle_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Untertitel', blank=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='subtitle_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Untertitel', blank=True),
        ),
    ]
