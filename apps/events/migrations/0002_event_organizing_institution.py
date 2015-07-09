# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organizing_institution',
            field=models.ForeignKey(verbose_name='Organizing institution', blank=True, to='institutions.Institution', null=True),
            preserve_default=True,
        ),
    ]
