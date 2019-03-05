# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='is public'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='valid_rating',
            field=models.BooleanField(default=False, verbose_name='is valid rating'),
        ),
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Grund'),
        ),
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Grund', blank=True),
        ),
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Grund', blank=True),
        ),
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Grund', blank=True),
        ),
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Grund', blank=True),
        ),
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Grund', blank=True),
        ),
        migrations.AlterField(
            model_name='moderatordeletionreason',
            name='reason_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Grund', blank=True),
        ),
    ]
