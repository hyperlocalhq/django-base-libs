# -*- coding: UTF-8 -*-
from django.db import models
import operator

# inspired by http://www.djangosnippets.org/snippets/166/
class ExtendedQuerySet(models.query.QuerySet):
    def __init__(self, *args, **kwargs):
        super(ExtendedQuerySet, self).__init__(*args, **kwargs)
        if args:
            self.model = args[0]
        else:
            self.model = kwargs.get("model", None)
        self.sort_order_map = None
        self.queryset_with_counts = self
        self.queryset_with_counts_default = self

    def __deepcopy__(self, memo):
        # based on http://groups.google.com/group/comp.lang.python/msg/170d9047a40f44d6?dmode=source
        import copy

        x = ExtendedQuerySet.__new__(ExtendedQuerySet)
        memo[id(self)] = x
        for n, v in self.__dict__.iteritems():
            setattr(x, n, copy.deepcopy(v, memo))
        return x

    def _get_table(self, model):
        return model._meta.db_table

    def _get_column(self, model, attr):
        return "%s.%s" % (self._get_table(model), model._meta.get_field(attr).column)

    def _get_related_column(self, model, attr):
        related = model._meta.get_field(attr).rel
        return "%s.%s" % (self._get_table(related.to), related.field_name)

    # method can be overwritten by subclasses (see fulltextsearch.py)
    def get_sort_order_mapper(self):
        return self.model.objects.get_sort_order_mapper()

    def get_sort_order_map(self):
        if not self.sort_order_map:
            sort_order_mapper = self.get_sort_order_mapper()
            sort_order_map = [
                (item, sort_order_mapper[item][1], sort_order_mapper[item][0])
                for item in sort_order_mapper
            ]
            sort_order_map.sort(key=operator.itemgetter(2))
            self.sort_order_map = sort_order_map
        return self.sort_order_map

    def get_order_by_clause(self, order_by_key):
        if self.get_sort_order_mapper().get(order_by_key, None):
            order_by_clause = self.get_sort_order_mapper()[order_by_key][2]

            for i in range(len(order_by_clause)):
                # check, if "order by related count" is used. That is indicated by a tuple
                if isinstance(order_by_clause[i], (tuple, list)):
                    self.queryset_with_counts = self.queryset_with_counts._count_related(
                        order_by_clause[i][1], "count%d" % i
                    )
                    order_by_clause[i] = "%scount%d" % (order_by_clause[i][0], i)
            return order_by_clause

    def get_default_order_by_clause(self):
        order_by_clause = self.get_sort_order_mapper()[self.get_sort_order_map()[0][0]][
            2
        ]

        for i in range(len(order_by_clause)):
            # check, if "order by related count" is used. That is indicated by a tuple
            if isinstance(order_by_clause[i], (tuple, list)):
                self.queryset_with_counts_default = self.queryset_with_counts_default._count_related(
                    order_by_clause[i][1], "count%d" % i
                )
                order_by_clause[i] = "%scount%d" % (order_by_clause[i][0], i)
        return order_by_clause

    def _related_count_sql(self, related, attr):
        return """SELECT COUNT(*) FROM %s WHERE %s = %s""" % (
            self._get_table(related),
            self._get_column(related, attr),
            self._get_related_column(related, attr),
        )

    def _count_related(self, query, count_attr=None, related_attr=None):
        """
        Count the rows matching `query` related to this model by their
        foreign key attribute `related_attr`, and store the result in
        `count_attr`.
        
        Article.objects.count_related(Visit).order_by('-visit__count')
        """

        """
        If `query` is a model class, use the all() method on its default
        manager as the query.
        """
        if isinstance(query, models.base.ModelBase):
            query = query._default_manager.all()

        """
        If `count_attr` is None, use the name of the module given in `query`
        suffixed with '__count'.
        """
        if count_attr is None:
            count_attr = query.model._meta.model_name + "__count"

        """    
        If `related_attr` is None, find the first foreign key field in the
        model queried by `query` relating to this model.
        """
        if related_attr is None:
            for field in query.model._meta.fields:
                if isinstance(field, models.related.RelatedField):
                    if field.rel.to is self.model:
                        related_attr = field.name

        select_count = self._related_count_sql(query.model, related_attr)
        joins, wheres, params = query._filters.get_sql(query.model._meta)
        if wheres:
            select_count += " AND %s" % wheres[0]
        return self.extra(select={count_attr: select_count}, params=params)

    def order_by(self, *field_names):
        """ 
        this is an overwritten version of hte QuerySet order_by function,
        which works with both, normal fields and those from a select in an 
        extra clause. Since the QSRF is up, there has to be made a difference. 
        The usual order_by doees not work with fields from a selct in an extra clause,
        for example:
            q = Entry.objects.extra(select={'is_recent': "pub_date > '2006-01-01'"})
            q = q.extra(order_by = ['-is_recent'])
        """
        return super(ExtendedQuerySet, self).order_by(*field_names)

    def sort_by(self, *args, **kwargs):

        default_order_by_clause = self.get_default_order_by_clause()
        order_by_clause = self.get_order_by_clause(*args)

        if (not args or not args[0]) and (not kwargs or len(kwargs) == 0):
            return self.queryset_with_counts_default.order_by(*default_order_by_clause)
        else:
            return self.queryset_with_counts.order_by(*order_by_clause)

    def __repr__(self):
        return "<ExtendedQuerySet>"
        # data = list(self[:REPR_OUTPUT_SIZE + 1])
        # if len(data) > REPR_OUTPUT_SIZE:
        #     data[-1] = "...(remaining elements truncated)..."
        # return repr(data)
