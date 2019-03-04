# Event Import Specification

_Last update: February 27, 2019_

[TOC]

## Introduction ##

The Creative City Berlin website shows events that can be created by its users or imported from content partners.

## How to prepare the feed?

The JSON for the import API should have the following structure:

```javascript
{
    "meta": {
        // meta information
    },
    "events": [
        {
            // event properties
            "event_times": [
                {
                    // event time properties
                },
                {
                    // event time properties
                },
                // other event times
            ],
            "opening_hours": {
                // opening hours properties
            }
        },
        {
            // event properties
        },
        // other events
    ]    
}
```

### The Meta Section ###

The `"meta"` section contains information about pagination and amount of events, as follows:

| Key                | Type    | Required | Description                                                            | Example                               |
|--------------------|---------|----------|------------------------------------------------------------------------|---------------------------------------|
| `"next"`           | URL     | no       | The API URL for the next page (or empty string for the last page)      | "http://example.com/api/events/?page=3" |
| `"previous"`       | URL     | no       | The API URL for the previous page (or empty string for the first page) | "http://example.com/api/events/?page=1" |
| `"total_count"`    | integer | yes      | How many events are there in total?                               | 521                                   |
| `"items_per_page"` | integer | yes      | What is the maximal amount of events per page?                    | 50                                    |

### The Events Section ###

The `"events"` section contains paginated list of events and their events.

## Events ##

### The Event Object ###

Each `event` object has the following keys and values:

| Object                   | Type              | Required | Description                                              | Example                            |
|--------------------------|-------------------|----------|----------------------------------------------------------|------------------------------------|
| `"id"`                   | string or integer | yes      | Unique event ID on your website                          | 12                                 |
| `"creation_date"`        | dateTime          | yes      | event creation timestamp in ISO 8601 format              | "2016-04-14T16:27:38"              |
| `"modified_date"`        | dateTime          | no       | event modification timestamp in ISO 8601 format          | "2016-04-14T16:27:38"              |
| `"title_de"`             | string            | yes      | Title in German                                          |                                    |
| `"title_en"`             | string            | no       | Title in English                                         |                                    |
| `"description_de"`       | string            | yes      | Plain-text description in German. HTML is not allowed.   |                                    |
| `"description_en"`       | string            | no       | Plain-text description in English. HTML is not allowed.  |                                    |
| `"event_type_id"`        | string            | yes      | ID of one of the event types                             | "exhibition"                       |
| `"event_times"`          | list              | no       | list of event times                                      | [{...}, {...}]                     |
| `"categories"`           | list              | no       | list of category IDs                                     | ["bildende-kunst", "fotografie"]   |
| `"venue_title"`          | string            | no       | Venue title                                              | "Hamburger Bahnhof"                |
| `"street_address"`       | string            | no       | Street address (first line) of the location              |                                    |
| `"street_address2"`      | string            | no       | Street address (second line) of the location             |                                    |
| `"postal_code"`          | string            | no       | Postal code of the location                              |                                    |
| `"city"`                 | string            | no       | City of the location                                     |                                    |
| `"latitude"`             | string            | no       | Latitude of the location                                 | "52.5192"                          |
| `"longitude"`            | string            | no       | Longitude of the location                                | "13.4061"                          |
| `"image"`                | URL               | no       | URL of event image in JPG format. Should end with ".jpg" | https://example.com/exhibition.jpg |
| `"photo_author"`         | string            | no       | The author of the image.                                 | John Doe                           |
| `"fees_de"`              | string            | no       | Prices in German                                         | "Erwachsene: 12 €. Kinder: Frei"   |
| `"fees_en"`              | string            | no       | Prices in English                                        | "Adults: 12 €. Children: Free"     |
| `"opening_times"`        | object            | no       | Opening times                                            | {...}                              |
| `"tags"`                 | list              | no       | List of tags                                             | ["original", "exclusive"]          |

### Event Types

These are the job types that can be used:

- Show | Aufführung (ID="show")
- Exhibition | Ausstellung (ID="exhibition")
- Reception | Empfang (ID="reception")
- Opening | Eröffnung (ID="opening")
- Guided Tour | Führung (ID="guided-tour")
- Festival | Festival (ID="festival")
- Closing-Event | Finissage (ID="closing-event")
- Convention | Kongress/Fachtagung/Konferenz (ID="convention")
- Concert | Konzert (ID="concert")
- Reading | Lesung (ID="reading")
- Meeting | Meeting (ID="meeting")
- Trade Show | Messe (ID="trade-show")
- Performance | Performance (ID="performance")
- Workshop | Seminar/Workshop/Kurs (ID="workshop")
- Vernissage | Vernissage (ID="vernissage")
- Lecture | Vortrag/Diskussion (ID="lecture")
- Competition | Wettbewerb/Ausschreibung (ID="competition")
- Open-Day | Tag der offenen Tür (ID="open-day")
- Press Conference | Pressekonferenz (ID="pressekonferenz")
- Panel Discussion | Podiumsdiskussion (ID="podiumsdiskussion")
- Aktionstag | Aktionstag (ID="aktionstag")
- Art Week | Kunstwoche (ID="kunstwoche")
- Consultation | Beratung (ID="beratung")
- Film | Film (ID="film")

### Categories

These are the categories that can be used:

