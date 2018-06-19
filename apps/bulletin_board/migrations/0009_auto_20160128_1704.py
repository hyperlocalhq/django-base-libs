# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0008_auto_20160121_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='status',
            field=models.CharField(default='published', max_length=20, verbose_name='Status', blank=True, choices=[('draft', 'Draft'), ('published', 'Published'), ('import', 'Imported'), ('expired', 'Expired')]),
            preserve_default=True,
        ),
    ]
