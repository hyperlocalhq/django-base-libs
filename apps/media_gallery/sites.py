import time
import urllib2
from datetime import datetime
from functools import update_wrapper

import os
from django import forms
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.db import models
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.conf import settings
from base_libs.utils.misc import get_installed
from base_libs.views import access_denied
from base_libs.models.models import STATUS_CODE_PUBLISHED, STATUS_CODE_DRAFT
from jetson.apps.utils.views import direct_to_js_template

MediaGallery = models.get_model("media_gallery", "MediaGallery")
MediaFile = models.get_model("media_gallery", "MediaFile")
PortfolioSettings = models.get_model("media_gallery", "PortfolioSettings")
Section = models.get_model("media_gallery", "Section")
media_gallery_app = models.get_app("media_gallery")
URL_ID_PORTFOLIO = media_gallery_app.URL_ID_PORTFOLIO
TOKENIZATION_SUMMAND = media_gallery_app.TOKENIZATION_SUMMAND
VIDEO_SPLASH_URL = media_gallery_app.VIDEO_SPLASH_URL
VIDEO_SPLASH_TN_URL = media_gallery_app.VIDEO_SPLASH_TN_URL
AUDIO_SPLASH_URL = media_gallery_app.AUDIO_SPLASH_URL
AUDIO_SPLASH_TN_URL = media_gallery_app.AUDIO_SPLASH_TN_URL
ImageFileForm = get_installed("media_gallery.forms.ImageFileForm")
VideoFileForm = get_installed("media_gallery.forms.VideoFileForm")
AudioFileForm = get_installed("media_gallery.forms.AudioFileForm")
PortfolioSettingsForm = get_installed("media_gallery.forms.PortfolioSettingsForm")
SectionForm = get_installed("media_gallery.forms.SectionForm")
MediaGalleryForm = get_installed("media_gallery.forms.MediaGalleryForm")

image_mods = models.get_app("image_mods")

MEDIA_FILE_FORM_MAP = {
    'image': ImageFileForm,
    'audio': AudioFileForm,
    'video': VideoFileForm,
}


