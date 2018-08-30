# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorialContent',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='editorial_editorialcontent', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('subtitle', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('description', base_libs.models.fields.ExtendedTextField(verbose_name='Description', blank=True)),
                ('website', models.CharField(max_length=255, verbose_name='Website', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('image_caption', base_libs.models.fields.ExtendedTextField(max_length=255, verbose_name='Image Caption', blank=True)),
                ('col_xs_width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Column width for phones', choices=[(3, '25% of the full width'), (4, '33.3% of the full width'), (6, '50% of the full width'), (8, '66.6% of the full width'), (9, '75% of the full width'), (12, 'Full width')])),
                ('col_sm_width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Column width for tablets', choices=[(3, '25% of the full width'), (4, '33.3% of the full width'), (6, '50% of the full width'), (8, '66.6% of the full width'), (9, '75% of the full width'), (12, 'Full width')])),
                ('col_md_width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Column width for small desktops', choices=[(3, '25% of the full width'), (4, '33.3% of the full width'), (6, '50% of the full width'), (8, '66.6% of the full width'), (9, '75% of the full width'), (12, 'Full width')])),
                ('col_lg_width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Column width for large desktops', choices=[(3, '25% of the full width'), (4, '33.3% of the full width'), (6, '50% of the full width'), (8, '66.6% of the full width'), (9, '75% of the full width'), (12, 'Full width')])),
                ('css_class', models.CharField(max_length=255, verbose_name='CSS Class', blank=True)),
                ('description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('image_caption_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Editorial content',
                'verbose_name_plural': 'Editorial contents',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Footnote',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='editorial_footnote', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(default=b'Literatur', max_length=255, verbose_name='Title')),
                ('description', base_libs.models.fields.ExtendedTextField(verbose_name='Description', blank=True)),
                ('description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Footnote',
                'verbose_name_plural': 'Footnotes',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='FrontpageTeaser',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='editorial_frontpageteaser', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('title2', models.CharField(max_length=255, verbose_name='Title 2', blank=True)),
                ('title3', models.CharField(max_length=255, verbose_name='Title 3', blank=True)),
                ('description', base_libs.models.fields.ExtendedTextField(verbose_name='Description', blank=True)),
                ('website', models.CharField(max_length=255, verbose_name='Website', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('image_caption', base_libs.models.fields.ExtendedTextField(max_length=255, verbose_name='Image Caption', blank=True)),
                ('description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('image_caption_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Frontpage Teaser',
                'verbose_name_plural': 'Frontpage Teasers',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Intro',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='editorial_intro', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('subtitle', models.CharField(max_length=200, verbose_name='Subtitle', blank=True)),
                ('description', base_libs.models.fields.ExtendedTextField(verbose_name='Description', blank=True)),
                ('subdescription', base_libs.models.fields.ExtendedTextField(verbose_name='Subdescription', blank=True)),
                ('description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('subdescription_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Intro',
                'verbose_name_plural': 'Intros',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='TeaserBlock',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='editorial_teaserblock', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('subtitle', models.CharField(max_length=255, verbose_name='Subtitle', blank=True)),
                ('description', base_libs.models.fields.ExtendedTextField(verbose_name='Description', blank=True)),
                ('website', models.CharField(max_length=255, verbose_name='Website', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('image_caption', base_libs.models.fields.ExtendedTextField(max_length=255, verbose_name='Image Caption', blank=True)),
                ('description_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('image_caption_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Teaser',
                'verbose_name_plural': 'Teasers',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
