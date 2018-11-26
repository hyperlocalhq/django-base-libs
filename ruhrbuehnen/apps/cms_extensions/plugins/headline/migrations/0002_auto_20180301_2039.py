# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('headline', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headline',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='headline_headline', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
    ]
