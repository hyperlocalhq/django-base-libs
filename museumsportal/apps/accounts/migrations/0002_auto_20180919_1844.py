# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='privacysettings',
            options={'ordering': ['user__username'], 'verbose_name': 'Privatsph\xe4re', 'verbose_name_plural': 'Privatsph\xe4re'},
        ),
        migrations.AlterField(
            model_name='privacysettings',
            name='display_to_public',
            field=models.BooleanField(default=True, verbose_name='Profil \xf6ffentlich anzeigen'),
        ),
        migrations.AlterField(
            model_name='privacysettings',
            name='display_username',
            field=models.BooleanField(default=False, verbose_name='Nutzernamen anzeigen an Stelle des Anmeldenamens'),
        ),
    ]
