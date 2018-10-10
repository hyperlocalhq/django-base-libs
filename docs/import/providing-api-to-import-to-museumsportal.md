# How to prepare data that will be imported to Museumsportal? #

[TOC]

## Introduction ##

There are three types of objects to prepare for import to Museumsportal. They are: **exhibitions**, **events**, and **workshops** (guided tours). The API should be provided as a web page in JSON (preferably) or XML format showing lists of objects with IDs and creation and modification timestamps. The import script will create according objects at Museumsportal and will map the IDs from the source to the IDs of the target. Creation and modification timestamps are necessary to track if the objects have changed since last import, so that the data could be updated.

General guidelines:

* The document should be encoded in UTF-8.
* The date and time format used should be "yyyy-mm-ddThh:mm" (with "T" or without), like "2007-04-05 14:30".
* All URLs in the links should start with protocol, like "**http://**www.google.com/".
* If data is paginated, there should be some variable telling the total amount of pages.
* If data should not be open to public, the API should be secured under an API_KEY that will be passed as URL query parameter, e.g. **?api_key=abc123**.
* If you manage multiple museums, please additionally provide a list of their IDs mapping to museum names.
* If your database structure doesn't match and you can't provide all information that is stored at Museumsportal, just skip some fields and give us a note.

The general structure for the page in JSON format could be like this:

    {
        "meta": {
            "page": 1,
            "total_pages": 9,
            "total_count": 521
        },
        "objects": [
            {
                "id": 123,
                "created": "2014-09-01 10:30",
                "modified": null,
                "title_de": "Beispiel",
                "title_en": "Example",
                ...
            },
            ...
        ]
    }

## Exhibitions ##

Exhibition last at the museums from start date till the end date. Some of them are permanent. We expect this data for **exhibitions**:

Field | Type | Description
---|---|---
id |	integer |	Unique identifier
created |	string |	Creation date and time in a format "yyyy-mm-ddThh:mm:as"
modified |	string |	Modification date and time in a format "yyyy-mm-ddThh:mm:ss"
title\_de |	string |	Title in German
title\_en |	string |	Title in English
subtitle\_de |	string |	Subtitle in German
subtitle\_en |	string |	Subtitle in English
press\_text\_de |	string |	Press text in German
press\_text\_en |	string |	Press text in English
catalog\_de |	string |	Catalog information in German
catalog\_en |	string |	Catalog information in English
catalog\_ordering\_de |	string |	Catalog ordering link for German readers
catalog\_ordering\_en |	string |	Catalog ordering link for English readers
website\_de |	string |	The URL of the exhibition at your website in German
website\_en |	string |	The URL of the exhibition at your website in English
start |	string |	Start date in a format "yyyy-mm-dd"
end |	string |	End date in a format "yyyy-mm-dd"
vernissage |	string |	The date and time of the vernissage in a format "yyyy-mm-ddThh:mm"
finissage |	string |	The date and time of the finissage in a format "yyyy-mm-ddThh:mm"
exhibition\_extended |	boolean |	Is this exhibition extended?
permanent |	boolean |	Is this exhibition permanent?
museum\_id |	integer |	Unique identifier of the museum
location\_name |	string |	Location name, when differs from museum
street\_address |	string | Street address
street\_address2 |	string |	Second line of street address
postal\_code |	string |	Postal code
city |	string |	City
country |	string |	Country code e.g. "de"
latitude |	float |	Latitude
longitude |	float |	Longitude
other\_locations\_de |	string |	Other locations in German
other\_locations\_en |	string |	Other locations in English
organizers |	list |	List of additional organizers
museum\_prices |	boolean |	Are the prices the same as at the museum?
free\_entrance |	boolean |	Is the entrance free?
admission\_price |	string |	Admission price in Euros, e.g. "12.00"
admission\_price\_info\_de |	string |	Admission price information in German
admission\_price\_info\_en |	string |	Admission price information in English
reduced\_price |	string |	Reduced admission price in Euros e.g. "8.00"
reduced\_price\_info\_de |	string |	Reduced admission price information in German
reduced\_price\_info\_en |	string |	Reduced admission price information in English
museum\_opening\_hours |	boolean |	Opening hours of the museum
seasons |	list |	List of season objects (one or none items)
suitable\_for\_disabled |	boolean |	Is the exhibition suitable for disabled?
suitable\_for\_disabled\_info\_de |	string |	Information in German about suitability for disabled people
suitable\_for\_disabled\_info\_en |	string |	Information in English about suitability for disabled people
is\_for\_children |	boolean |	Is the exhibition suitable for children?
media\_files |	list |	List of media files

