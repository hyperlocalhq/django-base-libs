# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_slugs_unique_together_with_usernames(apps, schema_editor):
    Institution = apps.get_model("institutions", "Institution")
    ContextItem = apps.get_model("site_specific", "ContextItem")
    ContentType = apps.get_model("contenttypes", "ContentType")
    try:
        ct = ContentType.objects.get(app_label="institutions", model="institution")
    except ContentType.DoesNotExist:
        return

    count = 0
    for inst in Institution.objects.all():
        item = ContextItem.objects.get(
            content_type=ct,
            object_id=inst.id,
        )
        if inst.slug != item.slug:
            inst.slug = item.slug
            inst.save()
            print(inst.slug)
            count += 1
    print("Institutions changed: %d" % count)


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_institution_categories'),
        ('site_specific', '0005_remove_contextitem_location_type'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(make_slugs_unique_together_with_usernames),
    ]
