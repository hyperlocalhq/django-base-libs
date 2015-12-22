# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0004_auto_20151218_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='status',
            field=models.CharField(default='published', max_length=20, verbose_name='Status', blank=True, choices=[('draft', 'Draft'), ('published', 'Published'), ('import', 'Imported')]),
            preserve_default=True,
        ),
    ]