Exhibition **organizers** should have these fields:

Field |	Type |	Description
---|---|---
organizing\_museum\_id |	string | Unique identifier of a museum
organizer\_title |	string |	Organizer title if not organized by a museum
organizer\_url\_link |	string |	Organizer URL if not organized by a museum

Exhibition **seasons** should have these fields:

Field |	Type |	Description
---|---|---
is\_appointment_based |	boolean |	Are the visits based on appointments?
is\_open\_24\_7 |	boolean |	Is open 24/7?
mon\_open |	string |	Opening time on Mondays in a format "hh:mm"
mon\_close |	string |	Closing time on Mondays in a format "hh:mm"
mon\_break\_close |	string |	Start time of the break on Mondays in a format "hh:mm"
mon\_break\_open |	string |	End time of the break on Mondays in a format "hh:mm"
tue\_open |	string |	Opening time on Tuesdays in a format "hh:mm"
tue\_close |	string |	Closing tine on Tuesdays in a format "hh:mm"
tue\_break\_close |	string |	Start time of the break on Tuesdays in a format "hh:mm"
tue\_break\_open |	string |	End time of the break on Tuesdays in a format "hh:mm"
wed\_open |	string |	Opening time on Wednesdays in a format "hh:mm"
wed\_close |	string |	Closing time on Wednesdays in a format "hh:mm"
wed\_break\_close |	string |	Start time of the break on Wednesdays in a format "hh:mm"
wed\_break\_open |	string |	End time of the break on Wednesdays in a format "hh:mm"
thu\_open |	string |	Opening time on Thursdays in a format "hh:mm"
thu\_close |	string |	Closing time on Thursdays in a format "hh:mm"
thu\_break\_close |	string |	Start time of the break on Thursdays in a format "hh:mm"
thu\_break\_open |	string |	End time of the break on Thursdays in a format "hh:mm"
fri\_open |	string |	Opening time on Fridays in a format "hh:mm"
fri\_close |	string |	Closing time on Fridays in a format "hh:mm"
fri\_break\_close |	string |	Start time of the break on Fridays in a format "hh:mm"
fri\_break\_open |	string |	End time of the break on Fridays in a format "hh:mm"
sat\_open |	string |	Opening time on Saturdays in a format "hh:mm"
sat\_close |	string |	Closing time on Saturdays in a format "hh:mm"
sat\_break\_close |	string |	Start time of the break on Saturdays in a format "hh:mm"
sat\_break\_open |	string |	End time of the break on Saturdays in a format "hh:mm"
sun\_open |	string |	Opening time on Sundays in a format "hh:mm"
sun\_close |	string |	Closing time on Sundays in a format "hh:mm"
sun\_break\_close |	string |	Start time of the break on Sundays in a format "hh:mm"
sun\_break\_open |	string |	End time of the break on Sundays in a format "hh:mm"
exceptions\_de |	string |	Exceptional opening hours in German
exceptions\_en |	string |	Exceptional opening hours in English
last\_entry\_de |	string |	Information about last entry in German
last\_entry\_en |	string |	Information about last entry in English

Exhibition **media_files** should have these fields:

