# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='status',
            field=models.CharField(default='d', max_length=1, verbose_name='Publishing status', choices=[('d', 'Draft'), ('p', 'Published')]),
        ),
    ]
