"""
Wrapper class that takes a list of template loaders as an argument and attempts
to load templates from them in order, caching the result.
"""
from django.template.loaders.cached import Loader as DjangoLoader

class Loader(DjangoLoader):
    """
    Cached loader that works well with debug toolbar
    """

    def load_template_source(self, template_name, template_dirs=None):
        pass

    def __init__(self, loaders=None):
        super(Loader, self).__init__(loaders)
        if not loaders:
            loaders = []
        self.template_cache = {}
        self._loaders = loaders
        self._cached_loaders = []

