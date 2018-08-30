# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perobjectgroup',
            name='title_es',
            field=models.CharField(max_length=80, verbose_name='title', blank=True),
        ),
        migrations.AddField(
            model_name='perobjectgroup',
            name='title_fr',
            field=models.CharField(max_length=80, verbose_name='title', blank=True),
        ),
        migrations.AddField(
            model_name='perobjectgroup',
            name='title_it',
            field=models.CharField(max_length=80, verbose_name='title', blank=True),
        ),
        migrations.AddField(
            model_name='perobjectgroup',
            name='title_pl',
            field=models.CharField(max_length=80, verbose_name='title', blank=True),
        ),
        migrations.AddField(
            model_name='perobjectgroup',
            name='title_tr',
            field=models.CharField(max_length=80, verbose_name='title', blank=True),
        ),
    ]