class PortfolioSite(object):
    """
    A PortfolioSite object encapsulates an instance of the media_gallery app,
    ready to be hooked in to your URLconf.

    The concept is based on django.contrib.admin.sites.AdminSite
    """

    template_name = "institutions/institution_portfolio_delete.html"

    def __init__(self, name=None, app_name='media_gallery', object_detail_dict=None):
        if not object_detail_dict:
            object_detail_dict = {}
        self.root_path = None
        self.object_detail_dict = object_detail_dict
        if name is None:
            self.name = 'portfolio'
        else:
            self.name = name
        self.app_name = app_name
        self.obj = None
        self.obj_ct = None
        self.obj_app_name = None
        self.obj_model_name = None
        self.published_gallery_list = ()
        self.all_gallery_list = ()
        self.extra_context = {}

    def check_object(self, **kwargs):
        self.obj = get_object_or_404(
            self.object_detail_dict['queryset'],
            **{self.object_detail_dict['slug_field']: kwargs['slug']}
        )
        if hasattr(self.obj, "content_object"):  # if the obj is ContextItem, then use its related object
            self.obj = self.obj.content_object
        self.obj_ct = ContentType.objects.get_for_model(self.obj)
        self.obj_app_name = type(self.obj)._meta.app_label
        self.obj_model_name = type(self.obj).__name__.lower()
        self.published_gallery_list = MediaGallery.published_objects.filter(
            content_type=self.obj_ct,
            object_id=self.obj.pk,
        ).order_by("section__sort_order", "sort_order")
        self.all_gallery_list = MediaGallery.objects.filter(
            content_type=self.obj_ct,
            object_id=self.obj.pk,
        ).order_by("section__sort_order", "sort_order")
        self.extra_context['object'] = self.obj
        self.extra_context['published_gallery_list'] = self.published_gallery_list
        self.extra_context['all_gallery_list'] = self.all_gallery_list
        self.extra_context['base_template'] = "%s/details_base.html" % self.obj_app_name

    def has_permission(self, request):
        """
        Returns True if the given HttpRequest has permission to manage
        portfolio
        """
        self.extra_context['can_manage_portfolio'] = request.user.has_perm(
            "%s.change_%s" % (self.obj_app_name, self.obj_model_name),
            self.obj,
        )
        return self.extra_context['can_manage_portfolio']

    def portfolio_view(self, view, cacheable=False, admin=False):
        """
        Decorator to create a portfolio view attached to this ``PortfolioSite``.
        This wraps the view and provides permission checking by calling
        ``self.has_permission`` for administrative views.

        You'll want to use this from within ``PortfolioSite.get_urls()``:

            class MyPortfolioSite(PortfolioSite):

                def get_urls(self):
                    from django.conf.urls import patterns, url

                    urls = super(MyPortfolioSite, self).get_urls()
                    urls += patterns('',
                        url(r'^my_view/$', self.portfolio_view(some_view))
                    )
                    return urls

        By default, portfolio_views are marked non-cacheable using the
        ``never_cache`` decorator. If the view can be safely cached, set
        cacheable=True.
        """

        def inner(request, *args, **kwargs):
            self.check_object(**kwargs)
            if not self.has_permission(request) and admin:
                return access_denied(request)
            return view(request, *args, **kwargs)

        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view, cacheable=False, admin=False):
            def wrapper(*args, **kwargs):
                self.extra_context['view_name'] = view.__name__
                return self.portfolio_view(view, cacheable, admin)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        # portfolio-wide views.
        urlpatterns = [
            url(
                r'^$',
                wrap(self.portfolio_overview),
            ),
            url(
                r'^settings/$',
                wrap(self.portfolio_settings, admin=True),
            ),
            url(
                r'^settings/delete-landing-page-image/$',
                wrap(self.delete_landing_page_image, admin=True),
            ),
            url(
                r'^manage/$',
                wrap(self.manage_galleries, admin=True),
            ),
            url(
                r'^section/add/$',
                wrap(self.create_update_section, admin=True),
            ),
            url(
                r'^section/(?P<section_token>\d+)/change/$',
                wrap(self.create_update_section, admin=True),
            ),
            url(
                r'^section/(?P<section_token>\d+)/delete/$',
                wrap(self.delete_section, admin=True),
            ),
            url(
                r'^album/add/$',
                wrap(self.create_update_gallery, admin=True),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/$',
                wrap(self.gallery_detail),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/change/$',
                wrap(self.create_update_gallery, admin=True),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/manage/$',
                wrap(self.manage_gallery, admin=True),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/delete/$',
                wrap(self.delete_gallery, admin=True),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/delete-cover/$',
                wrap(self.delete_gallery_cover, admin=True),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/add/((?P<media_file_type>[^/]+)/)?$',
                wrap(self.create_update_mediafile, admin=True),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/(?P<mediafile_token>\d+)/$',
                wrap(self.create_update_mediafile, admin=True),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/(?P<mediafile_token>\d+)/delete/$',
                wrap(self.delete_mediafile, admin=True),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/(?P<mediafile_token>\d+)/popup_delete/$',
                wrap(self.delete_mediafile_popup, admin=True),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/(?P<mediafile_token>\d+)/json/$',
                wrap(self.json_show_file),
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/comments/add/$',
                wrap(self.gallery_post_comment),
                {'user_ajax': False}
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/comments/add_ajax/$',
                wrap(self.gallery_post_comment),
                {'user_ajax': True}
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/comment/(?P<comment_id>\d+)/refuse/use-popup/$',
                wrap(self.gallery_refuse_comment),
                {
                    'use_popup': True,
                    'template_name': 'media_gallery/comments/popups/comment_refuse.html',
                }
            ),
            url(r'^album/(?P<gallery_token>\d+)/comment/(?P<comment_id>\d+)/refuse/$',
                wrap(self.gallery_refuse_comment), {
                    'use_popup': True,
                }
                ),
            url(
                r'^album/(?P<gallery_token>\d+)/comment/(?P<comment_id>\d+)/accept/use-popup/$',
                wrap(self.gallery_accept_comment),
                {
                    'use_popup': True,
                    'template_name': 'media_gallery/comments/popups/comment_accept.html',
                }
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/comment/(?P<comment_id>\d+)/accept/$',
                wrap(self.gallery_accept_comment), {
                    'use_popup': True,
                }
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/comment/(?P<comment_id>\d+)/mark_as_spam/use-popup/$',
                wrap(self.gallery_mark_comment_as_spam),
                {
                    'use_popup': True,
                    'template_name': 'media_gallery/comments/popups/comment_markasspam.html',
                }
            ),
            url(
                r'^album/(?P<gallery_token>\d+)/comment/(?P<comment_id>\d+)/mark_as_spam/$',
                wrap(self.gallery_mark_comment_as_spam), {
                    'use_popup': True,
                }
            ),
        ]

        return urlpatterns

    def urls(self):
        return self.get_urls(), self.app_name, self.name

    urls = property(urls)

    def token_to_pk(self, token):
        return int(token) - TOKENIZATION_SUMMAND

    '''
    def portfolio_overview(self, request, **kwargs):
        """
        A landing page for a portfolio of a person, institution or event.
        Depending on the landing_page value in PortfolioSettings for the object,
        this page does one of the following:
        * redirects to the first gallery / album
        * shows the list of galleries / albums
        * shows a custom image
        If there are still no public galleries, it shows a message
        that the portfolio is empty for non-owner of the object
        or guide the owner to the portfolio settings and sections list.
        """

        p_settings = PortfolioSettings.objects.get_for_object(self.obj)

        if self.published_gallery_list:
            if p_settings.landing_page == "first_album":
                return redirect("%(obj_url_path)s%(URL_ID_PORTFOLIO)s/album/%(gallery_token)s/" % {
                    'obj_url_path': self.obj.get_url_path(),
                    'URL_ID_PORTFOLIO': URL_ID_PORTFOLIO,
                    'gallery_token':self.published_gallery_list[0].get_token(),
                    })

        context_dict = {
            'portfolio_settings': p_settings,
            }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/portfolio_overview.html",
            context_dict,
            context_instance=RequestContext(request),
            )
    '''

    def portfolio_overview(self, request, **kwargs):
        """
        A landing page for a portfolio of a person, institution or event.

        * redirects to the first gallery / album if there is just one published gallery
        * shows the list of galleries / albums otherwise

        If there are still no public galleries, it shows a message
        that the portfolio is empty for non-owner of the object
        or guide the owner to the portfolio settings and sections list.
        """
        has_permission_to_edit = self.has_permission(request)
        p_settings = PortfolioSettings.objects.get_for_object(self.obj)

        if self.published_gallery_list and not has_permission_to_edit:
            if self.published_gallery_list.count() == 1:
                return redirect("%(obj_url_path)s%(URL_ID_PORTFOLIO)s/album/%(gallery_token)s/" % {
                    'obj_url_path': self.obj.get_url_path(),
                    'URL_ID_PORTFOLIO': URL_ID_PORTFOLIO,
                    'gallery_token': self.published_gallery_list[0].get_token(),
                })

        context_dict = {
            'portfolio_settings': p_settings,
        }
        context_dict.update(self.extra_context)
        if has_permission_to_edit:
            context_dict['gallery_list'] = self.all_gallery_list
        else:
            context_dict['gallery_list'] = self.published_gallery_list

        return render_to_response(
            "media_gallery/portfolio_overview.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def portfolio_settings(self, request, **kwargs):
        """
        Portfolio-settings page where an owner of an object can define
        the options for the landing page
        """
        p_settings = PortfolioSettings.objects.get_for_object(self.obj)

        if request.method == "POST":
            form = PortfolioSettingsForm(request.POST, request.FILES)
            if form.is_valid():
                cleaned = form.cleaned_data

                p_settings.landing_page = cleaned['landing_page']

                if cleaned.get("landing_page_image", None):
                    if p_settings.landing_page_image:
                        try:
                            image_mods.FileManager.delete_file(p_settings.landing_page_image.path)
                        except OSError:
                            pass

                    rel_dir = getattr(self.obj, "get_filebrowser_dir", lambda: "")()
                    rel_dir += URL_ID_PORTFOLIO + "/"
                    fname, fext = os.path.splitext(cleaned['landing_page_image'].name)
                    filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                    path = "".join((rel_dir, filename))
                    image_mods.FileManager.save_file(
                        path=path,
                        content=cleaned['landing_page_image'],
                    )

                    p_settings.landing_page_image = path
                p_settings.save()
                redirect_to = "%s%s/settings/" % (
                    self.obj.get_url_path(),
                    URL_ID_PORTFOLIO,
                )
                return redirect(redirect_to)
        else:
            initial = {
                'landing_page': p_settings.landing_page,
            }
            form = PortfolioSettingsForm(initial=initial)

        context_dict = {
            'form': form,
            'portfolio_settings': p_settings,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/portfolio_settings.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def delete_landing_page_image(self, request, **kwargs):
        """
        A page to delete a landing-page image
        """
        p_settings = PortfolioSettings.objects.get_for_object(self.obj)

        if request.method == "POST":
            form = forms.Form(request.POST)
            if form.is_valid():
                if p_settings.landing_page_image:
                    try:
                        image_mods.FileManager.delete_file(p_settings.landing_page_image.path)
                    except OSError:
                        pass
                p_settings.landing_page_image = ""
                p_settings.save()
                redirect_to = "%s%s/settings/" % (
                    self.obj.get_url_path(),
                    URL_ID_PORTFOLIO,
                )
                return redirect(redirect_to)

        context_dict = {
            'portfolio_settings': p_settings,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/delete_landing_page_image.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def update_gallery_parenting_and_ordering(self, tokens):
        # tokens is in this format:
        # "<section1_token>:<gallery1_token>,<gallery2_token>|<section2_token>:<gallery3_token>"
        sections = []
        for sections_str in tokens.split(u"|"):
            section_token, galleries_str = sections_str.split(u":")
            section = get_object_or_404(
                Section,
                content_type=self.obj_ct,
                object_id=self.obj.pk,
                pk=self.token_to_pk(section_token)
            )
            galleries = []
            if galleries_str:
                for gallery_token in galleries_str.split(u","):
                    gallery = get_object_or_404(
                        MediaGallery,
                        content_type=self.obj_ct,
                        object_id=self.obj.pk,
                        pk=self.token_to_pk(gallery_token)
                    )
                    galleries.append(gallery)
            sections.append((section, galleries))
        section_sort_order = 0
        for section, galleries in sections:
            section.sort_order = section_sort_order
            section.save()
            section_sort_order += 1

            gallery_sort_order = 0
            for gallery in galleries:
                gallery.section = section
                gallery.sort_order = gallery_sort_order
                gallery.save()
                gallery_sort_order += 1

    def manage_galleries(self, request, **kwargs):
        """
        A page where the owner of the portfolio can sort sections and galleries
        and move galleries from one section to the other
        """
        show = request.GET.get("show", "all")
        if show not in ("published", "unpublished", "all"):
            raise Http404

        unsectioned_gallery_list = MediaGallery.objects.filter(
            content_type=self.obj_ct,
            object_id=self.obj.pk,
            section=None,
        )
        if unsectioned_gallery_list:
            sections = Section.objects.filter(
                content_type=self.obj_ct,
                object_id=self.obj.pk,
            )
            if sections:
                section = sections[0]
            else:
                section = Section()
                section.content_object = self.obj
                section.save()
            for g in unsectioned_gallery_list:
                g.section = section
                g.save()

        if "parenting_and_ordering" in request.POST and request.is_ajax():
            tokens = request.POST['parenting_and_ordering']
            self.update_gallery_parenting_and_ordering(tokens)
            return HttpResponse("OK")

        sections = Section.objects.filter(
            content_type=self.obj_ct,
            object_id=self.obj.pk,
        ).order_by("sort_order")

        section_list = []
        for section in sections:
            if show == "published":
                galleries = section.mediagallery_set.filter(
                    status=STATUS_CODE_PUBLISHED,
                )
            elif show == "unpublished":
                galleries = section.mediagallery_set.filter(
                    status=STATUS_CODE_DRAFT,
                )
            else:
                galleries = section.mediagallery_set.all()
            section_list.append((section, galleries))

        context_dict = {
            'section_list': section_list,
            'show': show,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/manage_galleries.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def create_update_section(self, request, section_token=None, **kwargs):
        """
        A page to create or change the settings of a section
        """
        if section_token:
            section = get_object_or_404(
                Section,
                content_type=self.obj_ct,
                object_id=self.obj.id,
                pk=self.token_to_pk(section_token),
            )
        else:
            section = Section()
            section.content_object = self.obj

        if request.method == "POST":
            form = SectionForm(request.POST, request.FILES)
            if form.is_valid():
                cleaned = form.cleaned_data
                section.title_en = cleaned['title_en']
                section.title_de = cleaned['title_de']
                section.show_title = cleaned['show_title']
                if not section.pk:
                    section.sort_order = Section.objects.filter(
                        content_type=self.obj_ct,
                        object_id=self.obj.id,
                    ).count()
                else:
                    # trick not to reorder sections on save
                    section.sort_order = section.sort_order
                section.save()
                redirect_to = "%s%s/manage/" % (
                    self.obj.get_url_path(),
                    URL_ID_PORTFOLIO,
                )
                return redirect(redirect_to)
        else:
            initial = {
                'title_en': section.title_en,
                'title_de': section.title_de,
                'show_title': section.show_title,
            }
            form = SectionForm(initial=initial)

        context_dict = {
            'form': form,
            'section': section,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/create_update_section.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def delete_section(self, request, section_token, **kwargs):
        """
        A page to delete a section
        """
        section = get_object_or_404(
            Section,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(section_token),
        )

        if request.method == "POST":
            form = forms.Form(request.POST)
            if form.is_valid():
                for gallery in section.mediagallery_set.all():
                    for mediafile in gallery.mediafile_set.all():
                        if mediafile.path:
                            try:
                                image_mods.FileManager.delete_file(mediafile.path.path)
                            except OSError:
                                pass
                        if mediafile.splash_image_path:
                            try:
                                image_mods.FileManager.delete_file(mediafile.splash_image_path.path)
                            except OSError:
                                pass
                        mediafile.delete()
                    gallery.delete()
                section.delete()
                redirect_to = "%s%s/manage/" % (
                    self.obj.get_url_path(),
                    URL_ID_PORTFOLIO,
                )
                return redirect(redirect_to)

        context_dict = {
            'section': section,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/delete_section.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def create_update_gallery(self, request, gallery_token=None, **kwargs):
        """
        A page to create or change a gallery settings
        """
        if gallery_token:
            gallery = get_object_or_404(
                MediaGallery,
                content_type=self.obj_ct,
                object_id=self.obj.id,
                pk=self.token_to_pk(gallery_token),
            )
        else:
            gallery = MediaGallery()
            gallery.content_object = self.obj

        if request.method == "POST":
            form = MediaGalleryForm(gallery, request.POST, request.FILES)
            if form.is_valid():
                cleaned = form.cleaned_data
                gallery.title_en = cleaned['title_en']
                gallery.title_de = cleaned['title_de']
                gallery.description_en = cleaned['description_en']
                gallery.description_de = cleaned['description_de']
                gallery.status = [0, 1][cleaned['published']]
                gallery.photo_author = cleaned['photo_author']
                if not gallery.section:
                    if 'section' in request.REQUEST:
                        section = get_object_or_404(
                            Section,
                            content_type=self.obj_ct,
                            object_id=self.obj.id,
                            pk=self.token_to_pk(request.REQUEST['section']),
                        )
                    else:
                        sections = Section.objects.filter(
                            content_type=self.obj_ct,
                            object_id=self.obj.id,
                        )
                        if sections:
                            section = sections[0]
                        else:
                            section = Section()
                            section.content_object = self.obj
                            section.save()

                    gallery.section = section

                if cleaned.get("cover_image", None):
                    if gallery.cover_image:
                        try:
                            image_mods.FileManager.delete_file(gallery.cover_image.path)
                        except OSError:
                            pass

                    rel_dir = getattr(self.obj, "get_filebrowser_dir", lambda: "")()
                    rel_dir += URL_ID_PORTFOLIO + "/"
                    fname, fext = os.path.splitext(cleaned['cover_image'].name)
                    filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                    path = "".join((rel_dir, filename))
                    image_mods.FileManager.save_file(
                        path=path,
                        content=cleaned['cover_image'],
                    )
                    gallery.cover_image = path
                section = None
                if not gallery.pk:
                    gallery.sort_order = MediaGallery.objects.filter(
                        content_type=self.obj_ct,
                        object_id=self.obj.id,
                        section=section,
                    ).count()
                else:
                    # trick not to reorder galleries on save
                    gallery.sort_order = gallery.sort_order
                gallery.save()
                gallery.categories.clear()
                for cat in cleaned['categories']:
                    gallery.categories.add(cat)

                redirect_to = "%smanage/" % (
                    gallery.get_url_path(),
                )
                return redirect(redirect_to)
        else:
            initial = {
                'title_en': gallery.title_en,
                'title_de': gallery.title_de,
                'description_en': gallery.description_en,
                'description_de': gallery.description_de,
                'published': gallery.status == 1,
                'photo_author': gallery.photo_author,
            }
            if gallery.pk:
                initial['categories'] = gallery.categories.all()
            form = MediaGalleryForm(gallery, initial=initial)

        context_dict = {
            'form': form,
            'gallery': gallery,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/create_update_gallery.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def update_mediafile_ordering(self, tokens, gallery):
        # tokens is in this format:
        # "<mediafile1_token>,<mediafile2_token>,<mediafile3_token>"
        mediafiles = []
        for mediafile_token in tokens.split(u","):
            mediafile = get_object_or_404(
                MediaFile,
                gallery=gallery,
                pk=self.token_to_pk(mediafile_token)
            )
            mediafiles.append(mediafile)
        sort_order = 0
        for mediafile in mediafiles:
            mediafile.sort_order = sort_order
            mediafile.save()
            sort_order += 1

    def manage_gallery(self, request, gallery_token, **kwargs):
        """
        A page to create or change a gallery settings
        """
        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        if "ordering" in request.POST and request.is_ajax():
            tokens = request.POST['ordering']
            self.update_mediafile_ordering(tokens, gallery)
            return HttpResponse("OK")

        context_dict = {
            'gallery': gallery,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/manage_gallery.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def delete_gallery(self, request, gallery_token, **kwargs):
        """
        A page to delete a gallery
        """
        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        if request.method == "POST":
            form = forms.Form(request.POST)
            if form.is_valid():
                for mediafile in gallery.mediafile_set.all():
                    if mediafile.path:
                        try:
                            image_mods.FileManager.delete_file(mediafile.path.path)
                        except OSError:
                            pass
                    if mediafile.splash_image_path:
                        try:
                            image_mods.FileManager.delete_file(mediafile.splash_image_path.path)
                        except OSError:
                            pass
                    mediafile.delete()
                gallery.delete()
                redirect_to = "%s%s/manage/" % (
                    self.obj.get_url_path(),
                    URL_ID_PORTFOLIO,
                )
                return redirect(redirect_to)

        context_dict = {
            'gallery': gallery,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/delete_gallery.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def delete_gallery_cover(self, request, gallery_token, **kwargs):
        """
        A page to delete a gallery cover
        """
        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        if request.method == "POST":
            form = forms.Form(request.POST)
            if form.is_valid():
                if gallery.cover_image:
                    try:
                        image_mods.FileManager.delete_file(gallery.cover_image.path)
                    except OSError:
                        pass
                gallery.cover_image = ""
                gallery.save()
                redirect_to = "%s%s/album/%s/change/" % (
                    self.obj.get_url_path(),
                    URL_ID_PORTFOLIO,
                    gallery.get_token(),
                )
                return redirect(redirect_to)

        context_dict = {
            'gallery': gallery,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/delete_gallery_cover.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def gallery_detail(self, request, gallery_token, **kwargs):
        """
        shows gallery description, list of media files, and comments
        """
        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        list_of_files = gallery.mediafile_set.order_by("sort_order")

        if gallery:
            gallery.increase_views()

        context_dict = {
            'gallery': gallery,
            'list_of_files': list_of_files,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/gallery_detail/gallery_listed.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    gallery_detail = never_cache(gallery_detail)

    def create_update_mediafile(self, request, gallery_token, mediafile_token="", media_file_type="", **kwargs):

        media_file_type = media_file_type or "image"
        if media_file_type not in ("image", "video", "audio"):
            raise Http404

        if not "extra_context" in kwargs:
            kwargs["extra_context"] = {}

        rel_dir = getattr(self.obj, "get_filebrowser_dir", lambda: "")()
        rel_dir += URL_ID_PORTFOLIO + "/"

        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        filters = {}
        if mediafile_token:
            media_file_obj = get_object_or_404(
                MediaFile,
                gallery=gallery,
                pk=self.token_to_pk(mediafile_token),
            )
        else:
            media_file_obj = None

        if media_file_obj:
            if media_file_obj.file_type == "i":
                media_file_type = "image"
            elif media_file_obj.file_type == "a":
                media_file_type = "audio"
            elif media_file_obj.file_type in ("v", "y"):
                media_file_type = "video"

        form_class = MEDIA_FILE_FORM_MAP[media_file_type]

        if request.method == "POST":
            # just after submitting data
            form = form_class(request.POST, request.FILES)
            # Passing request.FILES to the form always breaks the form validation
            # WHY!?? As a workaround, let's validate just the POST and then
            # manage FILES separately.
            if not media_file_obj and ("media_file" not in request.FILES) and not request.POST.get("external_url", ""):
                # new media file - media file required
                form.fields['media_file'].required = True
                form.fields['external_url'].required = True
            if form.is_valid():
                cleaned = form.cleaned_data
                file_obj = None
                splash_image_obj = None
                path = ""
                if media_file_obj and media_file_obj.path:
                    path = media_file_obj.path.path
                if cleaned.get("media_file", None) or cleaned.get("external_url"):
                    if path:
                        # delete the old file
                        try:
                            image_mods.FileManager.delete_file(path)
                        except OSError:
                            pass
                        path = ""
                media_file_path = ""
                if cleaned.get("media_file", None):
                    fname, fext = os.path.splitext(cleaned['media_file'].name)
                    filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                    path = "".join((rel_dir, filename))
                    image_mods.FileManager.save_file(
                        path=path,
                        content=cleaned['media_file'],
                    )
                    media_file_path = path

                splash_image_file_path = ""
                if cleaned.get("splash_image_file", None):
                    if media_file_obj and media_file_obj.splash_image_path:
                        # delete the old file
                        try:
                            image_mods.FileManager.delete_file(media_file_obj.splash_image_path.path)
                        except OSError:
                            pass
                    time.sleep(1)  # ensure that the filenames differ
                    filename = datetime.now().strftime("%Y%m%d%H%M%S.jpg")
                    path = "".join((rel_dir, filename))
                    image_mods.FileManager.save_file(
                        path=path,
                        content=cleaned['splash_image_file'],
                    )
                    splash_image_file_path = path

                if not media_file_obj:
                    media_file_obj = MediaFile(
                        gallery=gallery
                    )
                media_file_obj.title_en = cleaned['title_en']
                media_file_obj.title_de = cleaned['title_de']
                media_file_obj.description_en = cleaned['description_en']
                media_file_obj.description_de = cleaned['description_de']

                image_url = cleaned['external_url']
                if image_url and media_file_type == "image":
                    rel_dir = getattr(self.obj, "get_filebrowser_dir", lambda: "")()
                    rel_dir += URL_ID_PORTFOLIO + "/"
                    fname, fext = os.path.splitext(image_url)
                    filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                    path = "".join((rel_dir, filename))
                    image_data = urllib2.urlopen(image_url)
                    image_mods.FileManager.save_file(
                        path=path,
                        content=image_data.read(),
                    )
                    media_file_obj.path = path
                else:
                    media_file_obj.external_url = image_url

                if media_file_path:  # update media_file path
                    media_file_obj.path = media_file_path
                if splash_image_file_path:  # update media_file splash image path
                    media_file_obj.splash_image_path = splash_image_file_path
                if not media_file_obj.pk:
                    media_file_obj.sort_order = MediaFile.objects.filter(
                        gallery=gallery,
                    ).count()
                else:
                    # trick not to reorder media files on save
                    media_file_obj.sort_order = media_file_obj.sort_order
                media_file_obj.save()

                if "save_continue" in request.POST:
                    redirect_to = "%s%s/album/%s/%s/" % (
                        self.obj.get_url_path(),
                        URL_ID_PORTFOLIO,
                        gallery.get_token(),
                        media_file_obj.get_token(),
                    )
                elif "save_add" in request.POST:
                    redirect_to = "%s%s/album/%s/add/%s/" % (
                        self.obj.get_url_path(),
                        URL_ID_PORTFOLIO,
                        gallery.get_token(),
                        media_file_type,
                    )
                else:
                    redirect_to = "%s%s/album/%s/manage/" % (
                        self.obj.get_url_path(),
                        URL_ID_PORTFOLIO,
                        gallery.get_token(),
                    )
                return HttpResponseRedirect(redirect_to)
        else:
            if media_file_obj:
                # existing media file
                form = form_class(initial=media_file_obj.__dict__)
            else:
                # new media file
                form = form_class()
                form.fields['media_file'].required = True

        context_dict = {
            'media_file': media_file_obj,
            'media_file_type': media_file_type,
            'form': form,
            'gallery': gallery,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/create_update_mediafile.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    create_update_mediafile = never_cache(create_update_mediafile)

    def delete_mediafile(self, request, gallery_token, mediafile_token="", **kwargs):

        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        filters = {
            'id': self.token_to_pk(mediafile_token),
        }
        if gallery:
            filters['gallery'] = gallery
        try:
            media_file_obj = MediaFile.objects.get(**filters)
        except Exception:
            raise Http404

        if "POST" == request.method:
            if media_file_obj:
                if media_file_obj.path:
                    try:
                        image_mods.FileManager.delete_file(media_file_obj.path.path)
                    except OSError:
                        pass
                if media_file_obj.splash_image_path:
                    try:
                        image_mods.FileManager.delete_file(media_file_obj.splash_image_path.path)
                    except OSError:
                        pass
                media_file_obj.delete()

            redirect_to = "%s%s/album/%s/manage/" % (
                self.obj.get_url_path(),
                URL_ID_PORTFOLIO,
                gallery.get_token(),
            )
            return HttpResponseRedirect(redirect_to)

        context_dict = {
            'media_file': media_file_obj,
        }
        context_dict.update(self.extra_context)

        return render_to_response(
            "media_gallery/delete_mediafile.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    def delete_mediafile_popup(self, request, gallery_token, mediafile_token="", **kwargs):
        response = self.delete_mediafile(request, gallery_token, mediafile_token, **kwargs)
        if isinstance(response, HttpResponseRedirect):
            response = HttpResponse("reload")
        return response

    def json_show_file(self, request, gallery_token, mediafile_token, **kwargs):
        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        filters = {
            'pk': self.token_to_pk(mediafile_token),
        }
        if gallery:
            filters['gallery'] = gallery
        try:
            media_file_obj = MediaFile.objects.get(**filters)
        except Exception:
            media_file_obj = None

        kwargs.pop('slug')
        kwargs['dictionary'] = {
            'media_file': media_file_obj,
        }
        kwargs['template_name'] = "media_gallery/includes/media_file.js"
        return direct_to_js_template(request, cache=False, **kwargs)

    ### COMMENTS ###

    def gallery_post_comment(self,
                             request,
                             gallery_token,
                             template_name=None,
                             extra_context=None, use_ajax=False, **kwargs):
        """
        handles posting a comment
        """
        use_ajax = request.is_ajax()

        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        if extra_context is None:
            extra_context = {}

        extra_context[settings.REDIRECT_FIELD_NAME] = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
        extra_context['gallery'] = gallery
        extra_context['object'] = self.obj

        if template_name is None:
            template_name = 'media_gallery/comments/form.html'

        redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')

        if request.method == 'POST':
            from jetson.apps.comments.views.comments import post_comment

            if request.POST.has_key('post'):

                post_comment(request, template_name=template_name, use_ajax=use_ajax)
                if not use_ajax:
                    redirect_to += "#comments"
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponse("reload")

            # the normal preview is done ...
            elif request.POST.has_key('preview'):
                return post_comment(request, template_name=template_name, use_ajax=use_ajax,
                                    extra_context=extra_context)

            # cancel
            else:
                if not use_ajax:
                    redirect_to += "#comments"
                    return HttpResponseRedirect(redirect_to)

        from django.template import Template

        extra_context['gallery'] = gallery
        t = Template("""
            {% load comments %}
            {% comment_form using "media_gallery/comments/form.html" for media_gallery.mediagallery gallery.id %}
            """)
        c = RequestContext(request, extra_context)
        return HttpResponse(t.render(c))

    gallery_post_comment = never_cache(gallery_post_comment)

    def gallery_refuse_comment(self,
                               request,
                               gallery_token,
                               comment_id,
                               template_name=None,
                               extra_context=None, use_popup=False, **kwargs):

        """
        Displays the delete comment form and handles the associated action
        """
        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
        if redirect_to == '':
            redirect_to = request.path.split('comment')[0]

        if extra_context is None:
            extra_context = {}
        extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
        extra_context['gallery'] = gallery
        extra_context.update(self.extra_context)

        if template_name is None:
            template_name = 'media_gallery/comments/refuse.html'

        from jetson.apps.comments.views.comments import refuse_comment

        response = refuse_comment(request, comment_id, template_name, redirect_to, extra_context, use_popup)
        if response.content == "reload" and not request.is_ajax():
            redirect_to = "%s%s/album/%s/" % (
                self.obj.get_url_path(),
                URL_ID_PORTFOLIO,
                gallery.get_token(),
            )
            return HttpResponseRedirect(redirect_to)
        return response

    def gallery_accept_comment(
            self,
            request,
            gallery_token,
            comment_id,
            template_name=None,
            extra_context=None, use_popup=False, **kwargs
    ):

        """
        Displays the accept comment form and handles the associated action
        """
        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
        if redirect_to == '':
            redirect_to = request.path.split('comment')[0]

        if extra_context is None:
            extra_context = {}
        extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
        extra_context['gallery'] = gallery
        extra_context.update(self.extra_context)

        if template_name is None:
            template_name = 'media_gallery/comments/accept.html'

        from jetson.apps.comments.views.comments import accept_comment

        response = accept_comment(request, comment_id, template_name, redirect_to, extra_context, use_popup)
        if response.content == "reload" and not request.is_ajax():
            redirect_to = "%s%s/album/%s/" % (
                self.obj.get_url_path(),
                URL_ID_PORTFOLIO,
                gallery.get_token(),
            )
            return HttpResponseRedirect(redirect_to)
        return response

    def gallery_mark_comment_as_spam(
            self,
            request,
            gallery_token,
            comment_id,
            template_name=None,
            extra_context=None, use_popup=False, **kwargs
    ):

        """
        Displays the "mark as spam" comment form and handles the associated action
        """
        gallery = get_object_or_404(
            MediaGallery,
            content_type=self.obj_ct,
            object_id=self.obj.id,
            pk=self.token_to_pk(gallery_token),
        )

        redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
        if redirect_to == '':
            redirect_to = request.path.split('comment')[0]

        if extra_context is None:
            extra_context = {}
        extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
        extra_context['gallery'] = gallery
        extra_context.update(self.extra_context)

        if template_name is None:
            template_name = 'media_gallery/comments/markasspam.html'

        from jetson.apps.comments.views.comments import mark_as_spam_comment

        response = mark_as_spam_comment(request, comment_id, template_name, redirect_to, extra_context, use_popup)
        if response.content == "reload" and not request.is_ajax():
            redirect_to = "%s%s/album/%s/" % (
                self.obj.get_url_path(),
                URL_ID_PORTFOLIO,
                gallery.get_token(),
            )
            return HttpResponseRedirect(redirect_to)
        return response
