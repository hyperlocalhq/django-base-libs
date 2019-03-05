# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('museumssummer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='description_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='description_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='description_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='description_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='description_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_es',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_fr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_it',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_pl',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='exceptions_tr',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Sonder\xf6ffnungszeiten', blank=True),
        ),
    ]
