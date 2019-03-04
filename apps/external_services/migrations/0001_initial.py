# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0001_initial'),
        ('sites', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectMapper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('external_id', models.CharField(max_length=512, verbose_name='External ID')),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
            ],
            options={
                'ordering': ('external_id',),
                'verbose_name': 'object mapper',
                'verbose_name_plural': 'object mappers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('url', models.URLField(verbose_name='URL')),
                ('api_key', models.CharField(default=b'', max_length=200, verbose_name='API Key', blank=True)),
                ('user', models.CharField(default=b'', max_length=200, verbose_name='User', blank=True)),
                ('password', models.CharField(default=b'', max_length=200, verbose_name='Password', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleImportSource',
            fields=[
                ('service_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='external_services.Service')),
                ('are_excerpts', models.BooleanField(default=False, help_text='Does the feed provide not full content, but excerpts? The link in the list of articles will lead to the external URL if full content is not provided.', verbose_name='Excerpts')),
                ('default_status', models.SmallIntegerField(default=0, help_text='Status to apply to the imported articles by default.', verbose_name='status', choices=[(0, 'Draft'), (1, 'Published')])),
                ('content_provider', models.ForeignKey(verbose_name='Content provider', blank=True, to='articles.ArticleContentProvider', null=True)),
                ('default_creative_sectors', mptt.fields.TreeManyToManyField(related_name='cs_ais', db_column=b'default_cs', to='structure.Term', blank=True, help_text='Creative sectors to apply to the imported articles by default.', null=True, verbose_name='Creative sectors')),
                ('default_sites', models.ManyToManyField(related_name='site_article_import_sources', to='sites.Site', blank=True, help_text='Sites to apply to the imported articles by default.', null=True, verbose_name='Sites')),
            ],
            options={
                'ordering': ('title',),
                'db_table': 'external_services_ais',
                'verbose_name': 'article-import source',
                'verbose_name_plural': 'article-import sources',
            },
            bases=('external_services.service',),
        ),
        migrations.CreateModel(
            name='ServiceActionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('request', base_libs.models.fields.PlainTextModelField(verbose_name='Request', blank=True)),
                ('response', base_libs.models.fields.PlainTextModelField(verbose_name='Response', blank=True)),
                ('response_code', models.IntegerField(verbose_name='Response Code', blank=True)),
                ('service', models.ForeignKey(verbose_name='Service', to='external_services.Service')),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'service-action log',
                'verbose_name_plural': 'service-action logs',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='objectmapper',
            name='service',
            field=models.ForeignKey(verbose_name='Service', to='external_services.Service'),
            preserve_default=True,
        ),
    ]
