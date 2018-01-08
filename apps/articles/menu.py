# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

from .models import ArticleType

class NewsMenu(CMSAttachMenu):
    name = _("News Menu")

    def get_nodes(self, request):
        article_type = ArticleType.objects.get(slug="news")
        nodes = []
        for at in article_type.get_children():
            nodes.append(NavigationNode(at.title, reverse("article_archive_for_news_by_type", kwargs={'type_sysname': at.slug}), at.id))
        return nodes

menu_pool.register_menu(NewsMenu)


class InterviewsMenu(CMSAttachMenu):
    name = _("Interviews Menu")

    def get_nodes(self, request):
        article_type = ArticleType.objects.get(slug="interviews")
        nodes = [
            NavigationNode(_("Overview"), reverse("magazine_overview"), 0)
        ]
        for at in article_type.get_children():
            nodes.append(NavigationNode(at.title, reverse("article_archive_for_interviews_by_type", kwargs={'type_sysname': at.slug}), at.id))
        nodes.append(NavigationNode(_("From the Blogs"), reverse("magazine_blog_posts"), 'magazine_blog_posts'))
        return nodes

menu_pool.register_menu(InterviewsMenu)


