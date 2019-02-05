# -*- coding: UTF-8 -*-
from django.db.models.query import QuerySet
from django.contrib.admin.views.main import ChangeList


class HierarchyChangeList(ChangeList):
    """
    extends the django.contrib.admin.views.main.ChangeList class
    for hierarchical structures. The filter method is overwritten
    """
    # overwritten
    def get_queryset(self, request):
        qs = super(HierarchyChangeList, self).get_queryset(request)
        # we have to get all parents of an item (recursively), even if the parent
        # is filtered out. Otherwise the hierarchical structure would be destroyed.
        # All the parents, which would be filtered out, are grayed out in the display.
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
            qs = qs | QuerySet(self.model).filter(pk__in=list(self.filtered_out))

        # Set ordering again.
        ordering = self.get_ordering(request, qs)
        qs = qs.order_by(*ordering)
        return qs
