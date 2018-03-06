# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('title', models.CharField(verbose_name='Title', max_length=200, null=True, editable=False)),
                ('subtitle', models.CharField(verbose_name='Subtitle', max_length=200, null=True, editable=False, blank=True)),
                ('short_description', models.TextField(default=b'', verbose_name='Short Description', null=True, editable=False, blank=True)),
                ('header_bg_color', models.CharField(help_text='Use RGB or HTML format, like "rgb(0, 0, 255)" or "#0000ff".', max_length=20, verbose_name='Header Background Color')),
                ('header_icon', filebrowser.fields.FileBrowseField(help_text='A path to a locally stored image.', max_length=255, verbose_name='Header Icon', blank=True)),
                ('subtitle_de', models.CharField(max_length=200, verbose_name='Subtitle', blank=True)),
                ('subtitle_en', models.CharField(max_length=200, verbose_name='Subtitle', blank=True)),
                ('title_de', models.CharField(max_length=200, verbose_name='Title')),
                ('title_en', models.CharField(max_length=200, verbose_name='Title', blank=True)),
                ('short_description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Short Description', blank=True)),
                ('short_description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('short_description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Short Description', blank=True)),
                ('short_description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
            ],
            options={
                'ordering': ['title_de'],
                'verbose_name': 'Service Page Banner',
                'verbose_name_plural': 'Service Page Banners',
            },
            bases=(models.Model,),
        ),
    ]
