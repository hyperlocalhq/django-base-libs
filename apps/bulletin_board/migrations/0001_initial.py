# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import filebrowser.fields
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_populate_localitytype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0003_unique_member_slugs'),
        ('structure', '0003_remove_category_sort_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('bulletin_type', models.CharField(max_length=20, verbose_name='Type', choices=[('searching', 'Searching'), ('offering', 'Offering')])),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(max_length=300, verbose_name='Description')),
                ('institution_title', models.CharField(max_length=255, verbose_name='Institution title', blank=True)),
                ('institution_url', models.URLField(max_length=255, verbose_name='Institution URL', blank=True)),
                ('contact_person', models.CharField(max_length=255, verbose_name='Contact person')),
                ('phone', models.CharField(max_length=200, verbose_name='Phone', blank=True)),
                ('email', models.CharField(max_length=254, verbose_name='Email', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('image_description', models.TextField(default='', verbose_name='Image Description', blank=True)),
                ('source_url', models.URLField(max_length=255, verbose_name='Source URL', blank=True)),
                ('published_from', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published immediately.", null=True, verbose_name='publishing date', blank=True)),
                ('published_till', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published forever.", null=True, verbose_name='published until', blank=True)),
                ('status', models.CharField(default='published', max_length=20, verbose_name='Status', blank=True, choices=[('draft', 'Draft'), ('published', 'Published')])),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'Bulletin',
                'verbose_name_plural': 'Bulletins',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BulletinCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='Title', max_length=200, null=True, editable=False)),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('title_en', models.CharField(max_length=200, verbose_name='Title', blank=True)),
                ('title_de', models.CharField(max_length=200, verbose_name='Title')),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name': 'Bulletin Category',
                'verbose_name_plural': 'Bulletin Categories',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bulletin',
            name='bulletin_category',
            field=models.ForeignKey(verbose_name='Bulletin category', to='bulletin_board.BulletinCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bulletin',
            name='categories',
            field=mptt.fields.TreeManyToManyField(related_name='creative_industry_bulletin', verbose_name='Categories', to='structure.Category', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bulletin',
            name='creator',
            field=models.ForeignKey(related_name='bulletin_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bulletin',
            name='institution',
            field=models.ForeignKey(blank=True, to='institutions.Institution', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bulletin',
            name='locality_type',
            field=mptt.fields.TreeForeignKey(related_name='locality_bulletin', verbose_name='Locality type', blank=True, to='location.LocalityType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bulletin',
            name='modifier',
            field=models.ForeignKey(related_name='bulletin_modifier', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
    ]
