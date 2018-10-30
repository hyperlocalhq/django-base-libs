# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curated_lists', '0009_curatedlist_image_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email address', blank=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First name', blank=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='institution_title',
            field=models.CharField(max_length=255, verbose_name='Institution title', blank=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Last name', blank=True),
        ),
        migrations.AlterField(
            model_name='listowner',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email address', blank=True),
        ),
        migrations.AlterField(
            model_name='listowner',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First name', blank=True),
        ),
        migrations.AlterField(
            model_name='listowner',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Last name', blank=True),
        ),
    ]
