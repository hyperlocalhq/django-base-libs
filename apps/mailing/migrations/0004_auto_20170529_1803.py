# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_auto_20170524_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='allowed_placeholders',
            field=models.ManyToManyField(to='mailing.EmailTemplatePlaceholder', verbose_name='Allowed Placeholders', blank=True),
        ),
    ]
