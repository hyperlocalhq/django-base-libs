# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cms.models.fields
import base_libs.models.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageTeaser',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='page_teaser_pageteaser', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('category', models.CharField(max_length=50, verbose_name='Category', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('alt', models.CharField(max_length=200, verbose_name='Alternative text', blank=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('short_description', base_libs.models.fields.ExtendedTextField(verbose_name='Short Description', blank=True)),
                ('link_external', models.URLField(max_length=255, verbose_name='External Link', blank=True)),
                ('link_text', models.CharField(default='read on', max_length=30, verbose_name='Link Text')),
                ('short_description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('internal_link', cms.models.fields.PageField(verbose_name='Internal link', blank=True, to='cms.Page', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
