# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('structure', '0005_auto_20170529_1803'),
        ('curated_lists', '0005_auto_20160901_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('owner_object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Owner', blank=True)),
                ('representation', models.CharField(verbose_name='Representation', max_length=255, null=True, editable=False, blank=True)),
                ('representation_en', models.CharField(max_length=255, verbose_name='Representation', blank=True)),
                ('representation_de', models.CharField(max_length=255, verbose_name='Representation', blank=True)),
            ],
            options={
                'ordering': ['creation_date'],
                'verbose_name': 'List Owner',
                'verbose_name_plural': 'List Owners',
            },
        ),
        migrations.RemoveField(
            model_name='curatedlist',
            name='owner_content_type',
        ),
        migrations.RemoveField(
            model_name='curatedlist',
            name='owner_object_id',
        ),
        migrations.AddField(
            model_name='curatedlist',
            name='categories',
            field=mptt.fields.TreeManyToManyField(to='structure.Category', verbose_name='categories', blank=True),
        ),
        migrations.AddField(
            model_name='listowner',
            name='curated_list',
            field=models.ForeignKey(verbose_name='Curated list', to='curated_lists.CuratedList'),
        ),
        migrations.AddField(
            model_name='listowner',
            name='owner_content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Owner's type (model)"),
        ),
    ]
