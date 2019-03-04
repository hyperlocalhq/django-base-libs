# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0007_auto_20181122_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='published_yyyy',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Year of Publishing', choices=[(2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028)]),
        ),
    ]
