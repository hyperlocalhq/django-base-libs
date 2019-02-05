# -*- coding: UTF-8 -*-
# inspired by recipe from http://code.activestate.com/recipes/576974-show-all-url-patterns-in-django/

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    def handle(self, *args, **options):
        pass

    help = """Prints a list of all URL regex patterns"""

    def handle_noargs(self, **options):
        import urls

        result = self.collect_urls(urls.urlpatterns)
        # pprint.pprint(result)
        concatenated_result = self.concatenate_ancestors(result)
        # pprint.pprint(concatenated_result)
        self.print_keys(concatenated_result)

    def collect_urls(self, urllist):
        d = {}
        for entry in urllist:
            d[entry.regex.pattern] = None
            if hasattr(entry, 'url_patterns'):
                d[entry.regex.pattern] = self.collect_urls(entry.url_patterns)
        return d

    def concatenate_ancestors(self, tree, prefix=''):
        d = {}
        for key, children in tree.items():
            new_prefix = prefix + key
            if children is None:
                d[new_prefix] = None
            else:
                d[new_prefix] = self.concatenate_ancestors(children, prefix=new_prefix)
        return d

    def print_keys(self, tree):
        for key, value in tree.items():
            print key
            if value is not None:
                self.print_keys(value)
