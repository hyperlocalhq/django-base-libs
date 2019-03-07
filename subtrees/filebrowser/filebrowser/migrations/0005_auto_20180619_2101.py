# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filebrowser', '0004_populate_file_path_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedescription',
            name='copyright_limitations',
            field=models.CharField(max_length=300, verbose_name='Copyright limitations', blank=True),
        ),
    ]
