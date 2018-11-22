# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_populate_localitytype'),
        ('site_specific', '0002_contextitem_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='contextitem',
            name='locality_type',
            field=mptt.fields.TreeForeignKey(verbose_name='Locality type', blank=True, to='location.LocalityType', null=True),
            preserve_default=True,
        ),
    ]
