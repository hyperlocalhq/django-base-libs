import vobject
from datetime import date

from django.db import models
from django.db.models.query import QuerySet

from base_libs.utils.misc import get_website_url

Event = models.get_model("events", "Event")
EventTime = models.get_model("events", "EventTime")


def add_vevent(cal, event_time):
    """
    adds a vEvent object to iCalender
    
    event_time is an instance of EventTime
    """
    event = event_time.event
    vevent = cal.add('vevent')
    vevent.add('summary').value = event.get_title()
    vevent.add('description').value = event.get_description()
    if event.has_start_date():
        if event_time.has_start_time():
            vevent.add('dtstart').value = event_time.start
        else:
            vevent.add('dtstart').value = date(event_time.start_yyyy or 2007, event_time.start_mm or 1,
                                               event_time.start_dd or 1)
    if event.has_end_date():
        if event_time.has_end_time():
            vevent.add('dtend').value = event_time.end
        else:
            vevent.add('dtend').value = date(event_time.end_yyyy or 2007, event_time.end_mm or 1,
                                             event_time.end_dd or 1)
    if getattr(event, "venue", False):
        location = event.venue.get_title()
        venue_address = event.venue.get_address_string()
        if venue_address:
            location += ', ' + venue_address
        vevent.add('location').value = location
    vevent.add('url').value = get_website_url() + event.get_absolute_url()[1:]


def create_ics(events):
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

    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this

    if isinstance(events, Event):
        # events is an instance of Event
        event = events
        for time in event.eventtime_set.all():
            add_vevent(cal, time)
    elif isinstance(events, EventTime):
        # events is an instance of EventTime
        time = events
        add_vevent(cal, time)
    elif isinstance(events, QuerySet):
        if issubclass(events.model, Event):
            # events is an queryset of Event instances
            for event in events:
                for time in event.eventtime_set.all():
                    add_vevent(cal, time)
        else:
            # events is an queryset of EventTime instances
            times = events
            for time in times:
                add_vevent(cal, time)
    elif events:
        if isinstance(events[0], Event):
            # events is a list of Event instances
            for event in events:
                for time in event.eventtime_set.all():
                    add_vevent(cal, time)
        else:
            # events is a list of EventTime instances
            times = events
            for time in times:
                add_vevent(cal, time)
    icalstream = cal.serialize()
    return icalstream
