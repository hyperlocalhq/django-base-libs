# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base_libs.models.fields
import tagging_autocomplete.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object', blank=True)),
                ('sysname', models.CharField(help_text="Please specify an additional URL identifier for the container here. The provided name must be the last part of the calling url, which wants to access the container. For example, if you have a FAQ-Container and you want to use the url 'http://www.example.com/gettinghelp/faqs/', the URL identifier must be 'faqs'. For different URL identifiers, you can create multiple containers for the same related object and site. Note, that the site, the related object and the URL identifier must be unique together.", max_length=255, verbose_name='URL Identifier')),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Related object's type (model)")),
                ('sites', models.ManyToManyField(help_text='Please select some sites, this container relates to. If you do not select any site, the container applies to all sites.', to='sites.Site', null=True, verbose_name='Sites', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'abstract': False,
                'verbose_name': 'blog',
                'verbose_name_plural': 'blogs',
                'permissions': (('add_blog_posts', 'Can add posts'), ('change_blog_posts', 'Can change posts'), ('delete_blog_posts', 'Can delete posts'), ('moderate_blog_comments', 'Can moderate blog comments')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('published_from', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published immediately.", null=True, verbose_name='publishing date', blank=True)),
                ('published_till', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published forever.", null=True, verbose_name='published until', blank=True)),
                ('status', models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Draft'), (1, 'Published')])),
                ('views', models.IntegerField(default=0, verbose_name='views', editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('tags', tagging_autocomplete.models.TagAutocompleteField(default=b'', help_text='Separate different tags by comma', max_length=255, verbose_name='tags', blank=True)),
                ('body', base_libs.models.fields.ExtendedTextField(verbose_name='body')),
                ('enable_comment_form', models.BooleanField(default=True, verbose_name='enable comment form')),
                ('body_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('author', models.ForeignKey(related_name='post_author', blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author')),
                ('blog', models.ForeignKey(related_name='blog', to='blog.Blog')),
                ('creator', models.ForeignKey(related_name='post_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('modifier', models.ForeignKey(related_name='post_modifier', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
            ],
            options={
                'ordering': ('-published_from',),
                'get_latest_by': 'published_from',
                'verbose_name': 'blog post',
                'verbose_name_plural': 'blog posts',
            },
            bases=(models.Model,),
        ),
    ]