Field |	Type |	Description
---|---|---
created | string |	Creation date and time in a format "yyyy-mm-ddThh:mm:ss"
modified | string |	Modification date and time in a format "yyyy-mm-ddThh:mm:ss"
url |	string |	High-quality image URL
title\_de |	string |	Title in German
title\_en |	string |	Title in English
description\_de |	string |	Description in German
description\_en |	string |	Description in English
author |	string |	Author and Copyright
copyright\_limitations |	string |	Additional Copyright Information

So when accessed by **http://yourwebsite.de/api/exhibitions/?api_key=abc123** or similar path, we should get information about exhibitions in the following JSON format:

    {
        "meta": {
            "page": 1,
            "total_pages": 9,
            "total_count": 521
        },
        "objects": [
            {
                "id": 123,
                "created": "2012-09-10T17:09:52",
                "modified": "2014-07-09T11:08:53",
                "title_de": "... den alten Fritz, der im Volke lebt",
                "title_en": "... den alten Fritz, der im Volke lebt",
                "subtitle_de": "Das Bild Friedrichs des Großen bei Adolph Menzel",
                "subtitle_en": "Das Bild Friedrichs des Großen bei Adolph Menzel",
                "press_text_de": "Die Sammlungen der Nationalgalerie und des Kupferstichkabinetts besitzen einen Großteil der malerischen und grafischen Arbeiten, die der junge Adolph Menzel (1815-1905) mit Begeisterung und großer Detailtreue zum Leben Friedrichs des Großen geschaffen hat. Dazu gehören neben Bildern hunderte Studien, Probedrucke und Holzstöcke zu den großen Illustrationsfolgen des Künstlers. Am populärsten wurden die fast 400 Holzstiche zur 1840 erschienenen "Geschichte Friedrichs des Großen" von Franz Kugler. Mit dieser Arbeit hatte Menzel nicht nur ein enormes Detailwissen erworben, sondern ein Bild des Monarchen entwickelt, das er in den folgenden Jahren in einer Reihe von Gemälden variierte, die, bis auf drei Kriegsverluste, erstmals zusammen in der Ausstellung präsentiert werden. Sie zeigen Friedrich II. als aufgeklärten Monarchen, als willensstarken Kriegsherrn, als Freund der Philosophie und der Künste - eine bürgerliche Rezeption Friedrichs und damals ein Modell für die Gegenwart. Vorangestellt ist der Ausstellung ein Kapitel, das sich den Darstellungen Friedrichs des Großen durch Künstler widmet, die ihm noch persönlich begegnet sind: Antoine Pesne und insbesondere Daniel Nikolaus Chodowiecki - Bilder, die bereits der Mythenbildung um den Preußenkönig dienten. Historische und aktuelle Themen sind in Menzels Werk aufs Anschaulichste miteinander verwoben und so schließt die Ausstellung mit Darstellungen seiner Gegenwart. Präsentes wie Vergangenes erfasst Menzel mit gleicher Eindringlichkeit, mit allem Flüchtigen und Zufälligen des Lebens, bei größter Genauigkeit im Detail.",
                "press_text_en": "",
                "catalog_de": "",
                "catalog_en": "",
                "catalog_ordering_de": "",
                "catalog_ordering_en": "",
                "website_de": "http://www.smb.museum/smb/kalender/details.php?objID=33824",
                "website_en": "http://www.smb.museum/smb/kalender/details.php?objID=33824",
                "start": "2012-03-23",
                "end": "2012-06-24",
                "vernissage": null,
                "finissage": null,
                "exhibition_extended": false,
                "permanent": false,
                "museum_id": 12,
                "location_name": "",
                "street_address": "",
                "street_address2": "",
                "postal_code": "",
                "city": "Berlin",
                "country": "de",
                "latitude": 52.520719,
                "longitude": 13.398495,
                "other_locations_de": "",
                "other_locations_en": "",
                "organizers": [
                    {
                       "organizing_museum_id": 12,
                       "organizer_title": "",
                       "organizer_url_link": ""
                    }
                ],
                "museum_prices": false,
                "free_entrance": false,
                "admission_price": "8.00",
                "admission_price_info_de": "",
                "admission_price_info_en": "",
                "reduced_price": "5.00",
                "reduced_price_info_de": "",
                "reduced_price_info_en": "",
                "museum_opening_hours": false,
                "seasons": [
                    {
                        "is_appointment_based": false,
                        "is_open_24_7": false,
                        "mon_open": null,
                        "mon_break_close": null,
                        "mon_break_open": null,
                        "mon_close": null,
                        "tue_open": "10:00",
                        "tue_break_close": null,
                        "tue_break_open": null,
                        "tue_close": "18:00",
                        "wed_open": "10:00"
                        "wed_break_close": null,
                        "wed_break_open": null,
                        "wed_close": "18:00",
                        "thu_open": "10:00",
                        "thu_break_close": null,
                        "thu_break_open": null,
                        "thu_close": "20:00",
                        "fri_open": "10:00",
                        "fri_break_close": null,
                        "fri_break_open": null,
                        "fri_close": "18:00",
                        "sat_open": "10:00",
                        "sat_break_close": null,
                        "sat_break_open": null,
                        "sat_close": "18:00",
                        "sun_open": "10:00",
                        "sun_break_close": null,
                        "sun_break_open": null,
                        "sun_close": "18:00",
                        "exceptions_de": "",
                        "exceptions_en": "",
                        "last_entry_de": "",
                        "last_entry_en": "",
                    }
                ],
                "suitable_for_disabled": true,
                "suitable_for_disabled_info_de": "",
                "suitable_for_disabled_info_en": "",
                "is_for_children": false,
                "media_files": [
                    {
                        "created": "2013-02-20T22:28:45",
                        "modified": null,
                        "url": "http://yourwebsite.de/media/exhibitions/den-alten-fritz-der-im-volke-lebt-das-bild-friedrichs-des-grossen-bei-adolph-menzel/menzel_floetenkonzert.jpg"
                        "title_de": "Menzel Flötenkonzert",
                        "title_en": ""
                        "description_de": "",
                        "description_en": "",
                        "author": ""
                    }
                ]
            },
            ...
        ]
    }

