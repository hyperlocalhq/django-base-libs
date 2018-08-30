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
            name='MenuBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Do not change this value!', max_length=255, verbose_name='Sysname')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('language', models.CharField(max_length=5, verbose_name='Language', choices=[('de', 'Deutsch'), ('en', 'English'), ('fr', 'Fran\xe7ais'), ('pl', 'Polski'), ('tr', 'T\xfcrk\xe7e'), ('es', 'Espa\xf1ol'), ('it', 'Italiano')])),
                ('left_column', base_libs.models.fields.ExtendedTextField(verbose_name='Left Column Content', blank=True)),
                ('center_column', base_libs.models.fields.ExtendedTextField(verbose_name='Center Column Content', blank=True)),
                ('right_column_headline', models.CharField(max_length=255, verbose_name='Headline', blank=True)),
                ('right_column_description', base_libs.models.fields.ExtendedTextField(verbose_name='Description', blank=True)),
                ('right_column_image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('right_column_link', models.CharField(max_length=255, verbose_name='Link', blank=True)),
                ('left_column_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('right_column_description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('center_column_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
            ],
            options={
                'verbose_name': 'Menu Block',
                'verbose_name_plural': 'Menu Blocks',
            },
        ),
    ]