- Architecture | Architektur (ID="architektur")
- Visual Arts | Bildene Kunst (ID="bildende-kunst")
- Design | Design (ID="design")
- Event Industry | Eventbranche (ID="eventbranche")
- Film & Broadcast | Film & Rundfunk (ID="film-rundfunk")
- Photography | Fotographie (ID="fotografie")
- Games & Interactive | Games & Interactive (ID="games-interactive")
- Literature & Publishing | Literatur & Verlage (ID="literatur-verlage")
- Fashion & Textile | Mode & Textil (ID="mode-textil")
- Music | Musik (ID="musik")
- Theatre & Dance | Tanz & Theater (ID="tanz-theater")
- Advertising & PR | Werbung & PR (ID="werbung-pr")
- Miscellaneous | Sonstiges (ID="sonstiges")

### Event Time

| Object         | Type              | Required | Description                                           | Example      |
|----------------|-------------------|----------|-------------------------------------------------------|--------------|
| `"id"`         | string or integer | yes      | Unique event time ID on your website                  | 12           |
| `"label"`      | string            | no       | Event label                                           | "premiere"   |
| `"start_date"` | date              | yes      | Start date in ISO 8601 format, Europe/Berlin timezone | "2019-05-05" |
| `"start_time"` | time              | no       | Start time in ISO 8601 format, Europe/Berlin timezone | "19:00"      |
| `"end_date"`   | date              | no       | End date in ISO 8601 format, Europe/Berlin timezone   | "2019-05-05" |
| `"end_time"`   | time              | no       | End time in ISO 8601 format, Europe/Berlin timezone   | "22:00"      |
| `"is_all_day"` | boolean           | no       | Is the event happening the whole day?                 | false        |

### Opening Times

| Object                   | Type    | Required | Description                                                     | Example                                      |
|--------------------------|---------|----------|-----------------------------------------------------------------|----------------------------------------------|
| `"is_appointment_based"` | boolean | no       | Is the event appointment based?                                 | false                                        |
| `"mon_open"`             | time    | no       | Opening time on Monday                                          | "10:00"                                      |
| `"mon_break_close"`      | time    | no       | Start of the break on Monday. Leave empty if there no break.    | "14:00"                                      |
| `"mon_break_open"`       | time    | no       | End of the break on Monday. Leave empty if there no break.      | "15:00"                                      |
| `"mon_close"`            | time    | no       | Closing time on Monday                                          | "19:00"                                      |
| `"tue_open"`             | time    | no       | Opening time on Tuesday                                         | "10:00"                                      |
| `"tue_break_close"`      | time    | no       | Start of the break on Tuesday. Leave empty if there no break.   | "14:00"                                      |
| `"tue_break_open"`       | time    | no       | End of the break on Tuesday. Leave empty if there no break.     | "15:00"                                      |
| `"tue_close"`            | time    | no       | Closing time on Tuesday                                         | "19:00"                                      |
| `"wed_open"`             | time    | no       | Opening time on Wednesday                                       | "10:00"                                      |
| `"wed_break_close"`      | time    | no       | Start of the break on Wednesday. Leave empty if there no break. | "14:00"                                      |
| `"wed_break_open"`       | time    | no       | End of the break on Wednesday. Leave empty if there no break.   | "15:00"                                      |
| `"wed_close"`            | time    | no       | Closing time on Wednesday                                       | "19:00"                                      |
| `"thu_open"`             | time    | no       | Opening time on Thursday                                        | "10:00"                                      |
| `"thu_break_close"`      | time    | no       | Start of the break on Thursday. Leave empty if there no break.  | "14:00"                                      |
| `"thu_break_open"`       | time    | no       | End of the break on Thursday. Leave empty if there no break.    | "15:00"                                      |
| `"thu_close"`            | time    | no       | Closing time on Thursday                                        | "19:00"                                      |
| `"fri_open"`             | time    | no       | Opening time on Friday                                          | "10:00"                                      |
| `"fri_break_close"`      | time    | no       | Start of the break on Friday. Leave empty if there no break.    | "14:00"                                      |
| `"fri_break_open"`       | time    | no       | End of the break on Friday. Leave empty if there no break.      | "15:00"                                      |
| `"fri_close"`            | time    | no       | Closing time on Friday                                          | "19:00"                                      |
| `"sat_open"`             | time    | no       | Opening time on Saturday                                        | "11:00"                                      |
| `"sat_break_close"`      | time    | no       | Start of the break on Saturday. Leave empty if there no break.  | ""                                           |
| `"sat_break_open"`       | time    | no       | End of the break on Saturday. Leave empty if there no break.    | ""                                           |
| `"sat_close"`            | time    | no       | Closing time on Saturday                                        | "17:00"                                      |
| `"sun_open"`             | time    | no       | Opening time on Sunday                                          | ""                                           |
| `"sun_break_close"`      | time    | no       | Start of the break on Sunday. Leave empty if there no break.    | ""                                           |
| `"sun_break_open"`       | time    | no       | End of the break on Sunday. Leave empty if there no break.      | ""                                           |
| `"sun_close"`            | time    | no       | Closing time on Sunday                                          | ""                                           |
| `"exceptions_de"`        | string  | no       | Exceptions for working hours in German                          | "Am ersten Montag jeden Monats geschlossen." |
| `"exceptions_en"`        | string  | no       | Exceptions for working hours in English                         | "Closed on the first Monday of every month." |
All times are in ISO 8601 format, Europe/Berlin timezone.

## Publishing

All the events of the feed will be published to [Creative City Berlin events](https://www.creative-city-berlin.de/de/events/) immediately when importing.
