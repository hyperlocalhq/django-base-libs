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
            name='Tile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('path', filebrowser.fields.FileBrowseField(help_text='A path to a locally stored image.', max_length=255, verbose_name='File path', blank=True)),
                ('link', models.CharField(max_length=255, verbose_name='Link', blank=True)),
                ('title', models.CharField(verbose_name='Title', max_length=200, null=True, editable=False, blank=True)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('description_en', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('title_en', models.CharField(max_length=200, verbose_name='Title', blank=True)),
                ('title_de', models.CharField(max_length=200, verbose_name='Title', blank=True)),
            ],
            options={
                'ordering': ['sysname'],
                'verbose_name': 'tile',
                'verbose_name_plural': 'tiles',
            },
            bases=(models.Model,),
        ),
    ]
