# -*- coding: UTF-8 -*-

from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.core.paginator import Paginator

import haystack.views as haystack_views
from haystack import connections
from haystack.exceptions import NotHandled

from forms import ModelSearchForm
from functions import model_choices, get_dictionaries


class SearchView(haystack_views.SearchView):
    def __init__(self, template=None, load_all=True, form_class=ModelSearchForm, searchqueryset=None, context_class=RequestContext, results_per_page=None, limit=None):
        super(SearchView, self).__init__(template, load_all, form_class, searchqueryset, context_class, results_per_page)
        self.limit = limit

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        # sort by default order
        app_models, indexes = get_dictionaries()

        result_groups = []

        if self.form.is_valid():
            for short_name, verbose_name in model_choices():
                if self.form.cleaned_data[self.form.MODELS_PARAM_NAME] and short_name not in self.form.cleaned_data[self.form.MODELS_PARAM_NAME]:
                    continue
                app_model = indexes[short_name]  # e.g. "museums.museum"
                results = self.results.filter(django_ct=app_model)
                length = results.count()
                if length and results:
                    d = {
                        'short_name': short_name,
                        'verbose_name': verbose_name,
                        'count': length,
                        'results': results[:self.limit] if self.limit else results,
                    }
                    if self.limit is None and self.form.cleaned_data[self.form.MODELS_PARAM_NAME] == short_name:
                        paginator = Paginator(results, self.results_per_page)
                        try:
                            page = paginator.page(int(self.request.GET.get('page', 1)))
                        except:
                            raise Http404
                        d['paginator'] = paginator
                        d['page'] = page
                    result_groups.append(d)

        context = {
            'query': self.query,
            'form': self.form,
            'full': self.limit is None,
            'result_groups': result_groups
        }
        context.update(self.extra_context())

        return render_to_response(self.template, context, context_instance=self.context_class(self.request))
