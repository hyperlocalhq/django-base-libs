import vobject
import calendar

from datetime import date, datetime, timedelta

from django.utils.encoding import force_unicode
from django.db import models
from django.db.models.query import QuerySet
from django.template.defaultfilters import striptags

from base_libs.utils.html import decode_entities
from base_libs.utils.misc import get_website_url


def add_vevent(cal, event_time):
    """
    adds a vEvent object to iCalender
    
    event_time is an instance of EventTime
    """
    event = event_time.event.event
    vevent = cal.add('vevent')

    # Summary of ical containing title and title of the specific occurrence
    vevent.add(
        'summary'
    ).value = "%s - %s" % (force_unicode(event.get_title()), event_time.label)

    vevent.add('description').value = striptags(
        decode_entities(event.get_description())
    )

    # Adding start and end dates to ical event
    if event.has_start_date():
        if event_time.has_start_time():
            vevent.add('dtstart').value = event_time.start
            #Events have start time but now we need to check if they have time end
            if event_time.has_end_time():
                vevent.add('dtend').value = event_time.end
            else:
                end_hh = event_time.end_hh or event_time.start_hh
                end_ii = event_time.end_ii or event_time.start_ii
                if end_hh is None:
                    end_hh = 23
                if end_ii is None:
                    end_ii = 59
                vevent.add('dtend').value = datetime(
                    event_time.end_yyyy or event_time.start_yyyy,
                    event_time.end_mm or event_time.start_mm,
                    event_time.end_dd or event_time.start_dd, end_hh, end_ii
                )
        else:
            #Events have not start time but now we need to check if they have time end
            vevent.add('dtstart').value = date(
                event_time.start_yyyy or 2007, event_time.start_mm or 1,
                event_time.start_dd or 1
            )
            end_mm = event_time.end_mm or event_time.start_mm or 12
            if event_time.end_dd:
                end_dd = event_time.end_dd
            else:
                end_dd = event_time.start_dd or calendar.monthrange(
                    int(event_time.end_yyyy or event_time.start_yyyy),
                    int(event_time.end_mm or event_time.start_mm or 12),
                )[1]
            end_date = date(
                event_time.end_yyyy or event_time.start_yyyy, end_mm, end_dd
            )
            if event_time.end_dd:
                end_date = end_date + timedelta(days=1)
            vevent.add('dtend').value = end_date
    else:
        #Events without start date
        vevent.add('dtstart').value = date(
            event_time.start_yyyy or 2007, event_time.start_mm or 1,
            event_time.start_dd or 1
        )
        #Events have start time but now we need to check if they have time end
        if event_time.has_end_time():
            vevent.add('dtend').value = event_time.end
        else:
            vevent.add('dtend').value = date(
                event_time.end_yyyy or event_time.start_yyyy,
                event_time.end_mm or event_time.start_mm,
                event_time.end_dd + 1 or event_time.start_dd
            )

    if event.postal_address:
        vevent.add('location').value = unicode(event.postal_address)
    elif getattr(event, "venue", False):
        location = event.venue.get_title()
        venue_address = event.venue.get_address_string()
        if venue_address:
            location += ', ' + venue_address
        vevent.add('location').value = location
    vevent.add('url').value = get_website_url() + event.get_absolute_url()[1:]


def create_ics(events, vevent_function=add_vevent):
    """
    Creates an .ics (iCalendar) file which includes the given events
    
    events might refer to 
        * an Event instance
        * an EventTime instance
        * queryset of Event instances
        * queryset of EventTime instances
        * list of Event instances
        * list of EventTime instances
    """
    from jetson.apps.events.base import EventBase

    Event = models.get_model("events", "Event")
    EventTime = models.get_model("events", "EventTime")

    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this

    if isinstance(events, EventBase):
        # events is an instance of Event
        event = events
        for time in event.eventtime_set.all():
            vevent_function(cal, time)
    elif isinstance(events, EventTime):
        # events is an instance of EventTime
        time = events
        vevent_function(cal, time)
    elif isinstance(events, QuerySet):
        if issubclass(events.model, EventBase):
            # events is an queryset of Event instances
            for event in events:
                for time in event.eventtime_set.all():
                    vevent_function(cal, time)
        else:
            # events is an queryset of EventTime instances
            times = events
            for time in times:
                vevent_function(cal, time)
    elif events:
        if isinstance(events[0], EventBase):
            # events is a list of Event instances
            for event in events:
                for time in event.eventtime_set.all():
                    vevent_function(cal, time)
        else:
            # events is a list of EventTime instances
            times = events
            for time in times:
                vevent_function(cal, time)
    icalstream = cal.serialize()
    return icalstream
