# -*- coding: UTF-8 -*-
from __future__ import unicode_literals


def patch_generic_foreign_keys():
    ### Fix empty content_object retrieval when object_id is of CharField type
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.core.exceptions import ObjectDoesNotExist

    def GenericForeignKey__get__(self, instance, instance_type=None):
        if instance is None:
            return self

        try:
            return getattr(instance, self.cache_attr)
        except AttributeError:
            rel_obj = None

            # Make sure to use ContentType.objects.get_for_id() to ensure that
            # lookups are cached (see ticket #5570). This takes more code than
            # the naive ``getattr(instance, self.ct_field)``, but has better
            # performance when dealing with GFKs in loops and such.
            f = self.model._meta.get_field(self.ct_field)
            ct_id = getattr(instance, f.get_attname(), None)
            if ct_id is not None:
                ct = self.get_content_type(id=ct_id, using=instance._state.db)
                try:
                    # For object_id use None instead of ""
                    # (or instead of 0 which shouldn't be used by default anyway)
                    rel_obj_pk = getattr(instance, self.fk_field) or None
                    rel_obj = ct.get_object_for_this_type(pk=rel_obj_pk)
                except ObjectDoesNotExist:
                    pass
            setattr(instance, self.cache_attr, rel_obj)
            return rel_obj

    GenericForeignKey.__get__ = GenericForeignKey__get__


patch_generic_foreign_keys()