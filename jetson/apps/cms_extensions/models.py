# -*- coding: utf-8 -*-
# calling the patch_settings() again as it didn't work correctly 
# previously from cms.conf for some reason (TODO: find the reason)
#from cms import conf
from django.conf import settings
from django.db.models import Q

#conf.ALREADY_PATCHED = False
#conf.patch_settings()

from cms.utils import page

def _is_valid_page_slug(page, parent, lang, slug, site):
    """Validates given slug depending on settings.
    """
    from cms.models import Title
    # Exclude the page with the publisher_state == page.PUBLISHER_STATE_DELETE
    qs = Title.objects.filter(page__site=site, slug=slug).exclude(
        Q(page=page) |
        Q(page=page.publisher_public) |
        Q(page__publisher_state=page.PUBLISHER_STATE_DELETE)
    )
    
    if ("cms.middleware.multilingual.MultilingualURLMiddleware" in settings.MIDDLEWARE_CLASSES or
        "jetson.apps.cms_extensions.middleware.MultilingualURLMiddleware" in settings.MIDDLEWARE_CLASSES):
        qs = qs.filter(language=lang)
    
    if not settings.CMS_FLAT_URLS:
        if parent and not parent.is_home(): 
            qs = qs.filter(page__parent=parent)
        else:
            qs = qs.filter(page__parent__isnull=True)

    if page.pk:
        qs = qs.exclude(language=lang, page=page)
    if qs.count():
        return False
    return True
    
page.is_valid_page_slug = _is_valid_page_slug
