# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import base_libs.models.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('day', models.DateField(verbose_name='Date')),
                ('title', models.CharField(verbose_name='Title', max_length=200, null=True, editable=False)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False)),
                ('preview_image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Preview Image', blank=True)),
                ('active_image_de', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Active Image', blank=True)),
                ('active_image_en', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Active Image', blank=True)),
                ('title_de', models.CharField(max_length=200, verbose_name='Title')),
                ('title_en', models.CharField(max_length=200, verbose_name='Title', blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung')),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('creator', models.ForeignKey(related_name='day_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('modifier', models.ForeignKey(related_name='day_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
            ],
            options={
                'ordering': ('-day',),
                'verbose_name': 'Day',
                'verbose_name_plural': 'Days',
            },
            bases=(models.Model,),
        ),
    ]
