# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('copyright_limitations', models.CharField(help_text='If this field does not contain precise restrictions or if no restrictions are set, the rights of use are granted non-exclusively, and unrestricted in terms of time, place and content.', max_length=300, verbose_name='Copyright limitations', blank=True)),
                ('description_de', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_en', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_fr', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_pl', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_tr', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_es', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_it', base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('title_de', models.CharField(max_length=300, verbose_name='Title', blank=True)),
                ('title_en', models.CharField(max_length=300, verbose_name='Title', blank=True)),
                ('title_fr', models.CharField(max_length=300, verbose_name='Title', blank=True)),
                ('title_pl', models.CharField(max_length=300, verbose_name='Title', blank=True)),
                ('title_tr', models.CharField(max_length=300, verbose_name='Title', blank=True)),
                ('title_es', models.CharField(max_length=300, verbose_name='Title', blank=True)),
                ('title_it', models.CharField(max_length=300, verbose_name='Title', blank=True)),
            ],
            options={
                'ordering': ['file_path'],
                'verbose_name': 'File description',
                'verbose_name_plural': 'File descriptions',
            },
        ),
    ]
