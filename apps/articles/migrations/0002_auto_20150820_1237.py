# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='language',
            field=models.CharField(default=b'', max_length=5, verbose_name='Language', blank=True, choices=[(b'en', b'en'), (b'de', b'de')]),
            preserve_default=True,
        ),
    ]
