# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields
import django.db.models.deletion
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('path', filebrowser.fields.FileBrowseField(help_text='A path to a locally stored image, video, or audio file.', max_length=255, verbose_name='File path', blank=True)),
                ('external_url', base_libs.models.fields.URLField(help_text='A URL of an external image, video, or audio file.', verbose_name='External URL', blank=True)),
                ('splash_image_path', filebrowser.fields.FileBrowseField(help_text='Used for still images in Flash players and for thumbnails.', max_length=255, verbose_name='Splash-image path', blank=True)),
                ('file_type', models.CharField(default=b'-', max_length=1, editable=False, choices=[(b'-', 'Unknown'), (b'i', 'Image'), (b'v', 'Video'), (b'a', 'Audio'), (b'y', 'Youtube video'), (b'm', 'Vimeo video')])),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False, blank=True)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('title_de', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_fr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_pl', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_tr', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_es', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_it', models.CharField(max_length=255, verbose_name='Title', blank=True)),
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
                ('creator', models.ForeignKey(related_name='mediafile_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
            ],
            options={
                'ordering': ['sort_order', 'creation_date'],
                'abstract': False,
                'verbose_name': 'Media File',
                'verbose_name_plural': 'Media File',
            },
        ),
        migrations.CreateModel(
            name='MediaGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('views', models.IntegerField(default=0, verbose_name='views', editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('title', models.CharField(verbose_name='Title', max_length=100, null=True, editable=False, blank=True)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('content_object_repr', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', null=True, verbose_name='Content object representation')),
                ('content_object_id', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for grouping the sortable galleries.', verbose_name='Content object ID combo')),
                ('cover_image', filebrowser.fields.FileBrowseField(default=b'', max_length=255, verbose_name='Cover image', blank=True)),
                ('sort_order', base_libs.models.fields.PositionField(default=0, verbose_name='Sort order')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('title_de', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('title_en', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('title_fr', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('title_pl', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('title_tr', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('title_es', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('title_it', models.CharField(max_length=100, verbose_name='Title', blank=True)),
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
                ('content_object_repr_de', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_object_repr_en', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_object_repr_fr', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_object_repr_pl', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_object_repr_tr', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_object_repr_es', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_object_repr_it', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
            ],
            options={
                'ordering': ['sort_order', '-creation_date'],
                'abstract': False,
                'get_latest_by': 'creation_date',
                'verbose_name': 'Media Gallery',
                'verbose_name_plural': 'Media Galleries',
            },
        ),
        migrations.AddField(
            model_name='mediafile',
            name='gallery',
            field=models.ForeignKey(default=0, verbose_name='Media Gallery', to='media_gallery.MediaGallery'),
        ),
        migrations.AddField(
            model_name='mediafile',
            name='modifier',
            field=models.ForeignKey(related_name='mediafile_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
        ),
    ]
