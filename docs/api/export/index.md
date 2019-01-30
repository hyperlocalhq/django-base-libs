# Museumsportal Export API v2 Documentation

[TOC]

## Formats

All API uris can be accessed either in **JSON** or in **XML** formats. The format can be defined by query parameter `?format=json` or `?format=xml`

There are tools to browse JSON in a convenient way for Chrome and Firefox:  

Firefox - [https://addons.mozilla.org/en-US/firefox/addon/jsonview/  
](https://addons.mozilla.org/en-US/firefox/addon/jsonview/)

Chrome - [https://chrome.google.com/webstore/detail/chklaanhfefbnpoihckbnefhakgolnmc](https://chrome.google.com/webstore/detail/chklaanhfefbnpoihckbnefhakgolnmc)

## Authentication

To access the lists and details of database entries you will need to authenticate with your **username** and **API key** by query parameters, e.g. `?username=demo&api_key=123456789`

## The Highest Level of API

If you enter `/api/v2/?format=json` , you can see all available **list endpoints**:

    {
        accessibility_option: {
            list_endpoint: "/api/v2/accessibility_option/",
            schema: "/api/v2/accessibility_option/schema/"
        },
        event: {
            list_endpoint: "/api/v2/event/",
            schema: "/api/v2/event/schema/"
        },
        event_category: {
            list_endpoint: "/api/v2/event_category/",
            schema: "/api/v2/event_category/schema/"
        },
        event_media_file: {
            list_endpoint: "/api/v2/event_media_file/",
            schema: "/api/v2/event_media_file/schema/"
        },
        event_time: {
            list_endpoint: "/api/v2/event_time/",
            schema: "/api/v2/event_time/schema/"
        },
        exhibition: {
            list_endpoint: "/api/v2/exhibition/",
            schema: "/api/v2/exhibition/schema/"
        },
        exhibition_category: {
            list_endpoint: "/api/v2/exhibition_category/",
            schema: "/api/v2/exhibition_category/schema/"
        },
        exhibition_media_file: {
            list_endpoint: "/api/v2/exhibition_media_file/",
            schema: "/api/v2/exhibition_media_file/schema/"
        },
        exhibition_season: {
            list_endpoint: "/api/v2/exhibition_season/",
            schema: "/api/v2/exhibition_season/schema/"
        },
        museum: {
            list_endpoint: "/api/v2/museum/",
            schema: "/api/v2/museum/schema/"
        },
        museum_category: {
            list_endpoint: "/api/v2/museum_category/",
            schema: "/api/v2/museum_category/schema/"
        },
        museum_media_file: {
            list_endpoint: "/api/v2/museum_media_file/",
            schema: "/api/v2/museum_media_file/schema/"
        },
        museum_season: {
            list_endpoint: "/api/v2/museum_season/",
            schema: "/api/v2/museum_season/schema/"
        },
        museum_social_media_chanel: {
            list_endpoint: "/api/v2/museum_social_media_chanel/",
            schema: "/api/v2/museum_social_media_chanel/schema/"
        },
        museum_special_opening_time: {
            list_endpoint: "/api/v2/museum_special_opening_time/",
            schema: "/api/v2/museum_special_opening_time/schema/"
        },
        workshop: {
            list_endpoint: "/api/v2/workshop/",
            schema: "/api/v2/workshop/schema/"
        },
        workshop_category: {
            list_endpoint: "/api/v2/workshop_category/",
            schema: "/api/v2/workshop_category/schema/"
        },
        workshop_media_file: {
            list_endpoint: "/api/v2/workshop_media_file/",
            schema: "/api/v2/workshop_media_file/schema/"
        },
        workshop_time: {
            list_endpoint: "/api/v2/workshop_time/",
            schema: "/api/v2/workshop_time/schema/"
        }
    }

This object shows you how to access the list views of museums (`"/api/v2/museum/"`), exhibitions (`"/api/v2/exhibition/"`), events (`"/api/v2/event/"`), workshops (`"/api/v2/workshop/"`), and other objects.

## Getting the Collection of Entries

All entries in the lists are paginated by 1000 by default. If you want to paginate by smaller amount, you can set the query parameter `limit.`

If you enter the URI 

    /api/v2/exhibition/?format=json&username=demo&api_key=123456789&limit=2

you would get a list like this:

    {
        "meta": {
            "limit": 2,
            "next": "/api/v2/exhibition/?username=demo2&api_key=9b80e6f80b981fbb0da25f9bb006d78145d7c2c0&limit=2&offset=2&format=json",
            "offset": 0,
            "previous": null,
            "total_count": 281
        },
        "objects": [
            {
                "admission_price": null,
                "admission_price_info_de": "",
                "admission_price_info_en": "",
                "catalog_de": "",
                "catalog_en": "",
                "catalog_ordering_de": "",
                "catalog_ordering_en": "",
                "categories": [
                    {
                        "creation_date": "2012-09-10T17:09:52",
                        "id": 9,
                        "level": 1,
                        "lft": 8,
                        "modified_date": "2013-03-13T17:55:23",
                        "resource_uri": "/api/v2/exhibition_category/9/",
                        "rght": 9,
                        "title_de": "19\. Jahrhundert und Anfang 20\. Jahrhundert",
                        "title_en": "Art to 1900",
                        "tree_id": 3
                    }
                ],
                "city": "Berlin",
                "country": "de",
                "creation_date": "2012-06-14T13:41:01",
                "end": "2012-06-24",
                "exhibition_extended": false,
                "finissage": null,
                "free_entrance": false,
                "id": 13,
                "is_for_children": false,
                "latitude": null,
                "link_de": "http://www.museumsportal-berlin.de/de/ausstellungen/den-alten-fritz-der-im-volke-lebt-das-bild-friedrichs-des-grossen-bei-adolph-menzel/",
                "link_en": "http://www.museumsportal-berlin.de/en/exhibitions/den-alten-fritz-der-im-volke-lebt-das-bild-friedrichs-des-grossen-bei-adolph-menzel/",
                "location_name": "",
                "longitude": null,
                "media_files": [
                    {
                        "creation_date": "2013-02-20T22:28:45",
                        "id": 1,
                        "modified_date": null,
                        "resource_uri": "/api/v2/exhibition_media_file/1/",
                        "url": "http://www.museumsportal-berlin.de/media/exhibitions/den-alten-fritz-der-im-volke-lebt-das-bild-friedrichs-des-grossen-bei-adolph-menzel/menzel_floetenkonzert.jpg"
                    }
                ],
                "modified_date": "2013-04-17T17:35:19",
                "museum": "/api/v2/museum/8/",
                "museum_opening_hours": false,
                "museum_prices": false,
                "organizers": [],
                "other_locations_de": "",
                "other_locations_en": "",
                "permanent": false,
                "postal_code": "",
                "press_text_de": "Die Sammlungen der Nationalgalerie und des Kupferstichkabinetts besitzen einen Großteil der malerischen und grafischen Arbeiten, die der junge Adolph Menzel (1815-1905) mit Begeisterung und großer Detailtreue zum Leben Friedrichs des Großen geschaffen hat. Dazu gehören neben Bildern hunderte Studien, Probedrucke und Holzstöcke zu den großen Illustrationsfolgen des Künstlers.\r\nAm populärsten wurden die fast 400 Holzstiche zur 1840 erschienenen \"Geschichte Friedrichs des Großen\" von Franz Kugler. Mit dieser Arbeit hatte Menzel nicht nur ein enormes Detailwissen erworben, sondern ein Bild des Monarchen entwickelt, das er in den folgenden Jahren in einer Reihe von Gemälden variierte, die, bis auf drei Kriegsverluste, erstmals zusammen in der Ausstellung präsentiert werden. Sie zeigen Friedrich II. als aufgeklärten Monarchen, als willensstarken Kriegsherrn, als Freund der Philosophie und der Künste - eine bürgerliche Rezeption Friedrichs und damals ein Modell für die Gegenwart.\r\nVorangestellt ist der Ausstellung ein Kapitel, das sich den Darstellungen Friedrichs des Großen durch Künstler widmet, die ihm noch persönlich begegnet sind: Antoine Pesne und insbesondere Daniel Nikolaus Chodowiecki - Bilder, die bereits der Mythenbildung um den Preußenkönig dienten. Historische und aktuelle Themen sind in Menzels Werk aufs Anschaulichste miteinander verwoben und so schließt die Ausstellung mit Darstellungen seiner Gegenwart. Präsentes wie Vergangenes erfasst Menzel mit gleicher Eindringlichkeit, mit allem Flüchtigen und Zufälligen des Lebens, bei größter Genauigkeit im Detail.",
                "press_text_en": "",
                "reduced_price": null,
                "reduced_price_info_de": "",
                "reduced_price_info_en": "",
                "resource_uri": "/api/v2/exhibition/13/",
                "seasons": [
                    {
                        "exceptions_de": "",
                        "exceptions_en": "",
                        "fri_break_close": null,
                        "fri_break_open": null,
                        "fri_close": "18:00:00",
                        "fri_open": "10:00:00",
                        "id": 18,
                        "is_appointment_based": false,
                        "is_open_24_7": false,
                        "last_entry_de": "",
                        "last_entry_en": "",
                        "mon_break_close": null,
                        "mon_break_open": null,
                        "mon_close": null,
                        "mon_open": null,
                        "resource_uri": "/api/v2/exhibition_season/18/",
                        "sat_break_close": null,
                        "sat_break_open": null,
                        "sat_close": "18:00:00",
                        "sat_open": "10:00:00",
                        "sun_break_close": null,
                        "sun_break_open": null,
                        "sun_close": "18:00:00",
                        "sun_open": "10:00:00",
                        "thu_break_close": null,
                        "thu_break_open": null,
                        "thu_close": "20:00:00",
                        "thu_open": "10:00:00",
                        "tue_break_close": null,
                        "tue_break_open": null,
                        "tue_close": "18:00:00",
                        "tue_open": "10:00:00",
                        "wed_break_close": null,
                        "wed_break_open": null,
                        "wed_close": "18:00:00",
                        "wed_open": "10:00:00"
                    }
                ],
                "start": "2012-03-23",
                "status": "expired",
                "street_address": "",
                "street_address2": "",
                "subtitle_de": "Das Bild Friedrichs des Großen bei Adolph Menzel",
                "subtitle_en": "Das Bild Friedrichs des Großen bei Adolph Menzel",
                "suitable_for_disabled": false,
                "suitable_for_disabled_info_de": "",
                "suitable_for_disabled_info_en": "",
                "title_de": "\"... den alten Fritz, der im Volke lebt\"",
                "title_en": "\"... den alten Fritz, der im Volke lebt\"",
                "vernissage": null,
                "website_de": "http://www.smb.museum/smb/kalender/details.php?objID=33824",
                "website_en": "http://www.smb.museum/smb/kalender/details.php?objID=33824"
            },
            {
                "admission_price": null,
                "admission_price_info_de": "",
                "admission_price_info_en": "",
                "catalog_de": "",
                "catalog_en": "",
                "catalog_ordering_de": "",
                "catalog_ordering_en": "",
                "categories": [
                    {
                        "creation_date": "2012-09-10T17:10:17",
                        "id": 11,
                        "level": 0,
                        "lft": 1,
                        "modified_date": null,
                        "resource_uri": "/api/v2/exhibition_category/11/",
                        "rght": 2,
                        "title_de": "Naturwissenschaft und Technik",
                        "title_en": "Science and Technology",
                        "tree_id": 7
                    },
                    {
                        "creation_date": "2012-09-10T17:09:37",
                        "id": 8,
                        "level": 0,
                        "lft": 1,
                        "modified_date": "2013-02-28T18:22:53",
                        "resource_uri": "/api/v2/exhibition_category/8/",
                        "rght": 16,
                        "title_de": "Geschichte, Kulturgeschichte",
                        "title_en": "Cultural History",
                        "tree_id": 9
                    },
                    {
                        "creation_date": "2012-09-10T17:08:33",
                        "id": 4,
                        "level": 1,
                        "lft": 2,
                        "modified_date": "2013-03-14T20:10:18",
                        "resource_uri": "/api/v2/exhibition_category/4/",
                        "rght": 3,
                        "title_de": "Berlingeschichte",
                        "title_en": "Berlin History",
                        "tree_id": 9
                    },
                    {
                        "creation_date": "2013-03-01T13:54:03",
                        "id": 19,
                        "level": 1,
                        "lft": 6,
                        "modified_date": "2013-03-14T20:10:27",
                        "resource_uri": "/api/v2/exhibition_category/19/",
                        "rght": 7,
                        "title_de": "Nationalsozialismus",
                        "title_en": "",
                        "tree_id": 9
                    }
                ],
                "city": "Berlin",
                "country": "de",
                "creation_date": "2013-02-14T12:16:01",
                "end": "2013-09-27",
                "exhibition_extended": false,
                "finissage": null,
                "free_entrance": false,
                "id": 267,
                "is_for_children": false,
                "latitude": 52.586305000000003,
                "link_de": "http://www.museumsportal-berlin.de/de/ausstellungen/der-reichstag-brennt/",
                "link_en": "http://www.museumsportal-berlin.de/en/exhibitions/der-reichstag-brennt/",
                "location_name": "",
                "longitude": 13.286204,
                "media_files": [
                    {
                        "author": "",
                        "copyright_limitations": "",
                        "creation_date": "2013-02-20T22:28:45",
                        "description_de": "",
                        "description_en": "",
                        "id": 2,
                        "modified_date": "2013-04-12T18:30:22",
                        "resource_uri": "/api/v2/exhibition_media_file/2/",
                        "title_de": "",
                        "title_en": "",
                        "url": "http://www.museumsportal-berlin.de/media/exhibitions/der-reichstag-brennt/sonderausstellungreichstag.jpg"
                    }
                ],
                "modified_date": "2013-04-17T17:35:19",
                "museum": "/api/v2/museum/63/",
                "museum_opening_hours": false,
                "museum_prices": false,
                "organizers": [],
                "other_locations_de": "",
                "other_locations_en": "",
                "permanent": false,
                "postal_code": "13507",
                "press_text_de": "Am 27\. Februar 2013 jährt sich die Brandstiftung im Reichstagsgebäude zum 80\. Male. Aus diesem Anlass wird vom 27\. Februar bis zum 27\. September 2013 im Feuerwehrmuseum eine Sonderausstellung gezeigt.Der Reichstagsbrand ist in der Geschichte der Berliner Feuerwehr wohl der Einsatz, der die weltweit größten Folgen nach sich zog. Gleichzeitig gibt es wohl auch keinen anderen Brand der achtzig Jahre später noch derart die Gemüter bewegt um die Frage, wer diesen Brand gelegt hat. In der juristischen und historischen Nachbetrachtung dieses Ereignisses wurde der Feuerwehreinsatz als solcher aber auch die Rolle der Feuerwehr und ihrer Führungskräfte bei diesem Ereignis bislang meist nur am Rande betrachtet.Mit der Ausstellung zum Reichstagsbrand im Feuerwehrmuseum sollen diese Aspekte beleuchtet werden. Damit möchte die Berliner Feuerwehr einen Beitrag zur geschichtlichen Aufarbeitung dieses Ereignisses leisten und dabei auch ihre eigene Rolle kritisch reflektieren. Gleichzeitig soll der Versuch unternommen werden, dieses Thema insbesondere jüngeren Menschen, die das Feuerwehrmuseum jährlich in großer Zahl besuchen, zu vermitteln.\r\nEine Ausstellung im Rahmen des Themenjahres 2013 \"Zerstörte Vielfalt\".",
                "press_text_en": "",
                "reduced_price": null,
                "reduced_price_info_de": "",
                "reduced_price_info_en": "",
                "resource_uri": "/api/v2/exhibition/267/",
                "seasons": [
                    {
                        "exceptions_de": "",
                        "exceptions_en": "",
                        "fri_break_close": null,
                        "fri_break_open": null,
                        "fri_close": "14:00:00",
                        "fri_open": "10:00:00",
                        "id": 514,
                        "is_appointment_based": false,
                        "is_open_24_7": false,
                        "last_entry_de": "30 Min. vor Schließung",
                        "last_entry_en": "30 Min. vor Schließung",
                        "mon_break_close": null,
                        "mon_break_open": null,
                        "mon_close": null,
                        "mon_open": null,
                        "resource_uri": "/api/v2/exhibition_season/514/",
                        "sat_break_close": null,
                        "sat_break_open": null,
                        "sat_close": "14:00:00",
                        "sat_open": "10:00:00",
                        "sun_break_close": null,
                        "sun_break_open": null,
                        "sun_close": null,
                        "sun_open": null,
                        "thu_break_close": null,
                        "thu_break_open": null,
                        "thu_close": "16:00:00",
                        "thu_open": "09:00:00",
                        "tue_break_close": null,
                        "tue_break_open": null,
                        "tue_close": "16:00:00",
                        "tue_open": "09:00:00",
                        "wed_break_close": null,
                        "wed_break_open": null,
                        "wed_close": "19:00:00",
                        "wed_open": "09:00:00"
                    }
                ],
                "start": "2013-02-27",
                "status": "published",
                "street_address": "Veitstraße 5",
                "street_address2": "",
                "subtitle_de": "",
                "subtitle_en": "",
                "suitable_for_disabled": false,
                "suitable_for_disabled_info_de": "",
                "suitable_for_disabled_info_en": "",
                "title_de": "\"Der Reichstag brennt!\"",
                "title_en": "\"Der Reichstag brennt!\"",
                "vernissage": null,
                "website_de": "http://www.feuerwehrmuseum-berlin.de/aktuell/index.html",
                "website_en": "http://www.feuerwehrmuseum-berlin.de/aktuell/index.html"
            }
        ]
    }

The `meta` section shows pagination options. The `objects` section lists exhibitions.

## Filtering

You can filter lists of museums, exhibitions, events, and workshops by creation date, modification date, both, status, or category. For example, 

Exhibitions **created** since September 1, 2012:

    /api/v2/exhibition/?format=json&username=demo&api_key=123456789&creation_date__gte=2012-09-01

Exhibitions **modified** since September 1, 2012:

    /api/v2/exhibition/?format=json&username=demo&api_key=123456789&modified_date__gte=2012-09-01

Exhibitions **created** or **modified** since September 1, 2012:

    /api/v2/exhibition/?format=json&username=demo&api_key=123456789&created_or_modified_since=2012-09-01

Exhibitions **created** or **modified** since September 1, 2012 with the **status** "published":

`/api/v2/exhibition/?format=json&username=demo&api_key=123456789&created_or_modified_since=2012-09-01&status=published`

Exhibitions with the **category** "Architecture, Arts and Crafts":

    /api/v2/exhibition/?format=json&username=demo&api_key=123456789&categories=1

Exhibitions with the **category** "Architecture, Arts and Crafts" (id=1) with the **status** "expired":

    /api/v2/exhibition/?format=json&username=demo&api_key=123456789&categories=1&status=expired

## Getting the Details of an Entry

Each entry object has `resource_uri` which points to the uri having the detail information about the entry.

For example if you access

    /api/v2/exhibition/99/?format=json&username=demo&api_key=123456789

you would get this object:

    {
        "admission_price": null,
        "admission_price_info_de": "",
        "admission_price_info_en": "",
        "catalog_de": "",
        "catalog_en": "",
        "catalog_ordering_de": "",
        "catalog_ordering_en": "",
        "categories": [
            {
                "creation_date": "2012-09-10T17:07:04",
                "id": 1,
                "level": 0,
                "lft": 1,
                "modified_date": "2013-03-13T17:43:19",
                "resource_uri": "/api/v2/exhibition_category/1/",
                "rght": 2,
                "title_de": "Architektur, Kunstgewerbe, Design",
                "title_en": "Architecture, Applied Arts and Crafts",
                "tree_id": 1
            }
        ],
        "city": "Berlin",
        "country": "de",
        "creation_date": "2012-08-20T16:11:57",
        "end": "2012-09-03",
        "exhibition_extended": false,
        "finissage": null,
        "free_entrance": false,
        "id": 99,
        "is_for_children": false,
        "latitude": null,
        "link_de": "http://www.museumsportal-berlin.de/de/ausstellungen/5-recyclingdesignpreis-2012/",
        "link_en": "http://www.museumsportal-berlin.de/en/exhibitions/5-recyclingdesignpreis-2012/",
        "location_name": "",
        "longitude": null,
        "media_files": [
            {
                "creation_date": "2013-02-20T22:28:45",
                "id": 14,
                "modified_date": null,
                "resource_uri": "/api/v2/exhibition_media_file/14/",
                "url": "http://www.museumsportal-berlin.de/media/exhibitions/5-recyclingdesignpreis-2012/outsiders_volvox_1.jpg"
            }
        ],
        "modified_date": "2013-04-17T17:35:19",
        "museum": "/api/v2/museum/196/",
        "museum_opening_hours": false,
        "museum_prices": false,
        "organizers": [],
        "other_locations_de": "",
        "other_locations_en": "",
        "permanent": false,
        "postal_code": "",
        "press_text_de": "Das Museum der Dinge zeigt vom 6\. Juli 2012 bis 3\. September 2012 eine Auswahl von den 2012 prämierten Objekten des 5\. RecyclingDesignpreis, der vom Arbeitskreis Recycling e.V./ RecyclingBörse! Herford ausgelobt wird.\r\nGewinner des mit 2.500 Euro dotierten deutschen RecyclingDesignpreises 2012 sind Lea Gerber und Samuel Coendet. Die Jury zeichnet die Schweizer Designer für ihre Secondhand-Stofftiere \"Outsiders\" aus. Den dritten Platz teilen sich die Münchnerin Waltraud Münzhuber für \"Verwebe deinen Lieblingsfilm\" (ein Papierkorb aus alten Video- oder Tonbändern) und Silke Koch für skulpturale Objekte aus Porzellan, Glas, Plastik, Metall mit dem Titel \"After Gravity's Rainbow\".Am Wettbewerb beteiligten sich über 600 Designer/innen. Neben 350 Bewerbungen aus Deutschland kamen Beiträge aus 35 Ländern. Unter anderem aus Belgien, Brasilien, China, Martinique, Nepal, Österreich, Polen, Spanien, Taiwan, USA. Das Spektrum der eingereichten und ausgestellten ReDesign-Entwicklungen reicht von Mode- und Deko-Accessoires über Kleidung bis zu Möbeln.\r\nMotto des RecyclingDesignpreises, der sich als einziger Wettbewerb zur Förderung der Ressourcenschonung und CO2-Vermeidung in der Produktentwicklung versteht, ist es, den \"verborgenen Sinn weggeworfener Dinge\" zu entdecken und nutzbar zu machen. Gefordert sind Entwicklungen aus industriellen oder handwerklichen Produktionsrückständen, aus Materialien vom Sperrmüll oder vom \"Schrott\".",
        "press_text_en": "",
        "reduced_price": null,
        "reduced_price_info_de": "",
        "reduced_price_info_en": "",
        "resource_uri": "/api/v2/exhibition/99/",
        "seasons": [
            {
                "exceptions_de": "",
                "exceptions_en": "",
                "fri_break_close": null,
                "fri_break_open": null,
                "fri_close": "19:00:00",
                "fri_open": "12:00:00",
                "id": 31,
                "is_appointment_based": false,
                "is_open_24_7": false,
                "last_entry_de": "",
                "last_entry_en": "",
                "mon_break_close": null,
                "mon_break_open": null,
                "mon_close": "19:00:00",
                "mon_open": "12:00:00",
                "resource_uri": "/api/v2/exhibition_season/31/",
                "sat_break_close": null,
                "sat_break_open": null,
                "sat_close": "19:00:00",
                "sat_open": "12:00:00",
                "sun_break_close": null,
                "sun_break_open": null,
                "sun_close": "19:00:00",
                "sun_open": "12:00:00",
                "thu_break_close": null,
                "thu_break_open": null,
                "thu_close": null,
                "thu_open": null,
                "tue_break_close": null,
                "tue_break_open": null,
                "tue_close": null,
                "tue_open": null,
                "wed_break_close": null,
                "wed_break_open": null,
                "wed_close": null,
                "wed_open": null
            }
        ],
        "start": "2012-07-06",
        "status": "expired",
        "street_address": "",
        "street_address2": "",
        "subtitle_de": "",
        "subtitle_en": "",
        "suitable_for_disabled": false,
        "suitable_for_disabled_info_de": "",
        "suitable_for_disabled_info_en": "",
        "title_de": "5\. RecyclingDesignpreis 2012",
        "title_en": "5\. RecyclingDesignpreis 2012",
        "vernissage": null,
        "website_de": "http://www.museumderdinge.de/programm/ausstellungen/",
        "website_en": "http://www.museumderdinge.de/programm/ausstellungen/"
    }


## Fields for each Type

### Categories

**Museum categories**, **exhibition categories**, and **event categories** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>

Title in English

</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the category</td>

</tr>

</tbody>

</table>

### Museums

**Museums** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>

Title in English

</td>

</tr>

<tr>

<td>subtitle_de</td>

<td>string</td>

<td>Subtitle in German</td>

</tr>

<tr>

<td>subtitle_en</td>

<td>string</td>

<td>Subtitle in English</td>

</tr>

<tr>

<td>street_address</td>

<td>string</td>

<td>

Street address

</td>

</tr>

<tr>

<td>street_address2</td>

<td>string</td>

<td>Second line of street address</td>

</tr>

<tr>

<td>postal_code</td>

<td>string</td>

<td>Postal code</td>

</tr>

<tr>

<td>city</td>

<td>string</td>

<td>City</td>

</tr>

<tr>

<td>country</td>

<td>string</td>

<td>Country code e.g. "de"</td>

</tr>

<tr>

<td>latitude</td>

<td>float</td>

<td>Latitude</td>

</tr>

<tr>

<td>longitude</td>

<td>float</td>

<td>Longitude</td>

</tr>

<tr>

<td>email</td>

<td>string</td>

<td>Email</td>

</tr>

<tr>

<td>website</td>

<td>string</td>

<td>External website</td>

</tr>

<tr>

<td>phone</td>

<td>list of strings</td>

<td>Country code, area code, and number of the phone</td>

</tr>

<tr>

<td>fax</td>

<td>list of strings</td>

<td>Country code, area code, and number of the fax</td>

</tr>

<tr>

<td>group_bookings_phone</td>

<td>list of strings</td>

<td>Country code, area code, and number of the group-bookings phone</td>

</tr>

<tr>

<td>service_phone</td>

<td>list of strings</td>

<td>Country code, area code, and number of the service phone</td>

</tr>

<tr>

<td>social_media_channels</td>

<td>list</td>

<td>List of social media channel objects</td>

</tr>

<tr>

<td>open_on_mondays</td>

<td>boolean</td>

<td>Is it open on Mondays?</td>

</tr>

<tr>

<td>free_entrance</td>

<td>boolean</td>

<td>Is the entrance free?</td>

</tr>

<tr>

<td>admission_price</td>

<td>string</td>

<td>Admission price in Euros, e.g. "12.00"</td>

</tr>

<tr>

<td>admission_price_info_de</td>

<td>string</td>

<td>Admission price information in German</td>

</tr>

<tr>

<td>admission_price_info_en</td>

<td>string</td>

<td>Admission price information in English</td>

</tr>

<tr>

<td>reduced_price</td>

<td>string</td>

<td>Reduced admission price in Euros e.g. "8.00"</td>

</tr>

<tr>

<td>reduced_price_info_de</td>

<td>string</td>

<td>Reduced admission price information in German</td>

</tr>

<tr>

<td>reduced_price_info_en</td>

<td>string</td>

<td>Reduced admission price information in English</td>

</tr>

<tr>

<td>show_family_ticket</td>

<td>boolean</td>

<td>Has family ticket?</td>

</tr>

<tr>

<td>show_group_ticket</td>

<td>boolean</td>

<td>Has group ticket?</td>

</tr>

<tr>

<td>group_ticket_de</td>

<td>string</td>

<td>Group ticket information in German</td>

</tr>

<tr>

<td>group_ticket_en</td>

<td>string</td>

<td>Group ticket information in English</td>

</tr>

<tr>

<td>show_yearly_ticket</td>

<td>boolean</td>

<td>Has yearly ticket</td>

</tr>

<tr>

<td>member_of_museumspass</td>

<td>boolean</td>

<td>Is this museum a member of Museumspass?</td>

</tr>

<tr>

<td>service_shop</td>

<td>boolean</td>

<td>Has shop?</td>

</tr>

<tr>

<td>service_restaurant</td>

<td>boolean</td>

<td>Has restaurant?</td>

</tr>

<tr>

<td>service_cafe</td>

<td>boolean</td>

<td>Has cafe?</td>

</tr>

<tr>

<td>service_library</td>

<td>boolean</td>

<td>Has library?</td>

</tr>

<tr>

<td>service_archive</td>

<td>boolean</td>

<td>Has archive?</td>

</tr>

<tr>

<td>service_diaper_changing_table</td>

<td>boolean</td>

<td>Has diaper changing table?</td>

</tr>

<tr>

<td>has_audioguide</td>

<td>boolean</td>

<td>Has audioguides?</td>

</tr>

<tr>

<td>has_audioguide_de</td>

<td>boolean</td>

<td>Has audioguide in German?</td>

</tr>

<tr>

<td>has_audioguide_en</td>

<td>boolean</td>

<td>Has audioguide in English?</td>

</tr>

<tr>

<td>has_audioguide_fr</td>

<td>boolean</td>

<td>Has audioguide in French?</td>

</tr>

<tr>

<td>has_audioguide_it</td>

<td>boolean</td>

<td>Has audioguide in Italian?</td>

</tr>

<tr>

<td>has_audioguide_sp</td>

<td>boolean</td>

<td>Has audioguide in Spanish?</td>

</tr>

<tr>

<td>has_audioguide_pl</td>

<td>boolean</td>

<td>Has audioguide in Polish?</td>

</tr>

<tr>

<td>has_audioguide_tr</td>

<td>boolean</td>

<td>Has audioguide in Turkish?</td>

</tr>

<tr>

<td>audioguide_other_languages</td>

<td>string</td>

<td>Other audioguide languages</td>

</tr>

<tr>

<td>has_audioguide_for_children</td>

<td>boolean</td>

<td>Has audioguide for children?</td>

</tr>

<tr>

<td>has_audioguide_for_learning_difficulties</td>

<td>boolean</td>

<td>Has audioguide for people with learning difficulties?</td>

</tr>

<tr>

<td>accessibility_options</td>

<td>list</td>

<td>List of accessibility options</td>

</tr>

<tr>

<td>accessibility_de</td>

<td>string</td>

<td>Accessibility information in German</td>

</tr>

<tr>

<td>accessibility_en</td>

<td>string</td>

<td>Accessibility information in English</td>

</tr>

<tr>

<td>mobidat_de</td>

<td>string</td>

<td>Mobidat information in German</td>

</tr>

<tr>

<td>mobidat_en</td>

<td>string</td>

<td>Mobidat information in English</td>

</tr>

<tr>

<td>seasons</td>

<td>list</td>

<td>List of season objects</td>

</tr>

<tr>

<td>special_opening_times</td>

<td>list</td>

<td>List of special-opening-time objects</td>

</tr>

<tr>

<td>media_files</td>

<td>list</td>

<td>List of media file objects</td>

</tr>

<tr>

<td>status</td>

<td>string</td>

<td>Status having one of these values: "draft", "published", "not_listed", "import", "trashed"</td>

</tr>

<tr>

<td>categories</td>

<td>list</td>

<td>List of category objects</td>

</tr>

<tr>

<td>link_de</td>

<td>string</td>

<td>The URL of the museum at http://www.museumsportal-berlin.de/ in German</td>

</tr>

<tr>

<td>link_en</td>

<td>string</td>

<td>The URL of the museum at http://www.museumsportal-berlin.de/ in English</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the museum</td>

</tr>

</tbody>

</table>

**Social media channels **have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>channel_type</td>

<td>string</td>

<td>Chanel type, e.g. "Facebook" or "Twitter"</td>

</tr>

<tr>

<td>url</td>

<td>string</td>

<td>URL of the media channel account</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the social media channel</td>

</tr>

</tbody>

</table>

**Accessibility options** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>Title in English</td>

</tr>

<tr>

<td>resoucre_uri</td>

<td>string</td>

<td>Endpoint to the details of the accessibility option</td>

</tr>

</tbody>

</table>

**Seasons **have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>Title in English</td>

</tr>

<tr>

<td>start</td>

<td>string</td>

<td>Start date in a format "yyyy-mm-dd"</td>

</tr>

<tr>

<td>end</td>

<td>string</td>

<td>End date in a format "yyyy-mm-dd"</td>

</tr>

<tr>

<td>is_appointment_based</td>

<td>boolean</td>

<td>Are the visits based on appointments?</td>

</tr>

<tr>

<td>mon_open</td>

<td>string</td>

<td>Opening time on Mondays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>mon_close</td>

<td>string</td>

<td>Closing time on Mondays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>mon_break_close</td>

<td>string</td>

<td>Start time of the break on Mondays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>mon_break_open</td>

<td>string</td>

<td>End time of the break on Mondays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>tue_open</td>

<td>string</td>

<td>Opening time on Tuesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>tue_close</td>

<td>string</td>

<td>Closing tine on Tuesdays in a fornat "hh:ii;ss"</td>

</tr>

<tr>

<td>tue_break_close</td>

<td>string</td>

<td>Start time of the break on Tuesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>tue_break_open</td>

<td>string</td>

<td>End time of the break on Tuesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>wed_open</td>

<td>string</td>

<td>Opening time on Wednesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>wed_close</td>

<td>string</td>

<td>Closing time on Wednesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>wed_break_close</td>

<td>string</td>

<td>Start time of the break on Wednesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>wed_break_open</td>

<td>string</td>

<td>End time of the break on Wednesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>thu_open</td>

<td>string</td>

<td>Opening time on Thursdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>thu_close</td>

<td>string</td>

<td>Closing time on Thursdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>thu_break_close</td>

<td>string</td>

<td>Start time of the break on Thursdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>thu_break_open</td>

<td>string</td>

<td>End time of the break on Thursdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>fri_open</td>

<td>string</td>

<td>Opening time on Fridays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>fri_close</td>

<td>string</td>

<td>Closing time on Fridays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>fri_break_close</td>

<td>string</td>

<td>Start time of the break on Fridays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>fri_break_open</td>

<td>string</td>

<td>End time of the break on Fridays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sat_open</td>

<td>string</td>

<td>Opening time on Saturdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sat_close</td>

<td>string</td>

<td>Closing time on Saturdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sat_break_close</td>

<td>string</td>

<td>Start time of the break on Saturdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sat_break_open</td>

<td>string</td>

<td>End time of the break on Saturdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sun_open</td>

<td>string</td>

<td>Opening time on Sundays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sun_close</td>

<td>string</td>

<td>Closing time on Sundays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sun_break_close</td>

<td>string</td>

<td>Start time of the break on Sundays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sun_break_open</td>

<td>string</td>

<td>End time of the break on Sundays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>exceptions_de</td>

<td>string</td>

<td>Exceptional opening hours in German</td>

</tr>

<tr>

<td>exceptions_en</td>

<td>string</td>

<td>Exceptional opening hours in English</td>

</tr>

<tr>

<td>last_entry_de</td>

<td>string</td>

<td>Information about last entry in German</td>

</tr>

<tr>

<td>last_entry_en</td>

<td>string</td>

<td>Information about last entry in English</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the season</td>

</tr>

</tbody>

</table>

**Special opening times** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>day_label_de</td>

<td>string</td>

<td>Day label in German</td>

</tr>

<tr>

<td>day_label_en</td>

<td>string</td>

<td>Day label in English</td>

</tr>

<tr>

<td>yyyy</td>

<td>integer</td>

<td>Year (`null` if happens every year)</td>

</tr>

<tr>

<td>mm</td>

<td>integer</td>

<td>Month</td>

</tr>

<tr>

<td>dd</td>

<td>integer</td>

<td>Day</td>

</tr>

<tr>

<td>opening</td>

<td>string</td>

<td>Opening time in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>closing</td>

<td>string</td>

<td>Closing time in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>break_close</td>

<td>string</td>

<td>Closing time for a break in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>break_open</td>

<td>string</td>

<td>Opening time after a break in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>is_closed</td>

<td>boolean</td>

<td>Is the museum closed at this day?</td>

</tr>

<tr>

<td>is_regular</td>

<td>boolean</td>

<td>Are the opening times regular at this day?</td>

</tr>

<tr>

<td>exceptions_de</td>

<td>string</td>

<td>Exceptions of the opening hours in German</td>

</tr>

<tr>

<td>exceptions_en</td>

<td>string</td>

<td>Exceptions of the opening hours in English</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the special opening time</td>

</tr>

</tbody>

</table>

**Media files** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>url</td>

<td>string</td>

<td>Image URL</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>Title in English</td>

</tr>

<tr>

<td>description_de</td>

<td>string</td>

<td>Description in German</td>

</tr>

<tr>

<td>description_en</td>

<td>string</td>

<td>Description in English</td>

</tr>

<tr>

<td>author</td>

<td>string</td>

<td>Author and Copyright</td>

</tr>

<tr>

<td>copyright_limitations</td>

<td>string</td>

<td>Additional Copyright Information</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the image</td>

</tr>

</tbody>

</table>

### Exhibitions

**Exhibitions** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>

Title in English

</td>

</tr>

<tr>

<td>subtitle_de</td>

<td>string</td>

<td>Subtitle in German</td>

</tr>

<tr>

<td>subtitle_en</td>

<td>string</td>

<td>Subtitle in English</td>

</tr>

<tr>

<td>press_text_de</td>

<td>string</td>

<td>Press text in German</td>

</tr>

<tr>

<td>press_text_en</td>

<td>string</td>

<td>Press text in English</td>

</tr>

<tr>

<td>catalog_de</td>

<td>string</td>

<td>Catalog information in German</td>

</tr>

<tr>

<td>catalog_en</td>

<td>string</td>

<td>Catalog information in English</td>

</tr>

<tr>

<td>catalog_ordering_de</td>

<td>string</td>

<td>Catalog ordering link for German readers</td>

</tr>

<tr>

<td>catalog_ordering_en</td>

<td>string</td>

<td>Catalog ordering link for English readers</td>

</tr>

<tr>

<td>website_de</td>

<td>string</td>

<td>External website for German readers</td>

</tr>

<tr>

<td>website_en</td>

<td>string</td>

<td>External website for English readers</td>

</tr>

<tr>

<td>start</td>

<td>string</td>

<td>Start date in a format "yyyy-mm-dd"</td>

</tr>

<tr>

<td>end</td>

<td>string</td>

<td>End date in a format "yyyy-mm-dd"</td>

</tr>

<tr>

<td>vernissage</td>

<td>string</td>

<td>The date and time of the vernissage in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>finissage</td>

<td>string</td>

<td>The date and time of the finissage in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>exhibition_extended</td>

<td>boolean</td>

<td>Is this exhibition extended?</td>

</tr>

<tr>

<td>permanent</td>

<td>boolean</td>

<td>Is this exhibition permanent?</td>

</tr>

<tr>

<td>museum</td>

<td>string</td>

<td>Endpoint to the details of the museum</td>

</tr>

<tr>

<td>location_name</td>

<td>string</td>

<td>Location name, when differs from museum</td>

</tr>

<tr>

<td>street_address</td>

<td>string</td>

<td>

Street address

</td>

</tr>

<tr>

<td>street_address2</td>

<td>string</td>

<td>Second line of street address</td>

</tr>

<tr>

<td>postal_code</td>

<td>string</td>

<td>Postal code</td>

</tr>

<tr>

<td>city</td>

<td>string</td>

<td>City</td>

</tr>

<tr>

<td>country</td>

<td>string</td>

<td>Country code e.g. "de"</td>

</tr>

<tr>

<td>latitude</td>

<td>float</td>

<td>Latitude</td>

</tr>

<tr>

<td>longitude</td>

<td>float</td>

<td>Longitude</td>

</tr>

<tr>

<td>other_locations_de</td>

<td>string</td>

<td>Other locations in German</td>

</tr>

<tr>

<td>other_locations_en</td>

<td>string</td>

<td>Other locations in English</td>

</tr>

<tr>

<td>organizers</td>

<td>list</td>

<td>List of additional organizers</td>

</tr>

<tr>

<td>museum_prices</td>

<td>boolean</td>

<td>Are the prices the same as at the museum?</td>

</tr>

<tr>

<td>free_entrance</td>

<td>boolean</td>

<td>Is the entrance free?</td>

</tr>

<tr>

<td>admission_price</td>

<td>string</td>

<td>Admission price in Euros, e.g. "12.00"</td>

</tr>

<tr>

<td>admission_price_info_de</td>

<td>string</td>

<td>Admission price information in German</td>

</tr>

<tr>

<td>admission_price_info_en</td>

<td>string</td>

<td>Admission price information in English</td>

</tr>

<tr>

<td>reduced_price</td>

<td>string</td>

<td>Reduced admission price in Euros e.g. "8.00"</td>

</tr>

<tr>

<td>reduced_price_info_de</td>

<td>string</td>

<td>Reduced admission price information in German</td>

</tr>

<tr>

<td>reduced_price_info_en</td>

<td>string</td>

<td>Reduced admission price information in English</td>

</tr>

<tr>

<td>museum_opening_hours</td>

<td>boolean</td>

<td>Opening hours of the museum</td>

</tr>

<tr>

<td>seasons</td>

<td>list</td>

<td>List of season objects (one or none items)</td>

</tr>

<tr>

<td>suitable_for_disabled</td>

<td>boolean</td>

<td>Is the exhibition suitable for disabled?</td>

</tr>

<tr>

<td>suitable_for_disabled_info_de</td>

<td>string</td>

<td>Information in German about suitability for disabled people</td>

</tr>

<tr>

<td>suitable_for_disabled_info_en</td>

<td>string</td>

<td>Information in English about suitability for disabled people</td>

</tr>

<tr>

<td>is_for_children</td>

<td>boolean</td>

<td>Is the exhibition suitable for children?</td>

</tr>

<tr>

<td>media_files</td>

<td>list</td>

<td>List of media files</td>

</tr>

<tr>

<td>status</td>

<td>string</td>

<td>Status having one of these values: "draft", "published", "not_listed", "expired", "import", "trashed"</td>

</tr>

<tr>

<td>categories</td>

<td>list</td>

<td>List of category objects</td>

</tr>

<tr>

<td>link_de</td>

<td>string</td>

<td>The URL of the exhibition at http://www.museumsportal-berlin.de/ in German</td>

</tr>

<tr>

<td>link_en</td>

<td>string</td>

<td>The URL of the exhibition at http://www.museumsportal-berlin.de/ in English</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the exhibition</td>

</tr>

</tbody>

</table>

**Organizers** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Descriotion</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>organizing_museum</td>

<td>string</td>

<td>Endpoint to the details of a museum</td>

</tr>

<tr>

<td>organizer_title</td>

<td>string</td>

<td>Organizer title if organizing_museum is empty</td>

</tr>

<tr>

<td>organizer_url_link</td>

<td>string</td>

<td>Organizer URL if organizing_museum is empty</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the organizer</td>

</tr>

</tbody>

</table>

**Seasons** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>is_appointment_based</td>

<td>boolean</td>

<td>Are the visits based on appointments?</td>

</tr>

<tr>

<td>is_open_24_7</td>

<td>boolean</td>

<td>Is open 24/7?</td>

</tr>

<tr>

<td>mon_open</td>

<td>string</td>

<td>Opening time on Mondays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>mon_close</td>

<td>string</td>

<td>Closing time on Mondays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>mon_break_close</td>

<td>string</td>

<td>Start time of the break on Mondays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>mon_break_open</td>

<td>string</td>

<td>End time of the break on Mondays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>tue_open</td>

<td>string</td>

<td>Opening time on Tuesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>tue_close</td>

<td>string</td>

<td>Closing tine on Tuesdays in a fornat "hh:ii;ss"</td>

</tr>

<tr>

<td>tue_break_close</td>

<td>string</td>

<td>Start time of the break on Tuesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>tue_break_open</td>

<td>string</td>

<td>End time of the break on Tuesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>wed_open</td>

<td>string</td>

<td>Opening time on Wednesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>wed_close</td>

<td>string</td>

<td>Closing time on Wednesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>wed_break_close</td>

<td>string</td>

<td>Start time of the break on Wednesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>wed_break_open</td>

<td>string</td>

<td>End time of the break on Wednesdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>thu_open</td>

<td>string</td>

<td>Opening time on Thursdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>thu_close</td>

<td>string</td>

<td>Closing time on Thursdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>thu_break_close</td>

<td>string</td>

<td>Start time of the break on Thursdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>thu_break_open</td>

<td>string</td>

<td>End time of the break on Thursdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>fri_open</td>

<td>string</td>

<td>Opening time on Fridays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>fri_close</td>

<td>string</td>

<td>Closing time on Fridays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>fri_break_close</td>

<td>string</td>

<td>Start time of the break on Fridays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>fri_break_open</td>

<td>string</td>

<td>End time of the break on Fridays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sat_open</td>

<td>string</td>

<td>Opening time on Saturdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sat_close</td>

<td>string</td>

<td>Closing time on Saturdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sat_break_close</td>

<td>string</td>

<td>Start time of the break on Saturdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sat_break_open</td>

<td>string</td>

<td>End time of the break on Saturdays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sun_open</td>

<td>string</td>

<td>Opening time on Sundays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sun_close</td>

<td>string</td>

<td>Closing time on Sundays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sun_break_close</td>

<td>string</td>

<td>Start time of the break on Sundays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>sun_break_open</td>

<td>string</td>

<td>End time of the break on Sundays in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>exceptions_de</td>

<td>string</td>

<td>Exceptional opening hours in German</td>

</tr>

<tr>

<td>exceptions_en</td>

<td>string</td>

<td>Exceptional opening hours in English</td>

</tr>

<tr>

<td>last_entry_de</td>

<td>string</td>

<td>Information about last entry in German</td>

</tr>

<tr>

<td>last_entry_en</td>

<td>string</td>

<td>Information about last entry in English</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the season</td>

</tr>

</tbody>

</table>

**Media files** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>url</td>

<td>string</td>

<td>Image URL</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>Title in English</td>

</tr>

<tr>

<td>description_de</td>

<td>string</td>

<td>Description in German</td>

</tr>

<tr>

<td>description_en</td>

<td>string</td>

<td>Description in English</td>

</tr>

<tr>

<td>author</td>

<td>string</td>

<td>Author and Copyright</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the image</td>

</tr>

</tbody>

</table>

### Events

**Events **have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>

Title in English

</td>

</tr>

<tr>

<td>subtitle_de</td>

<td>string</td>

<td>Subtitle in German</td>

</tr>

<tr>

<td>subtitle_en</td>

<td>string</td>

<td>Subtitle in English</td>

</tr>

<tr>

<td>event_type_de</td>

<td>string</td>

<td>Event type in German</td>

</tr>

<tr>

<td>event_type_en</td>

<td>string</td>

<td>Event type in Englsh</td>

</tr>

<tr>

<td>website_de</td>

<td>string</td>

<td>External website in German</td>

</tr>

<tr>

<td>website_en</td>

<td>string</td>

<td>External website in English</td>

</tr>

<tr>

<td>event_times</td>

<td>list</td>

<td>List of event times</td>

</tr>

<tr>

<td>museum</td>

<td>string</td>

<td>Endpoint to the details of the museum</td>

</tr>

<tr>

<td>location_name</td>

<td>string</td>

<td>Location name, when differs from museum</td>

</tr>

<tr>

<td>street_address</td>

<td>string</td>

<td>

Street address

</td>

</tr>

<tr>

<td>street_address2</td>

<td>string</td>

<td>Second line of street address</td>

</tr>

<tr>

<td>postal_code</td>

<td>string</td>

<td>Postal code</td>

</tr>

<tr>

<td>city</td>

<td>string</td>

<td>City</td>

</tr>

<tr>

<td>country</td>

<td>string</td>

<td>Country code e.g. "de"</td>

</tr>

<tr>

<td>latitude</td>

<td>float</td>

<td>Latitude</td>

</tr>

<tr>

<td>longitude</td>

<td>float</td>

<td>Longitude</td>

</tr>

<tr>

<td>meeting_place_de</td>

<td>string</td>

<td>Meeting place in German</td>

</tr>

<tr>

<td>meeting_place_en</td>

<td>string</td>

<td>Meeting place in English</td>

</tr>

<tr>

<td>organizers</td>

<td>list</td>

<td>List of organizers</td>

</tr>

<tr>

<td>exhibition</td>

<td>string</td>

<td>Endpoint to the details of the related exhibition</td>

</tr>

<tr>

<td>languages_de</td>

<td>list</td>

<td>List of languages in German</td>

</tr>

<tr>

<td>free_admission</td>

<td>boolean</td>

<td>Is the admission free?</td>

</tr>

<tr>

<td>admission_price</td>

<td>string</td>

<td>Admission price in Euros, e.g. "12.00"</td>

</tr>

<tr>

<td>admission_price_info_de</td>

<td>string</td>

<td>Admission price information in German</td>

</tr>

<tr>

<td>admission_price_info_en</td>

<td>string</td>

<td>Admission price information in English</td>

</tr>

<tr>

<td>reduced_price</td>

<td>string</td>

<td>Reduced admission price in Euros e.g. "8.00"</td>

</tr>

<tr>

<td>booking_info_de</td>

<td>string</td>

<td>Booking information in German</td>

</tr>

<tr>

<td>booking_info_en</td>

<td>string</td>

<td>Booking information in English</td>

</tr>

<tr>

<td>media_files</td>

<td>list</td>

<td>List of media files</td>

</tr>

<tr>

<td>status</td>

<td>string</td>

<td>Status having one of these values: "draft", "published", "not_listed", "expired", "import", "trashed"</td>

</tr>

<tr>

<td>categories</td>

<td>list</td>

<td>List of category objects</td>

</tr>

<tr>

<td>link_de</td>

<td>string</td>

<td>The URL of the event at http://www.museumsportal-berlin.de/ in German</td>

</tr>

<tr>

<td>link_en</td>

<td>string</td>

<td>The URL of the event at http://www.museumsportal-berlin.de/ in English</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the event</td>

</tr>

</tbody>

</table>

**Event times** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>event_date</td>

<td>string</td>

<td>Event date in a format "yyyy-mm-dd"</td>

</tr>

<tr>

<td>start</td>

<td>string</td>

<td>Start time in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>end</td>

<td>string</td>

<td>End tine in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the event time</td>

</tr>

</tbody>

</table>

**Organizers** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Descriotion</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>organizing_museum</td>

<td>string</td>

<td>Endpoint to the details of a museum</td>

</tr>

<tr>

<td>organizer_title</td>

<td>string</td>

<td>Organizer title if organizing_museum is empty</td>

</tr>

<tr>

<td>organizer_url_link</td>

<td>string</td>

<td>Organizer URL if organizing_museum is empty</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the organizer</td>

</tr>

</tbody>

</table>

**Media files** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>url</td>

<td>string</td>

<td>Image URL</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>Title in English</td>

</tr>

<tr>

<td>description_de</td>

<td>string</td>

<td>Description in German</td>

</tr>

<tr>

<td>description_en</td>

<td>string</td>

<td>Description in English</td>

</tr>

<tr>

<td>author</td>

<td>string</td>

<td>Author and Copyright</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the image</td>

</tr>

</tbody>

</table>

### Workshops (Guided Tours)

**Workshops **have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>

Title in English

</td>

</tr>

<tr>

<td>subtitle_de</td>

<td>string</td>

<td>Subtitle in German</td>

</tr>

<tr>

<td>subtitle_en</td>

<td>string</td>

<td>Subtitle in English</td>

</tr>

<tr>

<td>workshop_type_de</td>

<td>string</td>

<td>Workshop type in German</td>

</tr>

<tr>

<td>workshop_type_en</td>

<td>string</td>

<td>Workshop type in Englsh</td>

</tr>

<tr>

<td>website_de</td>

<td>string</td>

<td>External website in German</td>

</tr>

<tr>

<td>website_en</td>

<td>string</td>

<td>External website in English</td>

</tr>

<tr>

<td>workshop_times</td>

<td>list</td>

<td>List of workshop times</td>

</tr>

<tr>

<td>museum</td>

<td>string</td>

<td>Endpoint to the details of the museum</td>

</tr>

<tr>

<td>location_name</td>

<td>string</td>

<td>Location name, when differs from museum</td>

</tr>

<tr>

<td>street_address</td>

<td>string</td>

<td>

Street address

</td>

</tr>

<tr>

<td>street_address2</td>

<td>string</td>

<td>Second line of street address</td>

</tr>

<tr>

<td>postal_code</td>

<td>string</td>

<td>Postal code</td>

</tr>

<tr>

<td>city</td>

<td>string</td>

<td>City</td>

</tr>

<tr>

<td>country</td>

<td>string</td>

<td>Country code e.g. "de"</td>

</tr>

<tr>

<td>latitude</td>

<td>float</td>

<td>Latitude</td>

</tr>

<tr>

<td>longitude</td>

<td>float</td>

<td>Longitude</td>

</tr>

<tr>

<td>meeting_place_de</td>

<td>string</td>

<td>Meeting place in German</td>

</tr>

<tr>

<td>meeting_place_en</td>

<td>string</td>

<td>Meeting place in English</td>

</tr>

<tr>

<td>organizers</td>

<td>list</td>

<td>List of organizers</td>

</tr>

<tr>

<td>exhibition</td>

<td>string</td>

<td>Endpoint to the details of the related exhibition</td>

</tr>

<tr>

<td>languages_de</td>

<td>list</td>

<td>List of languages in German</td>

</tr>

<tr>

<td>free_admission</td>

<td>boolean</td>

<td>Is the admission free?</td>

</tr>

<tr>

<td>admission_price</td>

<td>string</td>

<td>Admission price in Euros, e.g. "12.00"</td>

</tr>

<tr>

<td>admission_price_info_de</td>

<td>string</td>

<td>Admission price information in German</td>

</tr>

<tr>

<td>admission_price_info_en</td>

<td>string</td>

<td>Admission price information in English</td>

</tr>

<tr>

<td>reduced_price</td>

<td>string</td>

<td>Reduced admission price in Euros e.g. "8.00"</td>

</tr>

<tr>

<td>booking_info_de</td>

<td>string</td>

<td>Booking information in German</td>

</tr>

<tr>

<td>booking_info_en</td>

<td>string</td>

<td>Booking information in English</td>

</tr>

<tr>

<td>has_group_offer</td>

<td>boolean</td>

<td>Has bookable group offer?</td>

</tr>

<tr>

<td>is_for_preschool</td>

<td>boolean</td>

<td>Is special for preschool children (up to 5 years)?</td>

</tr>

<tr>

<td>is_for_primary_school</td>

<td>boolean</td>

<td>Is special for children of primary school age (6-12 years)?</td>

</tr>

<tr>

<td>is_for_youth</td>

<td>boolean</td>

<td>Is special for youth (aged 13 years)?</td>

</tr>

<tr>

<td>is_for_families</td>

<td>boolean</td>

<td>Is special for families?</td>

</tr>

<tr>

<td>is_for_wheelchaired</td>

<td>boolean</td>

<td>Is special for people in wheelchairs?</td>

</tr>

<tr>

<td>is_for_deaf</td>

<td>boolean</td>

<td>Is special for deaf people?</td>

</tr>

<tr>

<td>is_for_blind</td>

<td>boolean</td>

<td>Is special for blind people?</td>

</tr>

<tr>

<td>is_for_learning_difficulties</td>

<td>boolean</td>

<td>Is special for people with learning difficulties?</td>

</tr>

<tr>

<td>media_files</td>

<td>list</td>

<td>List of media files</td>

</tr>

<tr>

<td>status</td>

<td>string</td>

<td>Status having one of these values: "draft", "published", "not_listed", "expired", "import", "trashed"</td>

</tr>

<tr>

<td>categories</td>

<td>list</td>

<td>List of category objects</td>

</tr>

<tr>

<td>link_de</td>

<td>string</td>

<td>The URL of the workshop at http://www.museumsportal-berlin.de/ in German</td>

</tr>

<tr>

<td>link_en</td>

<td>string</td>

<td>The URL of the workshop at http://www.museumsportal-berlin.de/ in English</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the workshop</td>

</tr>

</tbody>

</table>

**Workshop times** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>workshop_date</td>

<td>string</td>

<td>Workshop date in a format "yyyy-mm-dd"</td>

</tr>

<tr>

<td>start</td>

<td>string</td>

<td>Start time in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>end</td>

<td>string</td>

<td>End tine in a format "hh:ii:ss"</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the workshop time</td>

</tr>

</tbody>

</table>

**Organizers** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Descriotion</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>organizing_museum</td>

<td>string</td>

<td>Endpoint to the details of a museum</td>

</tr>

<tr>

<td>organizer_title</td>

<td>string</td>

<td>Organizer title if organizing_museum is empty</td>

</tr>

<tr>

<td>organizer_url_link</td>

<td>string</td>

<td>Organizer URL if organizing_museum is empty</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the organizer</td>

</tr>

</tbody>

</table>

**Media files** have these fields:

<table>

<tbody>

<tr>

<th>Field</th>

<th>Type</th>

<th>Description</th>

</tr>

<tr>

<td>id</td>

<td>integer</td>

<td>Unique identifier</td>

</tr>

<tr>

<td>creation_date</td>

<td>string</td>

<td>Creation date and time in a fornat "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>modified_date</td>

<td>string</td>

<td>Modification date and time in a format "yyyy-mm-ddThh:mm:ss"</td>

</tr>

<tr>

<td>url</td>

<td>string</td>

<td>Image URL</td>

</tr>

<tr>

<td>title_de</td>

<td>string</td>

<td>Title in German</td>

</tr>

<tr>

<td>title_en</td>

<td>string</td>

<td>Title in English</td>

</tr>

<tr>

<td>description_de</td>

<td>string</td>

<td>Description in German</td>

</tr>

<tr>

<td>description_en</td>

<td>string</td>

<td>Description in English</td>

</tr>

<tr>

<td>author</td>

<td>string</td>

<td>Author and Copyright</td>

</tr>

<tr>

<td>resource_uri</td>

<td>string</td>

<td>Endpoint to the details of the image</td>

</tr>

</tbody>

</table>