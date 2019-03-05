# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import base_libs.models.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20180829_2035'),
        ('exhibitions', '0001_initial'),
        ('museums', '0001_initial'),
        ('i18n', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='Name', max_length=255, null=True, editable=False)),
                ('subtitle', models.CharField(verbose_name='Subtitle', max_length=255, null=True, editable=False, blank=True)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image')),
                ('price', models.DecimalField(null=True, verbose_name='Price (\u20ac)', max_digits=5, decimal_places=2, blank=True)),
                ('link', models.URLField(max_length=255, verbose_name='Order link')),
                ('is_featured', models.BooleanField(verbose_name='Featured')),
                ('is_for_children', models.BooleanField(verbose_name='For children')),
                ('is_new', models.BooleanField(verbose_name='New')),
                ('status', models.CharField(default=b'draft', max_length=20, verbose_name='Status', blank=True, choices=[(b'draft', 'Draft'), (b'published', 'Published'), (b'trashed', 'Trashed')])),
                ('subtitle_de', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_en', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_fr', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_pl', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_tr', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_es', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('subtitle_it', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('title_de', models.CharField(max_length=255, verbose_name='Name')),
                ('title_en', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('title_fr', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('title_pl', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('title_tr', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('title_es', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('title_it', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_fr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_fr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_pl', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_pl_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_tr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_tr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_es', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_es_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_it', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True)),
                ('description_it_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('events', models.ManyToManyField(to='events.Event', verbose_name='Related Events', blank=True)),
                ('exhibitions', models.ManyToManyField(to='exhibitions.Exhibition', verbose_name='Related Exhibitions', blank=True)),
                ('languages', models.ManyToManyField(to='i18n.Language', verbose_name='Languages', blank=True)),
                ('museums', models.ManyToManyField(to='museums.Museum', verbose_name='Related Museums', blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ShopProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_fr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_pl', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_tr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_es', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_it', models.CharField(max_length=255, verbose_name='Title', blank=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
            },
        ),
        migrations.CreateModel(
            name='ShopProductType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_fr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_pl', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_tr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_es', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_it', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='shop.ShopProductType', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'Product Type',
                'verbose_name_plural': 'Product Types',
            },
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='product_categories',
            field=models.ManyToManyField(to='shop.ShopProductCategory', verbose_name='Categories', blank=True),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='product_types',
            field=mptt.fields.TreeManyToManyField(to='shop.ShopProductType', verbose_name='Types', blank=True),
        ),
    ]
