# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slideshows', '0002_auto_20160106_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='button',
            field=models.CharField(verbose_name='Title', max_length=200, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slide',
            name='button_de',
            field=models.CharField(max_length=200, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slide',
            name='button_en',
            field=models.CharField(max_length=200, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
