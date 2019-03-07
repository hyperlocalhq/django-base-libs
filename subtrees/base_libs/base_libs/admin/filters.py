# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
try:
    from django.contrib.admin.filters import FieldListFilter, RelatedFieldListFilter
except:
    # fallback for Django 1.3
    pass
else:
    """
    Some additional filterspecs classes for instance for filtering by hierarchical data.
    All the classes below have to be pushed manually onto the top of the  FilterSpec.filter_specs
    list. Only registering is not enough!
    """
    class HierarchyRelatedFilterSpec(RelatedFieldListFilter):

        def __init__(self, f, request, params, model, model_admin, field_path=None):
            super(HierarchyRelatedFilterSpec, self).__init__(f, request, params, model, model_admin, field_path=field_path)

            """
            we have to get all parents of an item (recursively), even if the parent
            is filtered out. Otherwise the hierarchical structure would be destroyed.
            All the parents, which would be filtered out, are grayed out in the display.
            """
            if isinstance(f, models.ManyToManyField):
                # get the pk of objects many-to-many-related to objects of model
                # i.e.:
                # restrict_to = Category.objects.exclude(
                #     item=None,
                #     ).values_list("pk", flat=True)
                restrict_to = f.rel.to._default_manager.exclude(**{
                    f.rel.get_related_field().name: None,
                    }).values_list("pk", flat=True)
                self.lookup_title = f.rel.to._meta.verbose_name
            else:
                # get the pk of objects many-to-one-related to objects of model
                # i.e.:
                # restrict_to = Item.objects.values_list("category", flat=True)
                restrict_to = model._default_manager.values_list(
                    f.attname,
                    flat=True,
                    )
                self.lookup_title = f.verbose_name
            qs = f.rel.to._default_manager.filter(pk__in=restrict_to)
            self.filtered_out = {}
            if qs.count():
                # all parents list:
                for item in qs:
                    parent = item.parent
                    while parent:
                        # maybe append parent to "filtered_out_list"
                        if qs.filter(pk=parent.pk).count() == 0:
                            self.filtered_out[parent.pk] = True
                        parent = parent.parent
                qs = qs | f.rel.to._default_manager.filter(pk__in=list(self.filtered_out))

            self.lookup_choices = [item for item in qs]

        def is_hierarchical(self):
            return True

        def choices(self, cl):
            yield {'filtered_out' : False,
                   'selected': self.lookup_val is None,
                   'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                   'display': {'pk' : 'all', 'parent_pk' : None, 'val': _('All')}
                   }

            for item in self.lookup_choices:
                parent_pk_val = None
                if item.parent:
                    parent_pk_val = item.parent.pk

                yield {
                    'filtered_out': self.filtered_out.has_key(item.pk),
                    'selected': self.lookup_val == smart_unicode(item.pk),
                    'query_string': cl.get_query_string({self.lookup_kwarg: item.pk}),
                    'display': {
                        'pk': item.pk,
                        'parent_pk': parent_pk_val,
                        'val': ("%s %s" % ("-" * item.get_level(), unicode(item))).strip(),
                        },
                    }

    FieldListFilter.register(lambda f: bool(f.rel) and getattr(f.rel.to, 'is_hierarchical', False), HierarchyRelatedFilterSpec)

    """
    as the newly registered FilterSpec class is at the end of the test_list now,
    it would never be tested! So, wo push the newly created class at the top of
    filter_specs
    """
    #tmp = FilterSpec.filter_specs.pop()
    #FilterSpec.filter_specs.insert(0, tmp)

