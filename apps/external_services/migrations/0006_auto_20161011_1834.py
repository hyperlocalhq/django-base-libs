# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('external_services', '0005_auto_20160324_1720'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='objectmapper',
            unique_together=set([('object_id', 'content_type', 'service')]),
        ),
    ]
