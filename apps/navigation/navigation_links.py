# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def for_all(context):
    return True


def for_anonymous_only(context):
    return context['request'].user.is_anonymous()


def for_authenticated_only(context):
    return context['request'].user.is_authenticated()


def is_claimable_institution(context):
    return (
        'object' in context and
        getattr(context['object'], "is_institution", lambda: False)() and
        getattr(context['object'], "is_claimable", lambda: False)()
    )


def is_deletable_job_offer(context):
    return (
        'object' in context and
        getattr(context['object'], "is_job_offer", lambda: False)() and
        getattr(context['object'], "is_deletable", lambda: False)()
    )


def is_deletable_event(context):
    return (
        'object' in context and
        getattr(context['object'], "is_event", lambda: False)() and
        getattr(context['object'], "is_deletable", lambda: False)()
    )


# TODO: 1) add more conditions where to show what for anonymous users.
# TODO: 2) maybe show some links with login required as teasers.
# TODO: 3) add badges for some of the links with object count.


navigation_links = {
    'members': [
        {
            'url_de': '/de/relaunch2015/network/',
            'url_en': '/en/relaunch2015/network/',
            'text_de': 'Alle',
            'text_en': 'All',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/$',
        },
        {
            'url_de': '/de/relaunch2015/network/favorites/',
            'url_en': '/en/relaunch2015/network/favorites/',
            'text_de': 'Favoriten',
            'text_en': 'Favorites',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/favorites/$',
        },
        {
            'url_de': '/de/relaunch2015/network/own-institutions/',
            'url_en': '/en/relaunch2015/network/own-institutions/',
            'text_de': 'Meine Institutionen',
            'text_en': 'My Institutions',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/own-institutions/$',
        },
        # {
        #     'url_de': '/de/relaunch2015/network/add-institution/',
        #     'url_en': '/en/relaunch2015/network/add-institution/',
        #     'text_de': 'Neue Institution eintragen',
        #     'text_en': 'Add New Institution',
        #     'should_be_shown': for_authenticated_only,
        #     'highlight_pattern': r'^/(de|en)/relaunch2015/network/add-institution/$',
        # },
        {
            'url_de': '/de/relaunch2015/network/relationships/',
            'url_en': '/en/relaunch2015/network/relationships/',
            'text_de': 'Bestätigte Kontakte',
            'text_en': 'Confirmed Contacts',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/relationships/$',
        },
        {
            'url_de': '/de/relaunch2015/network/requested/',
            'url_en': '/en/relaunch2015/network/requested/',
            'text_de': 'Einladungen',
            'text_en': 'Invitations',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/(requests|requested)/$',
        },
    ],

    'member': [
        {
            'url_de': '/de/relaunch2015/network/member/{{ object.slug }}/',
            'url_en': '/en/relaunch2015/network/member/{{ object.slug }}/',
            'text_de': 'Profil',
            'text_en': 'Profile',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/member/{{ object.slug }}/$',
        },
        {
            'url_de': '/de/relaunch2015/network/member/{{ object.slug }}/portfolio/',
            'url_en': '/en/relaunch2015/network/member/{{ object.slug }}/portfolio/',
            'text_de': 'Portfolio',
            'text_en': 'Portfolio',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/member/{{ object.slug }}/portfolio/',
        },
        {
            'url_de': '/de/relaunch2015/network/member/{{ object.slug }}/events/',
            'url_en': '/en/relaunch2015/network/member/{{ object.slug }}/events/',
            'text_de': 'Events',
            'text_en': 'Events',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/member/{{ object.slug }}/events/',
        },
        {
            'url_de': '/de/relaunch2015/network/member/{{ object.slug }}/blog/',
            'url_en': '/en/relaunch2015/network/member/{{ object.slug }}/blog/',
            'text_de': 'Blog',
            'text_en': 'Blog',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/member/{{ object.slug }}/blog/',
        },
    ],

    'portfolios': [
        {
            'url_de': '/de/portfolios/featured/',
            'url_en': '/en/portfolios/featured/',
            'text_de': 'Featured',
            'text_en': 'Featured',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/portfolios/featured/$',
        },
        {
            'url_de': '/de/portfolios/',
            'url_en': '/en/portfolios/',
            'text_de': 'Alle',
            'text_en': 'All',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/portfolios/$',
        },
        {
            'url_de': '/de/portfolios/favorites/',
            'url_en': '/en/portfolios/favorites/',
            'text_de': 'Favoriten',
            'text_en': 'Favorites',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/portfolios/favorites/$',
        },
        {
            'url_de': '/de/relaunch2015/network/member/{{ request.user.username }}/portfolio/album/add/',
            'url_en': '/en/relaunch2015/network/member/{{ request.user.username }}/portfolio/album/add/',
            'text_de': 'Neues Portfolio hinzufügen',
            'text_en': 'Add Own Portfolio',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/member/{{ request.user.username }}/portfolio/album/add/$',
        },
    ],

    'jobs': [
        {
            'url_de': '/de/relaunch2015/jobs/',
            'url_en': '/en/relaunch2015/jobs/',
            'text_de': 'Jobs',
            'text_en': 'Jobs',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/jobs/$',
        },
        {
            'url_de': '/de/relaunch2015/jobs/internships/',
            'url_en': '/en/relaunch2015/jobs/internships/',
            'text_de': 'Praktika',
            'text_en': 'Internships',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/jobs/internships/$',
        },
        {
            'url_de': '/de/relaunch2015/jobs/all/',
            'url_en': '/en/relaunch2015/jobs/all/',
            'text_de': 'Alle',
            'text_en': 'All',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/jobs/all/$',
        },
        {
            'url_de': '/de/relaunch2015/jobs/own-jobs/',
            'url_en': '/en/relaunch2015/jobs/own-jobs/',
            'text_de': 'Meine Jobangebote',
            'text_en': 'My Job Offers',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/jobs/own-jobs/$',
        },
        {
            'url_de': '/de/relaunch2015/jobs/add/',
            'url_en': '/en/relaunch2015/jobs/add/',
            'text_de': 'Jobangebot eintragen',
            'text_en': 'Offer a Job',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/jobs/add/$',
        },
    ],

    'bulletin_board': [
        {
            'url_de': '/de/relaunch2015/market-place/',
            'url_en': '/en/relaunch2015/market-place/',
            'text_de': 'Alle',
            'text_en': 'All',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/market-place/$',
        },
        {
            'url_de': '/de/relaunch2015/market-place/my-bulletins/',
            'url_en': '/en/relaunch2015/market-place/my-bulletins/',
            'text_de': 'Meine Inserate',
            'text_en': 'My Bulletins',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/market-place/my-bulletins/$',
        },
        {
            'url_de': '/de/relaunch2015/market-place/add/',
            'url_en': '/en/relaunch2015/market-place/add/',
            'text_de': 'Inserat eintragen',
            'text_en': 'Add a Bulletin',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/market-place/add/$',
        },
    ],

    'events': [
        {
            'url_de': '/de/relaunch2015/events/',
            'url_en': '/en/relaunch2015/events/',
            'text_de': 'Events',
            'text_en': 'Events',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/events/$',
        },
        {
            'url_de': '/de/relaunch2015/events/favorites/',
            'url_en': '/en/relaunch2015/events/favorites/',
            'text_de': 'Favoriten',
            'text_en': 'Favorites',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/events/favorites/$',
        },
        {
            'url_de': '/de/relaunch2015/events/own-events/',
            'url_en': '/en/relaunch2015/events/own-events/',
            'text_de': 'Meine Events',
            'text_en': 'My Events',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/events/own-events/$',
        },
        {
            'url_de': '/de/relaunch2015/events/add/',
            'url_en': '/en/relaunch2015/events/add/',
            'text_de': 'Neuen Event eintragen',
            'text_en': 'Add a new Event',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/events/add/$',
        },

    ],

    'event': [
        {
            'url_de': '/de/relaunch2015/events/event/{{ object.slug }}/',
            'url_en': '/en/relaunch2015/events/event/{{ object.slug }}/',
            'text_de': 'Profil',
            'text_en': 'Profile',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/events/event/{{ object.slug }}/$',
        },
        {
            'url_de': '/de/relaunch2015/events/event/{{ object.slug }}/portfolio/',
            'url_en': '/en/relaunch2015/events/event/{{ object.slug }}/portfolio/',
            'text_de': 'Portfolio',
            'text_en': 'Portfolio',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/relaunch2015/events/event/{{ object.slug }}/portfolio/$',
        },
    ],

    'menu_activities': [
        {
            'url_de': '/de/relaunch2015/network/member/{{ request.user.username }}/portfolio/album/add/',
            'url_en': '/en/relaunch2015/network/member/{{ request.user.username }}/portfolio/album/add/',
            'text_de': 'neues Projekt',
            'text_en': 'new Project',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/member/{{ request.user.username }}/portfolio/album/add/',
            'icon': 'fa-rocket',
        },
        {
            'url_de': '/de/events/add/',
            'url_en': '/en/events/add/',
            'text_de': 'neues Event',
            'text_en': 'new Event',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/events/add/',
            'icon': 'fa-calender-plus',
        },
        {
            'url_de': '/de/relaunch2015/network/member/{{ request.user.username }}/blog/new/',
            'url_en': '/en/relaunch2015/network/member/{{ request.user.username }}/blog/new/',
            'text_de': 'Blogpost',
            'text_en': 'Blog Post',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/relaunch2015/network/member/{{ request.user.username }}/blog/new/',
            'icon': 'fa-bullhorn',
        },
        {
            'url_de': '/de/jobs/add/',
            'url_en': '/en/jobs/add/',
            'text_de': 'Jobanzeige',
            'text_en': 'Job Offer',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/jobs/add/',
            'icon': 'fa-wrench',
        },
        {
            'url_de': '{{ object.get_url_path }}claim/',
            'url_en': '{{ object.get_url_path }}claim/',
            'text_de': 'mein Unternehmen',
            'text_en': 'claim Institution',
            'should_be_shown': is_claimable_institution,
            'highlight_pattern': r'^{{ object.get_url_path }}claim/',
            'icon': 'fa-fist',
        },
        {
            'url_de': '{{ object.get_url_path }}delete/',
            'url_en': '{{ object.get_url_path }}delete/',
            'text_de': 'Job löschen',
            'text_en': 'delete Job Offer',
            'should_be_shown': is_deletable_job_offer,
            'highlight_pattern': r'^{{ object.get_url_path }}delete/',
            'icon': 'fa-thumb-down',
        },
        {
            'url_de': '{{ object.get_url_path }}delete/',
            'url_en': '{{ object.get_url_path }}delete/',
            'text_de': 'Event löschen',
            'text_en': 'delete Event',
            'should_be_shown': is_deletable_event,
            'highlight_pattern': r'^{{ object.get_url_path }}delete/',
            'icon': 'fa-calender-minus',
        },
    ],

    'menu_settings': [
        {
            'url_de': '/de/notification/settings/',
            'url_en': '/en/notification/settings/',
            'text_de': 'Benachrichtigungen',
            'text_en': 'Notifications',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/notification/settings/',
        },
        {
            'url_de': '/de/social-connections/',
            'url_en': '/en/social-connections/',
            'text_de': 'Soziale Verbindungen',
            'text_en': 'Social Connections',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/social-connections/',
        },
        {
            'url_de': '/de/my-profile/privacy/',
            'url_en': '/en/my-profile/privacy/',
            'text_de': 'Privatsphäre',
            'text_en': 'Privacy Settings',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/my-profile/privacy/',
        },
        {
            'url_de': '/de/password-change/',
            'url_en': '/en/password-change/',
            'text_de': 'Kennwort ändern',
            'text_en': 'Change Password',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/password[-_]change/',
        },
        {
            'url_de': '/de/my-profile/delete/',
            'url_en': '/en/my-profile/delete/',
            'text_de': 'Mein Profil löschen',
            'text_en': 'Delete My Profile',
            'should_be_shown': for_authenticated_only,
            'highlight_pattern': r'^/(de|en)/my-profile/delete/',
        },
    ],

    'kreativarbeiten': [
        {
            'url_de': '/de/kreativarbeiten/blog/',
            'url_en': '/en/kreativarbeiten/blog/',
            'text_de': 'Blog',
            'text_en': 'Blog',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/kreativarbeiten/blog/',
            'is_promoted': True,
            'is_login_required': True,
        },
        {
            'url_de': '/de/kreativarbeiten/best-practice/',
            'url_en': '/en/kreativarbeiten/best-practice/',
            'text_de': 'Best Practice',
            'text_en': 'Best Practice',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/kreativarbeiten/best-practice/',
        },
        {
            'url_de': '/de/kreativarbeiten/events/',
            'url_en': '/en/kreativarbeiten/events/',
            'text_de': 'Termine',
            'text_en': 'Events',
            'should_be_shown': for_all,
            'highlight_pattern': r'^/(de|en)/kreativarbeiten/events/',
        },
    ],
}
