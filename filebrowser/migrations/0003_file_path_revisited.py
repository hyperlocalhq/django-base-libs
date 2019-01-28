# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filebrowser', '0002_auto_20180301_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedescription',
            name='file_path_hash',
            field=models.CharField(db_index=True, max_length=64, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='file_path',
            field=filebrowser.fields.FileBrowseField(max_length=500, verbose_name='File path'),
        ),
    ]
