# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulletinContentProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('url', base_libs.models.fields.URLField(verbose_name='URL', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'article-content provider',
                'verbose_name_plural': 'article-content providers',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='bulletin_category',
            field=models.ForeignKey(verbose_name='Bulletin category', blank=True, to='bulletin_board.BulletinCategory', null=True),
            preserve_default=True,
        ),
    ]
