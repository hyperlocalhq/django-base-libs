# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0001_initial'),
        ('internal_links', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkgroup',
            name='workshops',
            field=models.ManyToManyField(to='workshops.Workshop', verbose_name='Guided Tours', blank=True),
        ),
    ]