In addition, you can pass a list of exhibition categories with IDs and titles. We need to know the full list of categories at your website, so that we could map them correctly to the categories at  Museumsportal.

## Events ##

Events happen at museums one or more times. We expect this data for **events**:

Field |	Type |	Description
---|---|---
id |	integer |	Unique identifier
created |	string |	Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"
modified |	string |	Modification date and time in a format "yyyy-mm-ddThh:mm:ss"
title\_de |	string |	Title in German
title\_en |	string |	Title in English
subtitle\_de |	string |	Subtitle in German
subtitle\_en |	string |	Subtitle in English
press\_text\_de | string | Press text in German
press\_text\_en | string | Press text in English
event\_type\_de |	string |	Event type in German
event\_type\_en |	string |	Event type in English
website\_de |	string |	The URL of the event at your website in German
website\_en |	string |	The URL of the event at your website in English
event\_times |	list |	List of event times
museum\_id |	integer |	The ID of the museum
location\_name |	string |	Location name, when differs from museum
street\_address |	string | Street address
street\_address2 |	string |	Second line of street address
postal\_code |	string |	Postal code
city |	string |	City
country |	string |	Country code e.g. "de"
latitude |	float |	Latitude
longitude |	float |	Longitude
meeting\_place\_de |	string |	Meeting place in German
meeting\_place\_en |	string |	Meeting place in English
organizers |	list |	List of organizers
exhibition\_id |	integer |	The ID of the related exhibition
languages |	list |	List of language codes
free\_admission |	boolean |	Is the admission free?
admission\_price |	string |	Admission price in Euros, e.g. "12.00"
admission\_price\_info\_de |	string |	Admission price information in German
admission\_price\_info\_en |	string |	Admission price information in English
reduced\_price |	string |	Reduced admission price in Euros e.g. "8.00"
booking\_info\_de |	string |	Booking information in German
booking\_info\_en |	string |	Booking information in English
media\_files |	list |	List of media files

