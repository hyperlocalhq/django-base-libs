# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('curated_lists', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curatedlist',
            name='owner',
        ),
        migrations.AddField(
            model_name='curatedlist',
            name='owner_content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Owner's type (model)"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curatedlist',
            name='owner_object_id',
            field=models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Owner', blank=True),
            preserve_default=True,
        ),
    ]
