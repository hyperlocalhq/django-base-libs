# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noticetype',
            options={'ordering': ('sort_order', 'category__title', 'display'), 'verbose_name': 'notice type', 'verbose_name_plural': 'notice types'},
        ),
        migrations.AddField(
            model_name='noticetype',
            name='sort_order',
            field=models.IntegerField(default=0, verbose_name='Sort Order'),
            preserve_default=True,
        ),
    ]
