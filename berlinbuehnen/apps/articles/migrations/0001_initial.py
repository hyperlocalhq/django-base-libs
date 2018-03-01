# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import filebrowser.fields
import django.db.models.deletion
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('published_from', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published immediately.", null=True, verbose_name='publishing date', blank=True)),
                ('published_till', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published forever.", null=True, verbose_name='published until', blank=True)),
                ('status', models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Draft'), (1, 'Published')])),
                ('views', models.IntegerField(default=0, verbose_name='views', editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='title')),
                ('subtitle', models.CharField(default=b'', max_length=255, verbose_name='subtitle', blank=True)),
                ('description', base_libs.models.fields.ExtendedTextField(default=b'', verbose_name='summary', blank=True)),
                ('content', base_libs.models.fields.ExtendedTextField(default=b'', verbose_name='entry')),
                ('image_title', models.CharField(default=b'', max_length=50, verbose_name='image title', blank=True)),
                ('image_description', base_libs.models.fields.ExtendedTextField(default=b'', verbose_name='image description', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='overview image', blank=True)),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('language', models.CharField(default=b'', max_length=5, verbose_name='Language', blank=True, choices=[('de', 'Deutsch'), ('en', 'English')])),
                ('image_description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('content_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('short_title', models.CharField(default=b'', max_length=255, verbose_name='short title', blank=True)),
                ('newsletter', models.BooleanField(default=False, verbose_name='Show in newsletter')),
            ],
            options={
                'ordering': ('-published_from', '-creation_date'),
                'abstract': False,
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=512, null=True, editable=False)),
                ('title_de', models.CharField(max_length=512, verbose_name='title')),
                ('title_en', models.CharField(max_length=512, verbose_name='title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='articles.ArticleCategory', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'Article Category',
                'verbose_name_plural': 'Article Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleSelection',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=512, null=True, editable=False)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title_de', models.CharField(max_length=512, verbose_name='title')),
                ('title_en', models.CharField(max_length=512, verbose_name='title', blank=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='articles.ArticleType', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'abstract': False,
                'verbose_name': 'Article Type',
                'verbose_name_plural': 'Article Types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='article_type',
            field=mptt.fields.TreeForeignKey(verbose_name='Type', blank=True, to='articles.ArticleType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(related_name='article_author', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=mptt.fields.TreeForeignKey(verbose_name='Category', blank=True, to='articles.ArticleCategory', null=True),
            preserve_default=True,
        ),
    ]
