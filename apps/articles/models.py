# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from jetson.apps.articles.base import *


class ArticleType(ArticleTypeBase):
    objects = TreeManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            ArticleType.objects.insert_node(self, self.parent)
        super(ArticleType, self).save(*args, **kwargs)


class Article(ArticleBase):
    pass
