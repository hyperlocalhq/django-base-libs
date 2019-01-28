# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import filebrowser.fields
import django.db.models.deletion
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheaterOfTheWeek',
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
                ('article_type', mptt.fields.TreeForeignKey(verbose_name='Type', blank=True, to='articles.ArticleType', null=True)),
                ('author', models.ForeignKey(related_name='theateroftheweek_author', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author')),
                ('theater', models.ForeignKey(to='locations.Location')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Theater of the week',
                'verbose_name_plural': 'Theaters of the week',
            },
        ),
    ]
