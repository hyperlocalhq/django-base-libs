# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug_de', models.SlugField(verbose_name='Slug for URIs')),
                ('slug_en', models.SlugField(verbose_name='Slug for URIs', blank=True)),
                ('slug', models.SlugField(verbose_name='Slug for URIs', null=True, editable=False)),
                ('name', models.CharField(verbose_name='name', max_length=50, null=True, editable=False, db_index=True)),
                ('name_de', models.CharField(max_length=50, verbose_name='name', db_index=True)),
                ('name_en', models.CharField(db_index=True, max_length=50, verbose_name='name', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='object id', db_index=True)),
                ('content_type', models.ForeignKey(verbose_name='content type', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(related_name='items', verbose_name='tag', to='tagging.Tag')),
            ],
            options={
                'verbose_name': 'tagged item',
                'verbose_name_plural': 'tagged items',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='taggeditem',
            unique_together=set([('tag', 'content_type', 'object_id')]),
        ),
    ]
