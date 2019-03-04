# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160606_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='sites',
            field=models.ManyToManyField(help_text='Please select some sites, this container relates to. If you do not select any site, the container applies to all sites.', to='sites.Site', verbose_name='Sites', blank=True),
        ),
    ]
