# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0002_remove_sitesettings_registration_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagesettings',
            name='site',
            field=models.ForeignKey(verbose_name='Site', to='sites.Site'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='site',
            field=models.OneToOneField(verbose_name='Site', to='sites.Site'),
        ),
    ]
