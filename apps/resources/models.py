# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _

from jetson.apps.resources.base import *

from mptt.fields import TreeManyToManyField

### DOCUMENT MODIFICATION ###

class DocumentManagerExtended(DocumentManager):
    def featured_published(self):
        return self.latest_published().filter(is_featured=True).order_by("-creation_date")

class Document(DocumentBase):
    creative_sectors = TreeManyToManyField(
        Term,
        verbose_name=_("Creative sectors"),
        limit_choices_to={'vocabulary__sysname': 'categories_creativesectors'}, 
        related_name="creative_industry_documents",
        blank=True,
        )
    is_featured = models.BooleanField(_("Featured"), default=False)
    
    objects = DocumentManagerExtended()
    
    def get_creative_sectors(self):
        return self.creative_sectors.all()
        
    def is_addable_to_favorites(self, user=None):
        ContextItem = models.get_model("site_specific", "ContextItem")
        Favorite = models.get_model("favorites", "Favorite")
        user = get_current_user(user)
        return not Favorite.objects.is_favorite(
            ContextItem.objects.get_for(self),
            user,
            )

    def is_removable_from_favorites(self, user=None):
        ContextItem = models.get_model("site_specific", "ContextItem")
        Favorite = models.get_model("favorites", "Favorite")
        user = get_current_user(user)
        return Favorite.objects.is_favorite(
            ContextItem.objects.get_for(self),
            user,
            )
        