The **event_times** should have these fields:

Field |	Type |	Description
---|---|---
event\_date |	string |	Event date in a format "yyyy-mm-dd"
start |	string |	Start time in a format "hh:mm"
end |	string |	End tine in a format "hh:mm"

Event **organizers** should have these fields:

Field |	Type |	Description
---|---|---
organizing\_museum\_id |	string | Unique identifier of a museum
organizer\_title |	string |	Organizer title if not organized by a museum
organizer\_url\_link |	string |	Organizer URL if not organized by a museum

Event **media_files** should have these fields:

Field |	Type |	Description
---|---|---
created | string |	Creation date and time in a format "yyyy-mm-ddThh:mm:ss"
modified |	string |	Modification date and time in a format "yyyy-mm-ddThh:mm:ss"
url |	string |	High-quality image URL
title\_de |	string |	Title in German
title\_en |	string |	Title in English
description\_de |	string |	Description in German
description\_en |	string |	Description in English
author |	string |	Author and Copyright

So when accessed by **http://yourwebsite.de/api/events/?api_key=abc123** or similar path, we should get information about events in the following JSON format:

    {
        "meta": {
            "page": 1,
            "total_pages": 9,
            "total_count": 521
        },
        "objects": [
            {
                "id": 123,
                "created": "2014-02-04T15:02:14",
                "modified": "2014-07-01T11:27:05",
                "title_de": "\"Ágnes: Wir müssen uns öffnen, damit etwas bleibt\" und \"Ágnes: Es hat sich gelohnt, so lange zu leben\"",
                "title_en": "",
                "subtitle_de": "Filme von Helmuth Bauer und Lea-Rosa Lambeck sowie Astrid Schomäcker, 2004",
                "subtitle_en": "",
                "press_text_de": "Deutsche und ungarische Jugendliche begleiteten Ágnes Bartha, eine enge Freundin von Edith Kiss, die das selbe Schicksal erleiden musste,2002 an die Orte ihrer Kindheit und Jugend in Ungarn und auf dem Weg, den sie im Herbst 1944 bei ihrer Deportation ins Frauen-Konzentrationslager Ravensbrück zurücklegen musste. In Ravensbrück, in der Genshagener Heide bei Ludwigsfelde und auf der Todesmarschstrecke erzählt sie den „Urenkeln“ ihre Geschichte von KZ-Haft und Zwangsarbeit für Daimler-Benz.",
                "press_text_en": "",
                "event_type_de": "",
                "event_type_en": "",
                "website_de": "http://www.fhxb-museum.de/index.php?id=19",
                "website_en": ""
                "event_times": [
                    {
                        "event_date": "2014-03-19",
                        "start": "19:00"
                        "end": null,
                    }
                ],
                "museum_id": 12,
                "location_name": "FHXB Friedrichshain-Kreuzberg Museum",
                "street_address": "Adalbertstraße 95A",
                "street_address2": "",
                "postal_code": "10999",
                "city": "Berlin",
                "country": "de",
                "latitude": 52.500024,
                "longitude": 13.417633,
                "meeting_place_de": "Dachetage FHXB Museum",
                "meeting_place_en": "",
                "organizers": [],
                "exhibition_id": 123,
                "languages": [
                    "de"
                ],
                "free_admission": true,
                "admission_price": null,
                "admission_price_info_de": "",
                "admission_price_info_en": "",
                "reduced_price": null,
                "booking_info_de": "",
                "booking_info_en": "",
                "media_files": [
                    {
                        "created": "2014-02-04T15:21:06",
                        "modified_date": "2014-02-04T15:21:06",
                        "url": "http://yourwebsite.de/media/events/agnes-wir-mussen-uns-offnen-damit-etwas-bleibt-und-agnes-es-hat-sich-gelohnt-so-lange-zu-leben/20140204152106.png"
                        "title_de": "Ágnes Bartha (li) mit Frieda Malter, April 2001",
                        "title_en": "",
                        "description_de": "Ágnes Bartha (li) mit Frieda Malter, April 2001 ",
                        "description_en": "",
                        "author": "http://www.gesichter-der-zwangsarbeit.de",
                        "copyright_limitations": ""
                    }
                ]
            },
            ...
        ]
    }


