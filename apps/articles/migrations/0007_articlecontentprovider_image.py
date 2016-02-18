# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20160217_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecontentprovider',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True),
            preserve_default=True,
        ),
    ]
