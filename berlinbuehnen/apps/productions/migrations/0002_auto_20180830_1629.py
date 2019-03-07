# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='language_and_subtitles',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Language / Subtitles', blank=True, to='productions.LanguageAndSubtitles', null=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='language_and_subtitles',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Language / Subtitles', blank=True, to='productions.LanguageAndSubtitles', null=True),
        ),
    ]