In addition, you can pass a list of event categories with IDs and titles. We need to know the full list of categories at your website, so that we could map them correctly to the categories at  Museumsportal.

## Workshops (guided tours) ##

Like events, workshops happen at museums one or more times. We expect this data from **workshops**:

Field |	Type |	Description
---|---|---
id |	integer |	Unique identifier
created |	string |	Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"
modified |	string |	Modification date and time in a format "yyyy-mm-ddThh:mm:ss"
title\_de |	string |	Title in German
title\_en |	string | Title in English
subtitle\_de |	string |	Subtitle in German
subtitle\_en |	string |	Subtitle in English
press\_text\_de | string | Press text in German
press\_text\_en | string | Press text in English
workshop\_type\_de |	string |	Workshop type in German
workshop\_type\_en |	string |	Workshop type in English
website\_de |	string |	External website in German
website\_en |	string |	External website in English
workshop\_times |	list |	List of workshop times
museum\_id |	integer |	The ID of the museum
location\_name |	string |	Location name, when differs from museum
street\_address |	string | Street address
street\_address2 |	string |	Second line of street address
postal\_code |	string |	Postal code
city |	string |	City
country |	string |	Country code e.g. "de"
latitude |	float |	Latitude
longitude |	float |	Longitude
meeting\_place\_de |	string |	Meeting place in German
meeting\_place\_en |	string |	Meeting place in English
organizers |	list |	List of organizers
exhibition\_id |	integer |	The ID of the related exhibition
languages |	list |	List of language codes
free\_admission |	boolean |	Is the admission free?
admission\_price |	string |	Admission price in Euros, e.g. "12.00"
admission\_price\_info\_de |	string |	Admission price information in German
admission\_price\_info\_en |	string |	Admission price information in English
reduced\_price |	string |	Reduced admission price in Euros e.g. "8.00"
booking\_info\_de |	string |	Booking information in German
booking\_info\_en |	string |	Booking information in English
has\_group\_offer |	boolean |	Has bookable group offer?
is\_for\_preschool |	boolean |	Is special for preschool children (up to 5 years)?
is\_for\_primary\_school |	boolean |	Is special for children of primary school age (6-12 years)?
is\_for\_youth |	boolean |	Is special for youth (aged 13 years)?
is\_for\_families |	boolean |	Is special for families?
is\_for\_wheelchaired |	boolean |	Is special for people in wheelchairs?
is\_for\_deaf |	boolean |	Is special for deaf people?
is\_for\_blind |	boolean |	Is special for blind people?
is\_for\_learning\_difficulties |	boolean |	Is special for people with learning difficulties?
media\_files |	list |	List of media files
types | list | List of types

The **workshop_times** should have these fields:

Field |	Type |	Description
---|---|---
workshop\_date |	string |	Workshop date in a format "yyyy-mm-dd"
start |	string |	Start time in a format "hh:mm"
end |	string |	End tine in a format "hh:mm"

Workshop **organizers** should have these fields:

Field |	Type |	Description
---|---|---
organizing\_museum\_id |	string | Unique identifier of a museum
organizer\_title |	string |	Organizer title if not organized by a museum
organizer\_url\_link |	string |	Organizer URL if not organized by a museum

Workshop **media_files** should have these fields:

Field |	Type |	Description
---|---|---
created | string |	Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"
modified |	string |	Modification date and time in a format "yyyy-mm-ddThh:mm:ss"
url |	string |	High-quality image URL
title\_de |	string |	Title in German
title\_en |	string |	Title in English
description\_de |	string |	Description in German
description\_en |	string |	Description in English
author |	string |	Author and Copyright

