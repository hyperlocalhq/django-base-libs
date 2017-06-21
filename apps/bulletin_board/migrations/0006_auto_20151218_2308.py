# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0005_auto_20151218_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='description',
            field=models.TextField(verbose_name='Description'),
            preserve_default=True,
        ),
    ]
