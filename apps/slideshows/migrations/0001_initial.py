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
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', filebrowser.fields.FileBrowseField(help_text='A path to a locally stored image or video.', max_length=255, verbose_name='File path', blank=True)),
                ('link', models.CharField(max_length=255, verbose_name='Link', blank=True)),
                ('alt', models.CharField(verbose_name='Alternative text', max_length=100, null=True, editable=False, blank=True)),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('alt_de', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
                ('alt_en', models.CharField(max_length=100, verbose_name='Alternative text', blank=True)),
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
            field=models.ForeignKey(verbose_name='Slideshow', to='slideshows.Slideshow'),
            preserve_default=True,
        ),
    ]
