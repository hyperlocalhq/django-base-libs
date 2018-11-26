# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_remove_location_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='press_contact_name',
        ),
        migrations.RemoveField(
            model_name='location',
            name='press_email',
        ),
        migrations.RemoveField(
            model_name='location',
            name='press_fax_area',
        ),
        migrations.RemoveField(
            model_name='location',
            name='press_fax_country',
        ),
        migrations.RemoveField(
            model_name='location',
            name='press_fax_number',
        ),
        migrations.RemoveField(
            model_name='location',
            name='press_phone_area',
        ),
        migrations.RemoveField(
            model_name='location',
            name='press_phone_country',
        ),
        migrations.RemoveField(
            model_name='location',
            name='press_phone_number',
        ),
        migrations.RemoveField(
            model_name='location',
            name='press_website',
        ),
    ]
