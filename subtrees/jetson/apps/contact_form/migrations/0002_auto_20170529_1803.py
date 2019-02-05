# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contact_form', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactformcategory',
            name='recipients',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Recipient(s)', blank=True),
        ),
    ]