Workshop **types** will be matched to "Workshops" or "Guided Tours" at Museumsportal. Workshop **types** should have these fields:

Field |	Type |	Description
---|---|---
id |	string | Unique identifier of a type
title\_de |	string |	Title in German
title\_en |	string |	Title in English

So when accessed by **http://yourwebsite.de/api/workshops/?api_key=abc123** or similar path, we should get information about workshops and guided tours in the following JSON format:

    {
        "meta": {
            "page": 1,
            "total_pages": 9,
            "total_count": 521
        },
        "objects": [
            {
                "id": 123,
                "created": "2013-12-18T16:41:23",
                "modified": null,
                "title_de": "Napoleons Ritt über die Alpen, Sitzendorf, nach 1850",
                "title_en": "",
                "subtitle_de": "Familienführung",
                "subtitle_en": "",
                "press_text_de": "Das Deutsche Historische Museum bietet jeden Sonntag um 14 Uhr sowie in den Ferien ein Programm für Kinder und Familien abwechselnd in seinen Sonderausstellungen oder in der Dauerausstellung an. In der Ausstellung „1813 – Auf dem Schlachtfeld bei Leipzig“ schlüpfen Kinder ab 10 Jahren in die Rolle eines Reporters und decken auf, was bei Leipzig geschah und wie es dazu kam. Referenten geben Hilfestellung bei Personen und Hintergründen der Befreiungskriege und erläutern Objekte und Zusammenhänge altersgerecht. 10-14 Jahre",
                "press_text_en": "",
                "workshop_type_de": "",
                "workshop_type_en": ""                
                "website_de": "http://www.dhm.de/ausstellungen/auf-dem-schlachtfeld-bei-leipzig/fuehrungen.html",
                "website_en": "",
                "workshop_times": [
                    {
                        "workshop_date": "2013-10-12"
                        "start": "11:00",
                        "end": null,
                    },
                    {
                        "workshop_date": "2013-11-03"
                        "start": "14:00",
                        "end": null,
                    }
                ],
                "museum_id": 12,
                "location_name": "Deutsches Historisches Museum",
                "street_address": "Unter den Linden 2",
                "street_address2": "",
                "postal_code": "10117",
                "city": "Berlin",
                "country": "de",
                "latitude": 52.517687,
                "longitude": 13.396888,
                "meeting_place_de": "Ausstellungshalle",
                "meeting_place_en": "",
                "organizers": [],
                "exhibition_id": 123,
                "languages": [
                    "de",
                    "en"
                ],
                "free_admission": false,
                "admission_price": "2.00",
                "admission_price_info_de": "zzgl. Eintritt für Erwachsene, Familienkarte: 18€ (Eintritt und Führung für Erwachsene und max. 3 Kinder)",
                "admission_price_info_en": "",
                "reduced_price": null,
                "booking_info_de": "Alle Führungen frei Buchbar",
                "booking_info_en": "",
                "has_group_offer": false,
                "is_for_preschool": false,
                "is_for_primary_school": true,
                "is_for_youth": true,
                "is_for_families": true,
                "is_for_wheelchaired": false,
                "is_for_deaf": false,
                "is_for_blind": false,
                "is_for_learning_difficulties": false,
                "media_files": [
                    {
                        "created": "2013-12-18T16:12:10",
                        "modified": "2013-12-18T16:12:10",
                        "url": "http://yourwebsite.de/media/workshops/1813-kinderreporter-decken-auf-was-bei-leipzig-wirklich-geschah/20131218161210.jpg"
                        "title_de": "",
                        "title_en": "",
                        "description_de": "",
                        "description_en": "",
                        "author": "© Stiftung Deutsches Historisches Museum",
                    }
                ],
                "types": [
                    {
                        "id": 2,
                        "title_de": "Führung",
                        "title_en": "Guided tour"
                    }
                ]
            },
            ...
        ]
    }


In addition, you can pass a list of workshop categories with IDs and titles. We need to know the full list of categories at your website, so that we could map them correctly to the categories at  Museumsportal.
