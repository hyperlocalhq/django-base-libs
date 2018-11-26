# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
import django.db.models.deletion
import cms.models.fields
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('locations', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAndText',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200, verbose_name='Title', blank=True)),
                ('subtitle', models.CharField(max_length=200, verbose_name='Subtitle', blank=True)),
                ('body', base_libs.models.fields.ExtendedTextField(verbose_name='Body')),
                ('external_link', models.URLField(max_length=255, verbose_name='External Link', blank=True)),
                ('link_text', models.CharField(default='Yes, please', max_length=20, verbose_name='Link Text', choices=[('Yes, please', 'Yes, please'), ('more', 'more')])),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image')),
                ('alt', models.CharField(max_length=200, verbose_name='Alternative text', blank=True)),
                ('layout', models.CharField(default='image-left', max_length=20, verbose_name='Layout', choices=[('image-left', 'Image on the left'), ('image-right', 'Image on the right'), ('image-top', 'Image at the top'), ('image-bottom', 'Image at the bottom')])),
                ('body_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('internal_link', cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Internal link', blank=True, to='cms.Page', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='IndexItem',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('width', models.CharField(default='single', max_length=20, verbose_name='Width', choices=[('single', 'Single'), ('double', 'Double')])),
                ('external_link', models.URLField(max_length=255, verbose_name='External Link', blank=True)),
                ('banner', models.ForeignKey(verbose_name='Banner', to='services.Banner')),
                ('internal_link', cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Internal link', blank=True, to='cms.Page', null=True)),
            ],
            options={
                'verbose_name': 'Index Page Item',
                'verbose_name_plural': 'Index Page Items',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='LinkCategory',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Link Category',
                'verbose_name_plural': 'Link Categories',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('url', models.URLField(verbose_name='URL')),
                ('short_description', models.TextField(verbose_name='Short Description', blank=True)),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
            ],
            options={
                'ordering': ['sort_order'],
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='link',
            name='category',
            field=models.ForeignKey(to='services.LinkCategory'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ServiceGridItem',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('subtitle', models.CharField(max_length=200, verbose_name='Subtitle', blank=True)),
                ('short_description', base_libs.models.fields.ExtendedTextField(verbose_name='Short Description', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(help_text='A path to a locally stored image.', max_length=255, verbose_name='Header Icon', blank=True)),
                ('external_link', models.URLField(max_length=255, verbose_name='External Link', blank=True)),
                ('short_description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('internal_link', cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Internal link', blank=True, to='cms.Page', null=True)),
            ],
            options={
                'verbose_name': 'Grid Item',
                'verbose_name_plural': 'Grid Items',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ServiceListItem',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('subtitle', models.CharField(max_length=200, verbose_name='Subtitle', blank=True)),
                ('short_description', base_libs.models.fields.ExtendedTextField(verbose_name='Short Description', blank=True)),
                ('external_link', models.URLField(max_length=255, verbose_name='External Link', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(help_text='A path to a locally stored image.', max_length=255, verbose_name='Image', blank=True)),
                ('link_text', models.CharField(default='Yes, please', max_length=20, verbose_name='Link Text', choices=[('Yes, please', 'Yes, please'), ('more', 'more')])),
                ('short_description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('location', models.ForeignKey(blank=True, to='locations.Location', help_text='Theater linked to this service', null=True, verbose_name='Location')),
            ],
            options={
                'verbose_name': 'List Item',
                'verbose_name_plural': 'List Items',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='ServicePageBanner',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('banner', models.ForeignKey(verbose_name='Banner', to='services.Banner')),
            ],
            options={
                'verbose_name': 'Service Page Banner',
                'verbose_name_plural': 'Service Page Banners',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='TitleAndText',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200, verbose_name='Title', blank=True)),
                ('subtitle', models.CharField(max_length=200, verbose_name='Subtitle', blank=True)),
                ('body', base_libs.models.fields.ExtendedTextField(verbose_name='Body')),
                ('external_link', models.URLField(max_length=255, verbose_name='External Link', blank=True)),
                ('link_text', models.CharField(default='Yes, please', max_length=20, verbose_name='Link Text', choices=[('Yes, please', 'Yes, please'), ('more', 'more')])),
                ('width', models.CharField(default='full', max_length=20, verbose_name='Width', choices=[('full', 'Full'), ('half', 'Half')])),
                ('body_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('internal_link', cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Internal link', blank=True, to='cms.Page', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
