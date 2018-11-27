# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopproduct',
            name='workshops',
            field=models.ManyToManyField(to='workshops.Workshop', verbose_name='Related Workshops', blank=True),
        ),
    ]
