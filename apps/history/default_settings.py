# -*- coding: utf-8 -*-
from django.conf import settings

# Activity constants
A_UNDEFINED = 0
A_ADDITION = 1
A_CHANGE = 2
A_DELETION = 3
A_READ = 4
# custom activities depend on each app and model separately
# i.e. it might be sending an email for mailing.EmailMessage
#      or exporting a pdf out of flatpages.FlatPage
A_CUSTOM1 = 5
A_CUSTOM2 = 6
A_CUSTOM3 = 7

# Activity scope constants
AS_SYSTEM = 0  # might be shown only to administrators
AS_PRIVATE = 1  # might be shown only to the user, who is related to the action
AS_PUBLIC = 2  # might be shown to everyone

# Which models, what actions and in what scope should be tracked in the log for
# activity history and measuring?
TRACKED_MODELS = getattr(
    settings,
    "HISTORY_TRACKED_MODELS",
    {
        'people.person':
            {
                A_ADDITION: AS_SYSTEM,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_SYSTEM,
            },
        'bookmarks.bookmark':
            {
                A_ADDITION: AS_SYSTEM,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_SYSTEM,
            },
        'comments.comment':
            {
                A_ADDITION: AS_SYSTEM,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_SYSTEM,
            },
        'resources.document':
            {
                A_ADDITION: AS_PUBLIC,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PUBLIC,
            },
        'mailing.emailmessage':
            {
                A_ADDITION: AS_SYSTEM,
                A_CUSTOM1: AS_PRIVATE,
                A_CUSTOM2: AS_PRIVATE,
            },
        'mailing.emailtemplate':
            {
                A_ADDITION: AS_PRIVATE,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PRIVATE,
            },
        'events.event':
            {
                A_ADDITION: AS_PRIVATE,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PRIVATE,
            },
        'individual_relations.individualrelation':
            {
                A_ADDITION: AS_PRIVATE,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PRIVATE,
            },
        'favorites.favorite':
            {
                A_ADDITION: AS_PRIVATE,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PRIVATE,
            },
        'filebrowser.file':
            {
                A_ADDITION: AS_PRIVATE,
                A_CHANGE: AS_PRIVATE,
                A_DELETION: AS_PRIVATE,
            },
        'flaggings.flagging':
            {
                A_ADDITION: AS_PRIVATE,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PRIVATE,
            },
        'flatpages.flatpage':
            {
                A_ADDITION: AS_SYSTEM,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_SYSTEM,
            },
        'blocks.infoblock':
            {
                A_ADDITION: AS_SYSTEM,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_SYSTEM,
            },
        'institutions.institution':
            {
                A_ADDITION: AS_PUBLIC,
                A_CHANGE: AS_PRIVATE,
                A_DELETION: AS_PUBLIC,
            },
        'priorities.priority':
            {
                A_ADDITION: AS_PRIVATE,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PRIVATE,
            },
        'blog.post':
            {
                A_ADDITION: AS_PUBLIC,
                A_CHANGE: AS_PUBLIC,
                A_DELETION: AS_PUBLIC,
            },
        'forum.post':
            {
                A_ADDITION: AS_PUBLIC,
                A_CHANGE: AS_PUBLIC,
                A_DELETION: AS_PUBLIC,
            },
        'ratings.rating':
            {
                A_ADDITION: AS_SYSTEM,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_SYSTEM,
            },
        'reminders.reminder':
            {
                A_ADDITION: AS_PRIVATE,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PRIVATE,
            },
        'recommendations.recommendation':
            {
                A_ADDITION: AS_PUBLIC,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PUBLIC,
            },
        'configuration.sitesettings': {
            A_CHANGE: AS_SYSTEM,
        },
        'groups_networks.groupmembership':
            {
                A_ADDITION: AS_PUBLIC,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_PUBLIC,
            },
        'structure.term':
            {
                A_ADDITION: AS_SYSTEM,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_SYSTEM,
            },
        'auth.user': {
            A_CHANGE: AS_SYSTEM,
        },
        'structure.vocabulary':
            {
                A_ADDITION: AS_SYSTEM,
                A_CHANGE: AS_SYSTEM,
                A_DELETION: AS_SYSTEM,
            },
    },
)
