# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tile',
            name='link_de',
            field=models.CharField(max_length=255, verbose_name='Link', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tile',
            name='link_en',
            field=models.CharField(max_length=255, verbose_name='Link', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tile',
            name='link',
            field=models.CharField(verbose_name='Link', max_length=255, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
