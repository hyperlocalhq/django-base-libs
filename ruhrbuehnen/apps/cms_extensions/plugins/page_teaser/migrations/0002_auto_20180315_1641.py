# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('page_teaser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageteaser',
            name='internal_link',
            field=cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Internal link', blank=True, to='cms.Page', null=True),
        ),
    ]
