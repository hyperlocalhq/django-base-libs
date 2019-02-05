# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import filebrowser.fields
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0001_initial'),
        ('institutions', '0001_initial'),
        ('people', '0001_initial'),
        ('i18n', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('slug', models.CharField(max_length=255, verbose_name='Slug')),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('url_link', base_libs.models.fields.URLField(verbose_name='URL', blank=True)),
                ('document_file', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Document file', blank=True)),
                ('authors_plain', base_libs.models.fields.PlainTextModelField(help_text='Comma-separated list', max_length=255, verbose_name='External authors', blank=True)),
                ('published_yyyy', models.IntegerField(blank=True, null=True, verbose_name='Year of Publishing', choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)])),
                ('published_mm', models.SmallIntegerField(blank=True, null=True, verbose_name='Month of Publishing', choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('published_dd', models.SmallIntegerField(blank=True, null=True, verbose_name='Day of Publishing', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)])),
                ('playing_time', models.TimeField(null=True, verbose_name='Playing time', blank=True)),
                ('isbn10', models.CharField(max_length=13, verbose_name='ISBN-10', blank=True)),
                ('isbn13', models.CharField(max_length=17, verbose_name='ISBN-13', blank=True)),
                ('pages', models.PositiveIntegerField(default=0, null=True, verbose_name='Pages', blank=True)),
                ('file_size', models.PositiveIntegerField(default=0, null=True, verbose_name='File size (MB)', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('status', models.CharField(default=b'draft', max_length=20, verbose_name='Status', blank=True, choices=[(b'draft', 'Draft'), (b'published', 'Published'), (b'published_commercial', 'Published-Commercial'), (b'not_listed', 'Not Listed')])),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('authors', models.ManyToManyField(related_name='author_documents', verbose_name='Authors', to='people.Person', blank=True)),
                ('context_categories', mptt.fields.TreeManyToManyField(to='structure.ContextCategory', verbose_name='Context categories', blank=True)),
                ('creative_sectors', mptt.fields.TreeManyToManyField(related_name='creative_industry_documents', verbose_name='Creative sectors', to='structure.Term', blank=True)),
            ],
            options={
                'ordering': ['title', 'creation_date'],
                'abstract': False,
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='resources.DocumentType', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'document type',
                'verbose_name_plural': 'document types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Medium',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='Title', max_length=200, null=True, editable=False)),
                ('sort_order', models.IntegerField(default=0, verbose_name='Sort Order')),
                ('title_de', models.CharField(max_length=200, verbose_name='Title')),
                ('title_en', models.CharField(max_length=200, verbose_name='Title', blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Medium',
                'verbose_name_plural': 'Mediums',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=mptt.fields.TreeForeignKey(related_name='type_documents', verbose_name='Document type', to='resources.DocumentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='languages',
            field=models.ManyToManyField(to='i18n.Language', verbose_name='Languages', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='medium',
            field=models.ForeignKey(related_name='medium_documents', verbose_name='Medium', blank=True, to='resources.Medium', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='publisher',
            field=models.ForeignKey(verbose_name='Publisher', blank=True, to='institutions.Institution', null=True),
            preserve_default=True,
        ),
    ]
