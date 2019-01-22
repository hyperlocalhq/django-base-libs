# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_article_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='featured_in_magazine',
            field=models.BooleanField(default=False, verbose_name='Featured in magazine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='importance_in_magazine',
            field=models.PositiveIntegerField(default=0, help_text='The bigger the number, the more up-front it will be shown in the magazine overview', verbose_name='Importance in magazine'),
            preserve_default=True,
        ),
    ]
