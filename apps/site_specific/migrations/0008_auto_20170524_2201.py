# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_specific', '0007_contextitem_completeness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimrequest',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
    ]
