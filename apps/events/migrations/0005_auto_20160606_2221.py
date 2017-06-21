# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20160107_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(related_name='event_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='modifier',
            field=models.ForeignKey(related_name='event_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
    ]
