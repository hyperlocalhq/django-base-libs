# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def assign_localitytypes(apps, schema_editor):
    ContextItem = apps.get_model("site_specific", "ContextItem")
    LocalityType = apps.get_model("location", "LocalityType")
    for item in ContextItem.objects.all():
        if item.location_type:
            item.locality_type = LocalityType.objects.get(slug=item.location_type.slug)
            item.save()

undo = lambda apps, schema_editor: None


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_populate_localitytype'),
        ('site_specific', '0003_contextitem_locality_type'),
    ]

    operations = [
        migrations.RunPython(assign_localitytypes, undo),
    ]
