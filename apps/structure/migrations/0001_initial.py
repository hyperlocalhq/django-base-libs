# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import filebrowser.fields
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContextCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('body', models.TextField(default=b'', verbose_name='body', null=True, editable=False, blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('is_applied4person', models.BooleanField(default=True, verbose_name='for people')),
                ('is_applied4institution', models.BooleanField(default=True, verbose_name='for institutions')),
                ('is_applied4document', models.BooleanField(default=True, verbose_name='for documents')),
                ('is_applied4event', models.BooleanField(default=True, verbose_name='for events')),
                ('is_applied4persongroup', models.BooleanField(default=True, verbose_name='for groups of people')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('body_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt', blank=True)),
                ('body_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('body_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt', blank=True)),
                ('body_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'context category',
                'verbose_name_plural': 'context categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('body', models.TextField(default=b'', verbose_name='body', null=True, editable=False, blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('body_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt', blank=True)),
                ('body_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('body_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt', blank=True)),
                ('body_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='structure.Term', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'term',
                'verbose_name_plural': 'terms',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('body', models.TextField(default=b'', verbose_name='body', null=True, editable=False, blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('hierarchy', models.BooleanField(default=False, verbose_name='Will the terms of this vocabulary be used in hierarchical structure?')),
                ('body_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt', blank=True)),
                ('body_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('body_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt', blank=True)),
                ('body_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'vocabulary',
                'verbose_name_plural': 'vocabularies',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='term',
            name='vocabulary',
            field=models.ForeignKey(verbose_name='Vocabulary', to='structure.Vocabulary'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contextcategory',
            name='creative_sectors',
            field=mptt.fields.TreeManyToManyField(to='structure.Term', null=True, verbose_name='Available creative sectors', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contextcategory',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='structure.ContextCategory', null=True),
            preserve_default=True,
        ),
    ]
