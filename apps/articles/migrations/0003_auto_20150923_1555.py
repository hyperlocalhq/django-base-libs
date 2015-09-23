# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20150820_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='orig_published',
            field=models.DateTimeField(verbose_name='Originally published', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='language',
            field=models.CharField(default=b'', max_length=5, verbose_name='Language', blank=True, choices=[(b'en', b'English'), (b'de', b'German')]),
            preserve_default=True,
        ),
    ]
