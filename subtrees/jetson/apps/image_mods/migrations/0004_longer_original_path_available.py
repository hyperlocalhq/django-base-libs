# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('image_mods', '0003_auto_20180301_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagecropping',
            name='original',
            field=filebrowser.fields.FileBrowseField(max_length=500, verbose_name='Original'),
        ),
    ]
