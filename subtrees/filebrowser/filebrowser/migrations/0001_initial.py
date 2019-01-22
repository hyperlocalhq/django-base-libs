# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_path', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='File path')),
                ('title', models.CharField(verbose_name='Title', max_length=300, null=True, editable=False, blank=True)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('author', models.CharField(max_length=300, verbose_name='Copyright / Photographer', blank=True)),
                ('copyright_limitations', models.CharField(max_length=300, verbose_name='Copyright limitations', blank=True)),
                ('description_en', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('title_en', models.CharField(max_length=300, verbose_name='Title', blank=True)),
                ('title_de', models.CharField(max_length=300, verbose_name='Title', blank=True)),
            ],
            options={
                'ordering': ['file_path'],
                'verbose_name': 'File description',
                'verbose_name_plural': 'File descriptions',
            },
            bases=(models.Model,),
        ),
    ]
