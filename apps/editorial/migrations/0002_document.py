# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import base_libs.models.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('structure', '0003_remove_category_sort_order'),
        ('editorial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', base_libs.models.fields.ExtendedTextField(verbose_name='Description', blank=True)),
                ('publisher_title', models.CharField(max_length=255, verbose_name='Publisher Title', blank=True)),
                ('publisher_url', base_libs.models.fields.URLField(verbose_name='Publisher URL', blank=True)),
                ('pdf_upload', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='PDF Upload', blank=True)),
                ('pdf_url', base_libs.models.fields.URLField(verbose_name='PDF URL', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('categories', mptt.fields.TreeManyToManyField(related_name='creative_industry_document_plugins', verbose_name='Categories', to='structure.Category', blank=True)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
