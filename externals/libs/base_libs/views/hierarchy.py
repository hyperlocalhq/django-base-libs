# -*- coding: UTF-8 -*-
from django.db.models.query import QuerySet
from django.contrib.admin.views.main import ChangeList
"""
extends the django.contrib.admin.views.main.ChangeList class 
for hierarchical structures. The filter method is overwritten
""" 
class HierarchyChangeList(ChangeList):
    # overwritten
    def get_query_set(self):
        qs = super(HierarchyChangeList, self).get_query_set()
        """
        we have to get all parents of an item (recursively), even if the parent
        is filtered out. Otherwise the hierarchical structure would be destroyed.
        All the parents, which would be filtered out, are grayed out in the display.
        """
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
        if self.order_field:
            qs = qs.order_by('%s%s' % ((self.order_type == 'desc' and '-' or ''), self.order_field))
        return qs
