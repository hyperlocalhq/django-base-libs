# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0003_auto_20151218_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bulletin',
            name='source_url',
        ),
        migrations.AddField(
            model_name='bulletin',
            name='external_url',
            field=models.URLField(max_length=255, verbose_name='External URL', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bulletin',
            name='orig_published',
            field=models.DateTimeField(verbose_name='Originally published', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
