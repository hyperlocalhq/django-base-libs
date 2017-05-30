# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmap',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='gmap_gmap', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
    ]
