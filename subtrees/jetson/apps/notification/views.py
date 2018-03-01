# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.syndication.views import Feed
from django import forms
from django.utils.translation import ugettext_lazy as _

from jetson.apps.notification.models import *
from jetson.apps.notification.tasks import get_notification_setting
from jetson.apps.notification.decorators import basic_auth_required, simple_basic_auth_callback
from jetson.apps.notification.feeds import NoticeUserFeed

from .forms import NoticeSettingsForm


@basic_auth_required(realm='Notices Feed', callback_func=simple_basic_auth_callback)
def feed_for_user(request):
    url = "feed/%s" % request.user.username
    feed_instance = Feed()
    feed = feed_instance(request, url, {
        "feed": NoticeUserFeed(),
    })
    return feed


@login_required
@never_cache
def notices(request):
    notice_types = NoticeType.objects.all()
    notices = Notice.objects.notices_for(request.user)
    settings_table = []
    for notice_type in NoticeType.objects.all():
        settings_row = []
        for medium_id, medium_display in NOTICE_MEDIA:
            form_sysname = "%s_%s" % (notice_type.sysname, medium_id)
            setting = get_notification_setting(request.user, notice_type, medium_id)
            settings_row.append((form_sysname, setting.frequency))
        settings_table.append({"notice_type": notice_type, "cells": settings_row})

    notice_settings = {
        "column_headers": [medium_display for medium_id, medium_display in NOTICE_MEDIA],
        "rows": settings_table,
    }

    return render_to_response("notification/notices.html", {
        "notices": notices,
        "notice_types": notice_types,
        "notice_settings": notice_settings,
    }, context_instance=RequestContext(request))


class NoticeSettingForm(forms.Form):
    frequency = forms.ChoiceField(
        label=_("How often should the email be sent?"),
        choices=NOTICE_FREQUENCY,
    )


@login_required
@never_cache
def notification_settings(request):
    notice_types = NoticeType.objects.all()
    notices = Notice.objects.notices_for(request.user)
    settings_table = []

    if request.user.is_staff:
        queryset = NoticeType.objects.all()
    else:
        queryset = NoticeType.objects.filter(is_public=True)
    for notice_type in queryset:
        settings_row = []
        for medium_id, medium_display in NOTICE_MEDIA:
            form_sysname = "%s_%s" % (notice_type.sysname, medium_id)
            setting = get_notification_setting(request.user, notice_type, medium_id)
            if request.method == "POST":
                form = NoticeSettingForm(
                    prefix=form_sysname,
                    data=request.POST,
                )
                if form.is_valid():
                    setting.frequency = form.cleaned_data['frequency']
                setting.save()
            else:
                form = NoticeSettingForm(
                    prefix=form_sysname,
                    initial={'frequency': setting.frequency},
                )
            settings_row.append((form_sysname, form))
        settings_table.append({
            "category": notice_type.category,
            "notice_type": notice_type,
            "cells": settings_row,
        })

    notice_settings = {
        "column_headers": [medium_display for medium_id, medium_display in NOTICE_MEDIA],
        "rows": settings_table,
    }

    if request.method == "POST":
        form = NoticeSettingsForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(".")
    else:
        form = NoticeSettingsForm(request.user)

    return render_to_response("notification/settings.html", {
        "form": form,
        "notices": notices,
        "notice_types": notice_types,
        "notice_settings": notice_settings,
    }, context_instance=RequestContext(request))


@login_required
def single(request, id):
    notice = get_object_or_404(Notice, id=id)
    if request.user == notice.user:
        return render_to_response("notification/single.html", {
            "notice": notice,
        }, context_instance=RequestContext(request))
    raise Http404


@login_required
def archive(request, noticeid=None, next_page=None):
    if noticeid:
        try:
            notice = Notice.objects.get(id=noticeid)
            if request.user == notice.user or request.user.is_superuser:
                notice.archive()
            else:  # you can archive other users' notices
                # only if you are superuser.
                return HttpResponseRedirect(next_page)
        except Notice.DoesNotExist:
            return HttpResponseRedirect(next_page)
    return HttpResponseRedirect(next_page)


@login_required
def delete(request, noticeid=None, next_page=None):
    if noticeid:
        try:
            notice = Notice.objects.get(id=noticeid)
            if request.user == notice.user or request.user.is_superuser:
                notice.delete()
            else:  # you can delete other users' notices
                # only if you are superuser.
                return HttpResponseRedirect(next_page)
        except Notice.DoesNotExist:
            return HttpResponseRedirect(next_page)
    return HttpResponseRedirect(next_page)


@login_required
def mark_all_seen(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    for notice in Notice.objects.notices_for(request.user, unseen=True):
        notice.unseen = False
        notice.save()
    return HttpResponseRedirect(reverse("notification_notices"))
