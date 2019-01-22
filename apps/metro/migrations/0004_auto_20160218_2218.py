# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metro', '0003_tile_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tile',
            name='icon',
            field=models.CharField(help_text='The name of an icon (counselling version).', max_length=30, verbose_name='Icon', blank=True),
            preserve_default=True,
        ),
    ]
