# -*- coding: UTF-8 -*-
from django.db.models.loading import load_app
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.conf import settings

from jetson.apps.tracker.forms import TicketForm


@never_cache
def create_ticket(
    request,
    concern=None,
    content_type_id=None,
    object_id=None,
    template_name='tracker/createticket.html',
    template_done_name='tracker/postticket.html',
):
    """
    Displays the trouble ticket form and handles the associated action
    """
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')

    if request.method == 'POST':

        data = request.POST.copy()
        data.update(request.FILES)
        form = TicketForm(
            concern=concern,
            content_type_id=content_type_id,
            object_id=object_id,
            url=redirect_to,
            data=data
        )

        if form.is_valid():
            form.save()
            return render_to_response(
                template_done_name, {
                    settings.REDIRECT_FIELD_NAME: redirect_to,
                },
                context_instance=RequestContext(request)
            )
    else:
        form = TicketForm(
            concern=concern,
            content_type_id=content_type_id,
            object_id=object_id,
            url=redirect_to,
        )

    return render_to_response(
        template_name, {
            'form': form,
            settings.REDIRECT_FIELD_NAME: redirect_to,
        },
        context_instance=RequestContext(request)
    )
