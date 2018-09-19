# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filebrowser', '0003_populate_file_path_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedescription',
            name='description_de',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='description_en',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='description_es',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='description_fr',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='description_it',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='description_pl',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='description_tr',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
    ]
