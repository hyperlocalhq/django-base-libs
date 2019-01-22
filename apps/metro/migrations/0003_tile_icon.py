# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metro', '0002_auto_20160111_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='tile',
            name='icon',
            field=models.CharField(max_length=30, verbose_name='Icon', blank=True),
            preserve_default=True,
        ),
    ]
