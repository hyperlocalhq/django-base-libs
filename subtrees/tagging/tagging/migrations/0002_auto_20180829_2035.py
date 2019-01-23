# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='name_es',
            field=models.CharField(db_index=True, max_length=50, verbose_name='name', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='name_fr',
            field=models.CharField(db_index=True, max_length=50, verbose_name='name', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='name_it',
            field=models.CharField(db_index=True, max_length=50, verbose_name='name', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='name_pl',
            field=models.CharField(db_index=True, max_length=50, verbose_name='name', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='name_tr',
            field=models.CharField(db_index=True, max_length=50, verbose_name='name', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug_es',
            field=models.SlugField(verbose_name='Slug for URIs', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug_fr',
            field=models.SlugField(verbose_name='Slug for URIs', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug_it',
            field=models.SlugField(verbose_name='Slug for URIs', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug_pl',
            field=models.SlugField(verbose_name='Slug for URIs', blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='slug_tr',
            field=models.SlugField(verbose_name='Slug for URIs', blank=True),
        ),
    ]
