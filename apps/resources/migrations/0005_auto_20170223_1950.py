# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20160901_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='published_yyyy',
            field=models.IntegerField(blank=True, null=True, verbose_name='Year of Publishing', choices=[(2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026)]),
            preserve_default=True,
        ),
    ]
