# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
import django.db.models.deletion
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published_from', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published immediately.", null=True, verbose_name='publishing date', blank=True)),
                ('published_till', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published forever.", null=True, verbose_name='published until', blank=True)),
                ('status', models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Draft'), (1, 'Published')])),
                ('path', filebrowser.fields.FileBrowseField(help_text='A path to a locally stored image or video.', max_length=255, verbose_name='File path', blank=True)),
                ('link', models.CharField(max_length=255, verbose_name='Link', blank=True)),
                ('alt', models.CharField(verbose_name='Alternative text', max_length=100, null=True, editable=False, blank=True)),
                ('title', models.TextField(default=b'', verbose_name='Title', null=True, editable=False, blank=True)),
                ('subtitle', models.TextField(default=b'', verbose_name='Subtitle', null=True, editable=False, blank=True)),
                ('credits', models.CharField(verbose_name='Photo credits', max_length=255, null=True, editable=False, blank=True)),
                ('highlight', models.BooleanField(default=False, verbose_name='Highlight')),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('subtitle_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Untertitel', blank=True)),
                ('subtitle_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('subtitle_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Untertitel', blank=True)),
                ('subtitle_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Titel', blank=True)),
                ('title_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Titel', blank=True)),
                ('title_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('credits_de', models.CharField(max_length=255, verbose_name='Photo credits', blank=True)),
                ('credits_en', models.CharField(max_length=255, verbose_name='Photo credits', blank=True)),
                ('alt_de', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
                ('alt_en', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
                ('author', models.ForeignKey(related_name='slide_author', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author')),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'slide',
                'verbose_name_plural': 'slides',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slideshow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
            ],
            options={
                'ordering': ['sysname'],
                'verbose_name': 'slideshow',
                'verbose_name_plural': 'slideshows',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='slide',
            name='slideshow',
            field=models.ForeignKey(default=0, verbose_name='Slideshow', to='slideshows.Slideshow'),
            preserve_default=True,
        ),
    ]
