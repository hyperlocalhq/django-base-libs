# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_localitytype(apps, schema_editor):
    Term = apps.get_model("structure", "Term")
    LocalityType = apps.get_model("location", "LocalityType")
    for t_root in Term.objects.filter(
        vocabulary__sysname="basics_locality",
        level=0,
    ).order_by("tree_id", "lft"):
        lt_root = LocalityType()
        # the models in data migrations get no methods from the original model, only fields,
        # so we get the MPTT values from the Term
        lt_root.tree_id = t_root.tree_id
        lt_root.lft = t_root.lft
        lt_root.rght = t_root.rght
        lt_root.level = t_root.level
        # copy other field values
        lt_root.title_de = t_root.title_de
        lt_root.title_en = t_root.title_en
        lt_root.slug = t_root.slug
        lt_root.save()
        for t_child in Term.objects.filter(
            vocabulary__sysname="basics_locality",
            parent=t_root,
        ).order_by('lft'):
            lt_child = LocalityType(parent=lt_root)
            # the models in data migrations get no methods from the original model, only fields,
            # so we get the MPTT values from the Term
            lt_child.tree_id = t_child.tree_id
            lt_child.lft = t_child.lft
            lt_child.rght = t_child.rght
            lt_child.level = t_child.level
            # copy other field values
            lt_child.title_de = t_child.title_de
            lt_child.title_en = t_child.title_en
            lt_child.slug = t_child.slug
            lt_child.save()

    '''
    After this migration, the following needs to be called to fix tree_ids:
    >>> from jetson.apps.location.models import LocalityType
    >>> LocalityType.objects.rebuild()
    '''


undo = lambda apps, schema_editor: None


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_localitytype'),
        ('structure', '0003_remove_category_sort_order'),
    ]

    operations = [
        migrations.RunPython(populate_localitytype, undo),
    ]
