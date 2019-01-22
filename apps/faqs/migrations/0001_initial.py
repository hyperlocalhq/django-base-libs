# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=512, null=True, editable=False)),
                ('short_title', models.CharField(help_text='a short title to be displayed in page breadcrumbs and headline.', max_length=80, null=True, editable=False, verbose_name='short title')),
                ('description', models.TextField(default=b'', editable=False, max_length=8192, blank=True, null=True, verbose_name='description')),
                ('children_sort_order_format', models.CharField(default=b'%02d', max_length=20, blank=True, help_text="sort order format for children (python style, e.g '%d')", null=True, verbose_name='format for child categories')),
                ('faqs_on_separate_page', models.BooleanField(default=False, help_text="check, if you want to display relating faqs on a separate page. If this category is not a 'leaf category', it has no effect.", verbose_name='separate page')),
                ('title_de', models.CharField(max_length=512, verbose_name='title')),
                ('title_en', models.CharField(max_length=512, verbose_name='title', blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', max_length=8192, null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', max_length=8192, null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('short_title_de', models.CharField(help_text='a short title to be displayed in page breadcrumbs and headline.', max_length=80, verbose_name='short title')),
                ('short_title_en', models.CharField(help_text='a short title to be displayed in page breadcrumbs and headline.', max_length=80, verbose_name='short title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'FAQ Category',
                'verbose_name_plural': 'FAQ Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqContainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object', blank=True)),
                ('sysname', models.CharField(help_text="Please specify an additional URL identifier for the container here. The provided name must be the last part of the calling url, which wants to access the container. For example, if you have a FAQ-Container and you want to use the url 'http://www.example.com/gettinghelp/faqs/', the URL identifier must be 'faqs'. For different URL identifiers, you can create multiple containers for the same related object and site. Note, that the site, the related object and the URL identifier must be unique together.", max_length=255, verbose_name='URL Identifier')),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False, blank=True)),
                ('title_de', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Related object's type (model)")),
                ('sites', models.ManyToManyField(help_text='Please select some sites, this container relates to. If you do not select any site, the container applies to all sites.', to='sites.Site', null=True, verbose_name='Sites', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'abstract': False,
                'verbose_name': 'FAQ Container',
                'verbose_name_plural': 'FAQ Containers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('views', models.IntegerField(default=0, verbose_name='views', editable=False)),
                ('sort_order', models.IntegerField(verbose_name='sort order')),
                ('question', models.CharField(verbose_name='question', max_length=255, null=True, editable=False)),
                ('answer', models.TextField(default=b'', max_length=16384, null=True, editable=False, verbose_name='answer')),
                ('question_de', models.CharField(max_length=255, verbose_name='question')),
                ('question_en', models.CharField(max_length=255, verbose_name='question', blank=True)),
                ('answer_de', base_libs.models.fields.ExtendedTextField(default=b'', max_length=16384, null=True, verbose_name='Antwort')),
                ('answer_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('answer_en', base_libs.models.fields.ExtendedTextField(default=b'', max_length=16384, null=True, verbose_name='Antwort', blank=True)),
                ('answer_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('category', mptt.fields.TreeForeignKey(verbose_name='category', to='faqs.FaqCategory')),
                ('creator', models.ForeignKey(related_name='questionanswer_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('modifier', models.ForeignKey(related_name='questionanswer_modifier', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
            ],
            options={
                'ordering': ['category'],
                'verbose_name': 'Question-Answer',
                'verbose_name_plural': 'Questions-Answers',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='faqcategory',
            name='container',
            field=models.ForeignKey(verbose_name='container', to='faqs.FaqContainer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faqcategory',
            name='creator',
            field=models.ForeignKey(related_name='faqcategory_creator', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faqcategory',
            name='modifier',
            field=models.ForeignKey(related_name='faqcategory_modifier', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faqcategory',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='faqs.FaqCategory', null=True),
            preserve_default=True,
        ),
    ]
