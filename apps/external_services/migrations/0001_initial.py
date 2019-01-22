# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
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
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('url', models.URLField(verbose_name='Feed URL')),
                ('api_key', models.CharField(default=b'', max_length=200, verbose_name='API Key', blank=True)),
                ('user', models.CharField(default=b'', max_length=200, verbose_name='User', blank=True)),
                ('password', models.CharField(default=b'', max_length=200, verbose_name='Password', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
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
        ),
        migrations.AddField(
            model_name='objectmapper',
            name='service',
            field=models.ForeignKey(verbose_name='Service', to='external_services.Service'),
        ),
        migrations.AlterUniqueTogether(
            name='objectmapper',
            unique_together=set([('object_id', 'content_type', 'service')]),
        ),
    ]
