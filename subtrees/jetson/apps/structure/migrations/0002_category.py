# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='structure.Category', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
    ]
