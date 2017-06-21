# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base_libs.models.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('published_from', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published immediately.", null=True, verbose_name='publishing date', blank=True)),
                ('published_till', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published forever.", null=True, verbose_name='published until', blank=True)),
                ('status', models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Draft'), (1, 'Published')])),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('subtitle', models.CharField(verbose_name='subtitle', max_length=255, null=True, editable=False, blank=True)),
                ('short_title', models.CharField(verbose_name='short title', max_length=32, null=True, editable=False, blank=True)),
                ('content', models.TextField(default=b'', verbose_name='content', null=True, editable=False, blank=True)),
                ('url', models.CharField(help_text="All that goes after '/', for example: 'about/contact/'. Make sure to have trailing slash.", max_length=100, verbose_name='URL', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='image', blank=True)),
                ('image_title', models.CharField(verbose_name='image title', max_length=50, null=True, editable=False, blank=True)),
                ('image_description', models.TextField(default=b'', verbose_name='image description', null=True, editable=False, blank=True)),
                ('enable_comments', models.BooleanField(default=False, verbose_name='enable comments')),
                ('template_name', models.CharField(help_text="Example: 'flatpages/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'.", max_length=70, verbose_name='template name', blank=True)),
                ('registration_required', models.BooleanField(default=False, help_text='If this is checked, only logged-in users will be able to view the page.', verbose_name='registration required')),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('subtitle_de', models.CharField(max_length=255, verbose_name='subtitle', blank=True)),
                ('subtitle_en', models.CharField(max_length=255, verbose_name='subtitle', blank=True)),
                ('short_title_de', models.CharField(max_length=32, verbose_name='short title', blank=True)),
                ('short_title_en', models.CharField(max_length=32, verbose_name='short title', blank=True)),
                ('content_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt', blank=True)),
                ('content_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('content_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Inhalt', blank=True)),
                ('content_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('image_title_de', models.CharField(max_length=50, verbose_name='image title', blank=True)),
                ('image_title_en', models.CharField(max_length=50, verbose_name='image title', blank=True)),
                ('image_description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Bildbeschreibung', blank=True)),
                ('image_description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('image_description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Bildbeschreibung', blank=True)),
                ('image_description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('author', models.ForeignKey(related_name='flatpage_author', blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author')),
                ('creator', models.ForeignKey(related_name='flatpage_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('modifier', models.ForeignKey(related_name='flatpage_modifier', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
                ('sites', models.ManyToManyField(help_text='Restrict this object only for the selected site', to='sites.Site', verbose_name='Site')),
            ],
            options={
                'ordering': ('url',),
                'abstract': False,
                'verbose_name': 'flat page',
                'verbose_name_plural': 'flat pages',
            },
            bases=(models.Model,),
        ),
    ]
