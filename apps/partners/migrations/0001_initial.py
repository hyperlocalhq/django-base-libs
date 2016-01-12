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
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('website_url', models.URLField(max_length=255, verbose_name='Website URL', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Default Image', blank=True)),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('status', models.CharField(default=b'draft', max_length=20, verbose_name='Status', blank=True, choices=[(b'draft', 'Draft'), (b'published', 'Published')])),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Partner',
                'verbose_name_plural': 'Partners',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PartnerCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Do not change this value!', max_length=255, verbose_name='Sysname', blank=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('status', models.CharField(default=b'draft', max_length=20, verbose_name='Status', blank=True, choices=[(b'draft', 'Draft'), (b'published', 'Published'), (b'not-listed', 'Not listed at partners')])),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name': 'Partner category',
                'verbose_name_plural': 'Partner categories',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='partner',
            name='category',
            field=models.ForeignKey(to='partners.PartnerCategory'),
            preserve_default=True,
        ),
    ]
