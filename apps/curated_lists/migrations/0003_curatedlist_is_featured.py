# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curated_lists', '0002_auto_20160701_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='curatedlist',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='Featured'),
            preserve_default=True,
        ),
    ]
