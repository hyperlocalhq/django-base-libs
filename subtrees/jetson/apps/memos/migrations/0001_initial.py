# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object', blank=True)),
            ],
            options={
                'verbose_name': 'memo',
                'verbose_name_plural': 'memos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemoCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('token', models.CharField(help_text="Unique generated identifier saved in the cookie at a visitor's computer", unique=True, max_length=20, verbose_name='Token')),
                ('expiration', models.DateTimeField(help_text='Cookie expiration date', verbose_name='Expiration')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='memo',
            name='collection',
            field=models.ForeignKey(verbose_name='Collection', to='memos.MemoCollection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='memo',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Related object's type (model)"),
            preserve_default=True,
        ),
    ]
