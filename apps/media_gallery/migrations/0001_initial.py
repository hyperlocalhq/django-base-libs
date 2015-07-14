# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
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
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('creator', models.ForeignKey(related_name='mediafile_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
            ],
            options={
                'ordering': ['sort_order', 'creation_date'],
                'abstract': False,
                'verbose_name': 'Media File',
                'verbose_name_plural': 'Media File',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MediaGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('published_from', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published immediately.", null=True, verbose_name='publishing date', blank=True)),
                ('published_till', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published forever.", null=True, verbose_name='published until', blank=True)),
                ('status', models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Draft'), (1, 'Published')])),
                ('views', models.IntegerField(default=0, verbose_name='views', editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('title', models.CharField(verbose_name='Title', max_length=100, null=True, editable=False, blank=True)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('content_object_repr', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', null=True, verbose_name='Content object representation')),
                ('content_object_id', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for grouping the sortable galleries.', verbose_name='Content object ID combo')),
                ('cover_image', filebrowser.fields.FileBrowseField(default=b'', max_length=255, verbose_name='Cover image', blank=True)),
                ('sort_order', base_libs.models.fields.PositionField(default=0, verbose_name='Sort order')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('format', models.CharField(default=b'slideshow', max_length=20, verbose_name='Presentation format', choices=[(b'slideshow', 'Slideshow'), (b'listed', 'Large-scaled listing')])),
                ('title_de', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('title_en', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('content_object_repr_de', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_object_repr_en', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('author', models.ForeignKey(related_name='mediagallery_author', blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author')),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
            ],
            options={
                'ordering': ['sort_order', '-creation_date'],
                'abstract': False,
                'get_latest_by': 'creation_date',
                'verbose_name': 'Media Gallery',
                'verbose_name_plural': 'Media Galleries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PortfolioSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('content_object_repr', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', null=True, verbose_name='Content object representation')),
                ('content_object_id', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for grouping the sortable galleries.', verbose_name='Content object ID combo')),
                ('landing_page', models.CharField(default=b'first_album', max_length=20, verbose_name='Landing page', choices=[(b'first_album', 'First album'), (b'album_list', 'List of albums'), (b'custom_image', 'Custom image')])),
                ('landing_page_image', filebrowser.fields.FileBrowseField(help_text='A path to a custom landing page image.', max_length=255, verbose_name='Landing page image', blank=True)),
                ('content_object_repr_de', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_object_repr_en', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
            ],
            options={
                'verbose_name': 'Portfolio Settings',
                'verbose_name_plural': 'Portfolio Settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('title', models.CharField(verbose_name='Title', max_length=100, null=True, editable=False, blank=True)),
                ('content_object_repr', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', null=True, verbose_name='Content object representation')),
                ('content_object_id', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for grouping the sortable galleries.', verbose_name='Content object ID combo')),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('show_title', models.BooleanField(default=False, verbose_name='Show title')),
                ('title_de', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('title_en', models.CharField(max_length=100, verbose_name='Title', blank=True)),
                ('content_object_repr_de', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_object_repr_en', models.CharField(default=b'', editable=False, max_length=100, blank=True, help_text='Used for search and ordering in administration.', verbose_name='Content object representation')),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
            ],
            options={
                'verbose_name': 'Portfolio Section',
                'verbose_name_plural': 'Portfolio Sections',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mediagallery',
            name='section',
            field=models.ForeignKey(verbose_name='Section', blank=True, to='media_gallery.Section', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mediafile',
            name='gallery',
            field=models.ForeignKey(verbose_name='Media Gallery', to='media_gallery.MediaGallery'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mediafile',
            name='modifier',
            field=models.ForeignKey(related_name='mediafile_modifier', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
    ]
