# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='editorial_document', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='questionanswer',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='editorial_questionanswer', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
    ]
