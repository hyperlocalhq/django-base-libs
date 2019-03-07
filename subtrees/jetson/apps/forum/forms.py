# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.fields import BLANK_CHOICE_DASH

from base_libs.widgets import TreeSelectWidget
from base_libs.forms import dynamicforms

from jetson.apps.forum.models import Forum, ForumThread
from base_libs.utils.misc import smart_truncate


class ForumOptionsForm(dynamicforms.Form):
    """
    Form for Forum Options
    """
    title = forms.CharField(
        label=_("Title"),
        required=True,
        help_text=_("Specify the 'global' title for all forums here."),
    )

    allow_bumping = forms.BooleanField(
        label=_("Allow bumping"),
        required=False,
        help_text=_("Check, if you want to allow bumping in your forums."),
    )

    # currently disabled
    """
    max_level = forms.ChoiceField(
        label= _("Max level for nested forums"),
        required=True,
        help_text= _("If you do not want any nested forums, just set the max level to '1'. If you want to allow only one (default) forum, set the max level to '0'."),
        choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], 
        widget=forms.Select(attrs={'disabled': 'disabled'}),    
        )
    """

    def __init__(self, *args, **kwargs):
        self.container = kwargs.get('container', None)
        if self.container:
            kwargs.pop(
                'container'
            )  #we must not pass extra kwargs to the super constructor!!!
        #TODO!!!!!
        #    self.container.get_forum_depth()
        #    # you must not reduce max_level (if there are already existing nested forums!!!)
        #    self.fields["max_level"].choices =

        super(ForumOptionsForm, self).__init__(*args, **kwargs)


class ForumForm(dynamicforms.Form):
    """
    Form for forums
    """
    title = forms.CharField(
        label=_("Title"),
        required=True,
        max_length=512,
    )

    short_title = forms.CharField(
        label=_("Short Title"),
        required=False,
        max_length=32,
        help_text=_(
            "a short title to be displayed in page breadcrumbs and headline. If left blank, short title is derived from title."
        ),
    )

    description = forms.CharField(
        label=_("Description"),
        required=False,
        widget=forms.Textarea(),
    )

    parent = forms.ChoiceField(
        label=_("Parent Forum"),
        required=False,
        widget=TreeSelectWidget(Forum),
    )

    status = forms.ChoiceField(
        label=_("Status"),
        required=True,
        choices=Forum._meta.get_field("status").get_choices(),
    )

    def __init__(self, *args, **kwargs):
        self.container = kwargs.get('container', None)
        self.current_forum = kwargs.get('current_forum', None)
        if kwargs.has_key('container'):
            kwargs.pop('container')
        if kwargs.has_key('current_forum'):
            kwargs.pop('current_forum')
        super(ForumForm, self).__init__(*args, **kwargs)
        """ choices for forum parents: only forums at the same container
        are allowed and forums with no! threads! """
        forums = Forum.objects.filter(container=self.container)
        if self.current_forum:
            forums = forums.exclude(id=self.current_forum.id)
        forums_with_threads = [
            thread.forum.id for thread in ForumThread.objects.all()
        ]
        forums = forums.exclude(id__in=forums_with_threads)
        parent_choices = BLANK_CHOICE_DASH + [
            (forum.id, smart_truncate(str(forum), 32)) for forum in forums
        ]
        self.fields['parent'].choices = parent_choices


class ThreadForm(dynamicforms.Form):
    """
    Form for forum threads
    """
    subject = forms.CharField(
        label=_("Subject"),
        required=True,
        max_length=255,
    )

    message = forms.CharField(
        label=_("Message"),
        required=True,
        #widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
        widget=forms.Textarea(),
    )

    forum = forms.ChoiceField(
        label=_("Forum"),
        required=False,
        widget=TreeSelectWidget(Forum),
    )

    is_sticky = forms.BooleanField(
        label=_("Sticky"),
        required=False,
        help_text=_(
            "check this field, if you want your thread to appear continually at the top of the forum."
        ),
    )

    def __init__(self, *args, **kwargs):
        self.container = kwargs.get('container', None)
        if self.container:
            kwargs.pop('container')
        super(ThreadForm, self).__init__(*args, **kwargs)

        forums = Forum.objects.filter(container=self.container)
        forum_choices = [
            (forum.id, smart_truncate(str(forum), 32)) for forum in forums
        ]
        self.fields['forum'].choices = forum_choices


class ReplyForm(dynamicforms.Form):
    """
    Form for forum replies
    """
    message = forms.CharField(
        label=_("Message"),
        required=True,
        #widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
        widget=forms.Textarea(),
    )
