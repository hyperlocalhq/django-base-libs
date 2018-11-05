# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_document_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='end',
            field=models.DateField(null=True, verbose_name='End', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='start',
            field=models.DateField(null=True, verbose_name='Start', blank=True),
            preserve_default=True,
        ),
    ]
