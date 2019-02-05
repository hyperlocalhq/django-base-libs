# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_added_main_image_and_photo_credits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='image',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='photo_author',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=200, verbose_name='Main Image', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='image_author',
            field=models.CharField(max_length=100, verbose_name='Image Credits', blank=True),
        ),
    ]
