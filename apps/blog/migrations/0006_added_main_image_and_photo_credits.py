# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170529_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=200, verbose_name='Main Image', blank=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='photo_author',
            field=models.CharField(max_length=100, verbose_name='Photo', blank=True),
        ),
    ]
