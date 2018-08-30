# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', filebrowser.fields.FileBrowseField(help_text='A path to a locally stored image or video.', max_length=255, verbose_name='File path', blank=True)),
                ('link', models.CharField(max_length=255, verbose_name='Link', blank=True)),
                ('alt', models.CharField(verbose_name='Alternative text', max_length=100, null=True, editable=False, blank=True)),
                ('title', models.TextField(default=b'', verbose_name='Title', null=True, editable=False, blank=True)),
                ('subtitle', models.TextField(default=b'', verbose_name='Subtitle', null=True, editable=False, blank=True)),
                ('credits', models.CharField(verbose_name='Photo credits', max_length=255, null=True, editable=False, blank=True)),
                ('highlight', models.BooleanField(verbose_name='Highlight')),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('subtitle_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Subtitle', blank=True)),
                ('subtitle_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('subtitle_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Subtitle', blank=True)),
                ('subtitle_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('subtitle_fr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Subtitle', blank=True)),
                ('subtitle_fr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('subtitle_pl', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Subtitle', blank=True)),
                ('subtitle_pl_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('subtitle_tr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Subtitle', blank=True)),
                ('subtitle_tr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('subtitle_es', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Subtitle', blank=True)),
                ('subtitle_es_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('subtitle_it', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Subtitle', blank=True)),
                ('subtitle_it_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Titel', blank=True)),
                ('title_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Titel', blank=True)),
                ('title_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_fr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Titel', blank=True)),
                ('title_fr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_pl', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Titel', blank=True)),
                ('title_pl_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_tr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Titel', blank=True)),
                ('title_tr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_es', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Titel', blank=True)),
                ('title_es_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_it', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Titel', blank=True)),
                ('title_it_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('credits_de', models.CharField(max_length=255, verbose_name='Photo credits', blank=True)),
                ('credits_en', models.CharField(max_length=255, verbose_name='Photo credits', blank=True)),
                ('credits_fr', models.CharField(max_length=255, verbose_name='Photo credits', blank=True)),
                ('credits_pl', models.CharField(max_length=255, verbose_name='Photo credits', blank=True)),
                ('credits_tr', models.CharField(max_length=255, verbose_name='Photo credits', blank=True)),
                ('credits_es', models.CharField(max_length=255, verbose_name='Photo credits', blank=True)),
                ('credits_it', models.CharField(max_length=255, verbose_name='Photo credits', blank=True)),
                ('alt_de', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
                ('alt_en', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
                ('alt_fr', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
                ('alt_pl', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
                ('alt_tr', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
                ('alt_es', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
                ('alt_it', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'slide',
                'verbose_name_plural': 'slides',
            },
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
        ),
        migrations.AddField(
            model_name='slide',
            name='slideshow',
            field=models.ForeignKey(default=0, verbose_name='Slideshow', to='slideshows.Slideshow'),
        ),
    ]
