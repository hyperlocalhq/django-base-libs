from base_libs.admin.options import ExtendedModelAdmin, ExtendedStackedInline
try:
    from base_libs.admin.filters import HierarchyRelatedFilterSpec
except:
    # fallback for Django 1.3
    pass
