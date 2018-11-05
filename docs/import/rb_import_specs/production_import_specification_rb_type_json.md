# Production Import Specification #

Last update: October 30, 2018

[TOC]

## Introduction ##

The Ruhr Bühnen website has locations (theaters) and stages where plays happen. All plays are named as productions. Productions have general information about the play. Each production has multiple events, that is, exact dates and times when the play happens. Events might overwrite some general information of their production.

## How to prepare the feed?

The JSON for the import API should have the following structure:

```javascript
{
    "meta": {
        // meta information
    },
    "productions": [
        {
            // production properties
            "events": [
                {
                    // event properties
                },
                {
                    // event properties
                },
                // other events
            ]
        },
        {
            // production properties
            "events": [
                {
                    // event properties
                },
                {
                    // event properties
                },
                // other events
            ]
        },
        // other productions
    ]    
}
```

[For XML version look here](production_import_specification_bb_type_xml.html)


### The Meta Section ###

The `"meta"` section contains information about pagination and amount of productions, as follows:

| Key | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"next"` | URL | no | The API URL for the next page (or empty string for the last page) | "http://example.com/api/productions/?page=3" |
| `"previous"` | URL | no | The API URL for the previous page (or empty string for the first page) | "http://example.com/api/productions/?page=1" |
| `"total_count"` | integer | yes | How many productions are there in total? | 521 |
| `"items_per_page"` | integer | yes | What is the maximal amount of productions per page? | 50 |

### The Productions Section ###

The `"productions"` section contains paginated list of productions and their events.

## Productions ##

### The Production Object ###

Each `production` object has the following keys and values:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"id"` | string or integer | yes | Unique production ID on your website | 12 |
| `"creation_date"`| dateTime | yes | Production creation timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"modified_date"` | dateTime | no | Production modification timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"status"` | string | yes | Publishing status, one of: "`draft`", "`published`", "`not_listed`", "`expired`", "`trashed`" | "published" |
| `"prefix_de"` | string | no | Title prefix in German | |
| `"prefix_en"` | string | no | Title prefix in English | |
| `"title_de"` | string | yes | Title in German | "Rotkäppchen" |
| `"title_en"` | string | yes | Title in English | "Little Red Riding Hood" |
| `"subtitle_de"` | string | no | Subtitle (Unterüberschrift) in German | |
| `"subtitle_en"` | string | no | Subtitle (Unterüberschrift) in English | |
| `"original_de"` | string | no | Original title in German | |
| `"original_en"` | string | no | Original title in English | |
| `"website_de"` | URL | no | A link to the your website page about this production in German | "http://example.com/de/productions/2345/" |
| `"website_en"` | URL | no | A link to the your website page about this production in English | "http://example.com/en/productions/2345/" |
| `"description_de"` | string | no | Plain-text description in German | |
| `"description_en"` | string | no | Plain-text description in English | |
| `"teaser_de"` | string | no | Plain-text teaser in German | |
| `"teaser_en"` | string | no | Plain-text teaser in English | |
| `"work_info_de"` | string | no | Plain-text work info in German | |
| `"work_info_en"` | string | no | Plain-text work info in English | |
| `"contents_de"` | string | no | Plain-text contents in German | |
| `"contents_en"` | string | no | Plain-text contents in English | |
| `"press_text_de"` | string | no | Plain-text press text in German | |
| `"press_text_en"` | string | no | Plain-text press text in English | |
| `"credits_de"` | string | no | Plain-text credits in German | |
| `"credits_en"` | string | no | Plain-text credits in English | |
| `"concert_program_de"` | string | no | Plain-text concert program in German | |
| `"concert_program_en"` | string | no | Plain-text concert program in English | |
| `"supporting_program_de"` | string | no | Plain-text supporting program in German | |
| `"supporting_program_en"` | string | no | Plain-text supporting program in English | |
| `"remarks_de"` | string | no | Plain-text remarks in German | |
| `"remarks_en"` | string | no | Plain-text remarks in English | |
| `"duration_text_de"` | string | no | Plain-text information about duration in German | |
| `"duration_text_en"` | string | no | Plain-text information about duration in English | |
| `"subtitles_text_de"` | string | no | Plain-text information about subtitles in German | |
| `"subtitles_text_en"` | string | no | Plain-text information about subtitles in English | |
| `"age_text_de"` | string | no | Plain-text information about the age of the audience in German | |
| `"age_text_en"` | string | no | Plain-text information about the age of the audience in English | |
| `"ensembles"` | string | no | Ensemble or ensembles playing in this production  | |
| `"organizers"` | string | no | Organizer or organizers of this production | |
| `"in_cooperation_with"` | string | no | Cooperator or cooperators | |
| `"free_entrance"` | string | no | Is the entrance free? One of "true" or "false" | "false" |
| `"price_from"` | string | no | Price from in Euros (no currency sign included) | "8.00" |
| `"price_till"` | string | no | Price till in Euros (no currency sign included) | "12.00" |
| `"tickets_website"` | URL | no | The URL of a website page where you can buy tickets to this production | "http://example.com/tickets/" |
| `"price_information_de"` | string | no | Additional plain-text information about prices in German | |
| `"price_information_en"` | string | no | Additional plain-text information about prices in English | |
| `"age_from"` | integer | no | Audience age from | 18 |
| `"age_till"` | integer | no | Audience age till | 99 |
| `"edu_offer_website"` | URL | no | The URL of a website page with educational offer | "http://example.com/educational-offer/" |
| `"in_program_of"` | list of location IDs | no | Theaters organizing this production | |
| `"play_locations"` | list of location IDs | no | Theaters where this production takes place | |
| `"play_stages"` | list of stage IDs | no | Stages where this production takes place | |
| `"location_title"` | string | no | Location title (if `"play_locations"` is empty) | |
| `"street_address"`| string | no | Street address (first line) of the location (if `"play_locations"` is empty) | |
| `"street_address2"` | string | no | Street address (second line) of the location (if `"play_locations"` is empty) | |
| `"postal_code"`| string | no | Postal code of the location (if `"play_locations"` is empty) | |
| `"city"`| string | no | City of the location (if `"play_locations"` is empty) | |
| `"latitude"`| string | no | Latitude of the location (if `"play_locations"` is empty) | "52.5192" |
| `"longitude"` | string | no | Longitude of the location (if `"play_locations"` is empty) | "13.4061" |
| `"categories"` | list of category IDs | no | Categories | |
| `"characteristics"`| list of characteristic IDs | no | Production characteristics | |
| `"leaders"` | list of `leader` objects | no | Leaders | |
| `"authors"` | list of `author` objects | no | Authors | |
| `"participants"` | list of `participant` objects | no | Participants | |
| `"videos"` | list of `video` objects | no | Videos | |
| `"live_streams"` | list of `live_stream` objects | no | Live streams | |
| `"images"` | list of `image` objects | no | Images | |
| `"pdfs"` | list of `pdf` objects | no | PDF documents | |
| `"social_media"` | list of `social_media_channel` objects | no | Social media | |
| `"language_and_subtitles_id"` | string | no | Language and subtitles | "in-deutscher-sprache" |
| `"sponsors"` | list of `sponsor` objects | no | Sponsors | |
| `"events"` | list of `event` objects | no | Events | |
| `"classiccard"` | string | no | Intended for ClassicCard holders. One of “true” or “false” | "false" |

### The Locations and Stages for Productions or Events ###

This is a list of all available locations and stages with location IDs and stage IDs to enter as values at `"location_id"` and `"stage_id"`:

<!--
from ruhrbuehnen.apps.locations.models import Location
ls = Location.objects.filter(status='published')
for l in ls:
    print u'- {0} (Location ID = {1})'.format(l.title, l.pk)
    for s in l.stage_set.all():
        print u'  - {0} (Stage ID = {1})'.format(s.title, s.pk)        
-->

- Deutsche Oper am Rhein im Theater Duisburg (Location ID = 229)
  - Deutsche Oper am Rhein im Theater Duisburg (Stage ID = 239)
- Musiktheater im Revier Gelsenkirchen (Location ID = 232)
  - Grosses Haus / Kleines Haus (Stage ID = 244)
- PACT Zollverein (Location ID = 230)
  - PACT Zollverein (Stage ID = 240)
- Ringlokschuppen Ruhr (Location ID = 234)
  - Ringlokschuppen Ruhr (Stage ID = 248)
- Schauspielhaus Bochum (Location ID = 226)
- Schauspielhaus Bochum (Location ID = 227)
  - Schauspielhaus / Kammerspiele / Oval Office (Stage ID = 227)
  - Zeche Eins (Stage ID = 228)
- Schlosstheater Moers (Location ID = 225)
  - Schloss (Stage ID = 224)
  - Studio (Stage ID = 246)
  - St. Barbara Jugendheim (Stage ID = 247)
- Theater Dortmund (Location ID = 228)
  - Schauspiel / Studio (Stage ID = 234)
  - Opernhaus (Stage ID = 235)
  - Konzerthaus Dortmund (Stage ID = 236)
  - Junge Oper (Stage ID = 237)
  - Kinder- und Jugendtheater KJT (Stage ID = 238)
- Theater Hagen (Location ID = 233)
  - Grosses Haus / Lutz (Stage ID = 245)
- Theater Oberhausen (Location ID = 236)
  - Grosses Haus / Saal 2 (Stage ID = 250)
  - Aussenspielort (Stage ID = 251)
- Theater an der Ruhr (Location ID = 235)
  - Theater an der Ruhr (Stage ID = 249)
- Theater und Philharmonie Essen (Location ID = 231)
  - Aalto-Theater (Stage ID = 241)
  - Grillo-Theater (Stage ID = 242)
  - CASA Theaterpassage (Stage ID = 243)
  
For example, if a production is organized by "Theater Dortmund" and happens in the "Opernhaus" stage, the following keys and values should be set:

```json
"in_program_of": [228],
"play_stages": [235],
```

### The Categories for Productions ###

This is a list of all available categories and subcategories with IDs to enter as values at `"category_id"`:

<!--
from ruhrbuehnen.apps.productions.models import ProductionCategory
cs = ProductionCategory.objects.filter(parent=None)
for c in cs:
    print u'- {0} | {1} (Category ID = {2})'.format(c.title_de, c.title_en, c.pk)
    for s in c.children.all():
        print u'  - {0} | {1} (Category ID = {2})'.format(s.title_de, s.title_en, s.pk)
-->

- Schauspiel | Theatre (Category ID = 1)
- Oper & Operette | Music Theater (Category ID = 2)
- Musical & Liederabend | Concert (Category ID = 5)
- Ballett & Tanz | Ballet & Dance (Category ID = 3)
- Performance & Installation | Performance (Category ID = 4)
- Literatur & Diskurs | Discourse (Category ID = 9)
- Kinder & Jugend | Children & Youth (Category ID = 8)
- Außerdem | Other (Category ID = 10)

For example, if a production can be classified as "Tanz", "Konzert", and "Comedy & Kabarett", the following key and value should be set:

```json
"categories": [3, 5, 7],
```

### The Production Characteristics ###

This is a list of all available characteristics with IDs to enter as values at `"characteristic_id"` of the production:

<!--
from ruhrbuehnen.apps.productions.models import ProductionCharacteristics
ps = ProductionCharacteristics.objects.all()
for p in ps:
    print u'- {0} | {1} (ID = "{2}")'.format(p.title_de, p.title_en, p.slug)
-->

- On Tour | On Tour (ID = "on-tour")
- Gastspiel | Guest Play (ID = "gastspiel")
- Repertoire | Repertoire (ID = "repertoire")
- Wiederaufnahme | Replay (ID = "wiederaufnahme")
- Uraufführung | Premiere (ID = "urauffuehrung")

For example, if a production can be classified as "Gastspiel", the following key and value should be set:

```json
"characteristics": ["gastspiel"],
```

### The Leaders, Authors, and Participants for Productions or Events ###

The `"leaders"` object contains a list of `leader` objects with such content:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"prefix_id"` | string | no | Prefix ID | "ms-dr" |
| `"first_name"` | string | no | First name of the person | "Erika" |
| `"last_name"` | string | yes | Last name of the person | "Mustermann" |
| `"function_de"` | NCName | yes | Description in German what this leader is doing for the production | "Direktorin" |
| `"function_en"` | NCName | yes | Description in English what this leader is doing for the production | "Director" |
| `"sort_order"` | integer | yes | Sort order | 1 |

The `"authors"` object contains a list of `author` objects with such content:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"prefix_id"` | string | no | Prefix ID | "mr" |
| `"first_name"` | string | no | First name of the person | "Max" |
| `"last_name"` | string | yes | Last name of the person | "Mustermann" |
| `"authorship_type_id"` | string | yes | Authorship type. One of: "komponist", "autor", "uebersetzer" | "komponist" |
| `"sort_order"` | integer | yes | Sort order | 1 |

The `"participants"` object contains a list of `participant` objects with such content:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"prefix_id"` | string | no | Prefix ID | "ms-dr" |
| `"first_name"` | string | no | First name of the person | "Erika" |
| `"last_name"` | string | yes | Last name of the person or a title of a group | "Mustermann" |
| `"involvement_type_id"` | string | no | Involvement type ID | "musik" |
| `"role_de"` | string | no | Role in German | "Rotkäppchen" |
| `"role_en"` | string | no | Role in English | "Little Red Riding Hood" |
| `"instrument_de"` | string | no | Instrument in German | "Klavier" |
| `"instrument_en"` | string | no | Instrument in English | "Piano" |
| `"sort_order"` | integer | yes | Sort order | 1 |

Either `"involvement_type_id"`, or `"role_*"`, or `"instrument_*"` should be provided.

Prefixes and their IDs are these:

<!--
from ruhrbuehnen.apps.people.models import Prefix 
ps = Prefix.objects.all()
for p in ps:
    print u'- {0} | {1} (ID = "{2}")'.format(p.title_de, p.title_en, p.slug)
-->

- Herr | Mr. (ID = "mr")
- Frau | Mrs./Ms. (ID = "ms")
- Dr. | Dr. (ID = "dr")
- Prof. | Prof. (ID = "prof")
- Herr Dr. | Mr. Dr. (ID = "mr-dr")
- Frau Dr. | Ms. Dr. (ID = "ms-dr")
- Herr Prof. | Mr. Prof. (ID = "mr-prof")
- Frau Prof. | Ms. Prof. (ID = "ms-prof")
- Herr Prof. Dr. | Mr. Prof. Dr. (ID = "mr-prof-dr")
- Frau Prof. Dr. | Ms. Prof. Dr. (ID = "ms-prof-dr")

Involvement types and their IDs are these:

<!--
from ruhrbuehnen.apps.people.models import InvolvementType 
its = InvolvementType.objects.all()
for it in its:
    print u'- {0} | {1} (ID = "{2}")'.format(it.title_de, it.title_en, it.slug)
-->

- Ausstatter/-in | Decorator (ID = "ausstatter")
- Bühnenbildner/-in | Scene builder (ID = "buhnenbildner")
- Chor | Choir (ID = "chor")
- Choreografie | Choreography (ID = "choreografie")
- Dirigent/ -in | Director of an orchestra, chorus (ID = "dirigent")
- Diskussionsteilnehmer/ -in | Discussant (ID = "diskussionsteilnehmer")
- Dramaturgie | Dramaturgy (ID = "dramaturgie")
- Einrichtung | arrangement (ID = "einrichtung")
- Einstudierung | Rehearsal (ID = "einstudierung")
- Ensemble | Ensemble (ID = "ensemble")
- Inspizient / -in | Stage caller (ID = "inspizient")
- Klangregie | Sound Direction (ID = "klangregie")
- Kostüme | Costumes (ID = "kostume")
- Künstler/ -in | Artist (ID = "kuenstler")
- Künstlerische Leitung | Artistic director (ID = "kunstlerische-leitung")
- Licht | Light (ID = "licht")
- Moderator/-in | Moderator (ID = "moderator")
- Musik | Music (ID = "musik")
- Orchester | Orchestra (ID = "orchester")
- Performer/-in |  (ID = "performer")
- Produktionsleitung | Production Managment (ID = "produktionsleitung")
- Pyrothechnik | Pyrotechnic (ID = "pyrothechnik")
- Referent/-in | Speaker (ID = "referent")
- Regie | Direction (ID = "regie")
- Regieassistenz | Direction assistence (ID = "regieassistenz")
- Requisite | Prop (ID = "requisite")
- Rezitation | Reciting (ID = "rezitation")
- Sänger/-in | Singer (ID = "saenger")
- Schauspieler / -in | Actor (ID = "schauspieler")
- Solist/-in | Soloist (ID = "solist")
- Souffleur/Souffleuse | Prompter (ID = "souffleur-souffleuse")
- Statisterie | Background actor (ID = "statisterie")
- Tänzer/-in | Dancer (ID = "taenzer")
- Text | Text (ID = "text")
- Video | Video (ID = "video")

For example, the leaders, authors and participants can be defined like this:

```json
"leaders": [
    {
        "prefix_id": "ms-dr",
        "first_name": "Erika",
        "last_name": "Mustermann",
        "function_de": "Direktorin",
        "function_en": "Director",
        "sort_order": 1
    }
],
"authors": [ 
    {
        "prefix_id": "mr",
        "first_name": "Max",
        "last_name": "Mustermann",
        "authorship_type_id": "komponist",
        "sort_order": 1
    }
],
"participants": [
    {
        "first_name": "Otto",
        "last_name": "Normalverbraucher",
        "involvement_type_id": "musik"
        "instrument_de": "Klavier",
        "instrument_en": "Piano",
        "sort_order": 1
    },
    {
        "first_name": "Lieschen",
        "last_name": "Müller"
        "involvement_type_id": "schauspieler",
        "role_de": "Rotkäppchen",
        "role_en": "Little Red Riding Hood",
        "sort_order": 2
    }
]
```

### Videos, Live Streams, Images, and PDF Documents for Productions or Events ###

The `"videos"` object contains a list of `video` objects with such content:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"creation_date"`| dateTime | yes | Creation timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"modified_date"` | dateTime | no | Modification timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"title_de"` | string | yes | Title in German | |
| `"title_en"` | string | yes | Title in English | |
| `"embed"` | string | yes | HTML embed code | `"<iframe src=\"http://example.com/videos/45645/embed/\"></iframe>"` |
| `"sort_order"` | integer | yes | Sort order of the video | 1 |

The `"live_streams"` object contains a list of `live_stream` objects with such content:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"creation_date"`| string | yes | Creation timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"modified_date"` | string | no | Modification timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"title_de"` | string | yes | Title in German | |
| `"title_en"` | string | yes | Title in English | |
| `"embed"` | string | yes | HTML embed code | `"<iframe src=\"http://example.com/live-videos/45645/embed/\"></iframe>"` |
| `"sort_order"` | integer | yes | Sort order of the video | 1 |

The `"images"` object contains a list of `image` objects with such content:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"creation_date"`| string | yes | Creation timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"modified_date"` | string | no | Modification timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"url"` | URL | yes | URL of the original (large-scale) image | |
| `"title_de"` | string | yes | Title in German | |
| `"title_en"` | string | yes | Title in English | |
| `"description_de"` | string | no | Plain-text description in German | |
| `"description_en"` | string | no | Plain-text description in English | |
| `"author"` | string | no | The name of the author | |
| `"copyright_restrictions"` | string | yes | Permissions to use this photo. One of: "general_use" or "protected" | "general_use" |
| `"copyright"` | string | no | Copyright information | "© 2016 example.com" |
| `"sort_order"` | integer | yes | Sort order of the video | 1 |

The `"pdfs"` object contains a list of `pdf` objects with such content:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"creation_date"`| string | yes | Creation timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"modified_date"` | string | no | Modification timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"url"` | URL | yes | URL of the PDF document | |
| `"title_de"` | string | yes | Title in German | |
| `"title_en"` | string | yes | Title in English | |
| `"description_de"` | string | no | Plain-text description in German | |
| `"description_en"` | string | no | Plain-text description in English | |
| `"author"` | string | no | The name of the author | |
| `"copyright"` | string | no | Copyright information | "© 2016 example.com" |
| `"sort_order"` | integer | yes | Sort order of the video | 1 |

For example, videos, live streams, images, and PDF documents can be defined like this:

```json
"videos": [
    {
        "creation_date": ""2016-04-14T16:27:38"",
        "modified_date": ""2016-04-14T16:27:38"",
        "title_de": "",
        "title_en": "",
        "embed": "<iframe src=\"http://example.com/videos/45645/embed/\"></iframe>",
        "sort_order": 1
    }
],
"live_streams": [
    {
        "creation_date": ""2016-04-14T16:27:38"",
        "modified_date": ""2016-04-14T16:27:38"",
        "title_de": "",
        "title_en": "",
        "embed": "<iframe src=\"http://example.com/videos/45645/embed/\"></iframe>",
        "sort_order": 1
    }
],
"images": [
    {
        "creation_date": ""2016-04-14T16:27:38"",
        "modified_date": ""2016-04-14T16:27:38"",
        "url": "http://example.com/media/589231.jpg",
        "title_de": "",
        "title_en": "",
        "description_de": "",
        "description_en": "",
        "author": "",
        "copyright_restrictions": "general_use",
        "copyright": "© 2016 example.com",
        "sort_order": 1
    }
],
"pdfs": [
    {
        "creation_date": ""2016-04-14T16:27:38"",
        "modified_date": ""2016-04-14T16:27:38"",
        "url": "http://example.com/media/564285.pdf",
        "title_de": "",
        "title_en": "",
        "description_de": "",
        "description_en": "",
        "author": "",
        "copyright": "© 2016 example.com",
        "sort_order": 1
    }
]
```

### Social media for Productions ###

The `"social_media"` object contains a list of `social_media_channel` objects with such content:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"channel_type"` | NCName | yes | Type of social media: "Facebook", "Twitter", "Google+", etc. | "Facebook" |
| `"url"` | URL | yes | URL of social media profile | "https://www.facebook.com/ruhrbuehnen" |

For example, Twitter and Facebook profiles for the production can be defined like this:

```json
"social_media": [
    {
        "channel_type": "Twitter",
        "url": "https://twitter.com/ruhrbuehnen"
    },
    {
        "channel_type": "Facebook",
        "url": "https://www.facebook.com/ruhrbuehnen"
    }
],
```

### Language and subtitles for Productions or Events ###

This is a list of choices for the `"language_and_subtitles_id"` object:

<!--
from ruhrbuehnen.apps.productions.models import LanguageAndSubtitles
ls = LanguageAndSubtitles.objects.all()
for l in ls:
    print u'- {0} | {1} (ID = "{2}")'.format(l.title_de, l.title_en, l.slug)
-->

- Sprache kein Problem | Language no Problem (ID = "sprache-kein-problem")
- In englischer Sprache | In English (ID = "in-englischer-sprache")
- Mit englischen Übertiteln | With English surtitles (ID = "mit-engl-uebertiteln")
- Mit französischen Übertiteln | With French surtitles (ID = "mit-franzoesischen-uebertiteln")
- Andere Sprache | Other Languages (ID = "andere-sprache")
- Simultanübersetzung englisch-deutsch | Simultaneous translation English-German (ID = "simultanubersetzung-englisch-deutsch")
- In deutscher Sprache | In German (ID = "in-deutscher-sprache")

For example, if you want to tell that the language for production doesn't matter, you would use such key and value:

```json
"language_and_subtitles_id": "sprache-kein-problem",
```

### Sponsors for Productions or Events ###

The `"sponsors"` object contains a list of `sponsor` objects with such content:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"creation_date"`| string | yes | Creation timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"modified_date"` | string | no | Modification timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"website"` | URL | no | URL of the sponsor website | "http://example.com/sponsor/" |
| `"image_url"` | URL | no | URL of the sponsor logo in JPG or PNG format | "http://example.com/media/sponsor-logo.png" |
| `"title_de"` | string | no | Title in German | &nbsp; |
| `"title_en"` | string | no | Title in English | &nbsp; |

For example, a sponsor can be defined like this:

```json
"sponsors": [
    {
        "creation_date": ""2016-04-14T16:27:38"",
        "modified_date": ""2016-04-14T16:27:38"",
        "website": "http://example.com/sponsor/",
        "image_url": "http://example.com/media/sponsor-logo.png",
        "title_de": "Beispiel Sponsor",
        "title_en": "Example Sponsor"
    }
]
```

## Events ##

Events are specific dates and times when production is happening. If event's keys match production's keys, they will overwrite production's data, otherwise the value from the production will be used at the Ruhr Bühnen website. The `"events"` key contains a list of `event` objects.

### The Event Object ###

These elements are available for the `event` object:

| Object | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `"id"` | string or integer | yes | Unique event ID on your website | 123 |
| `"creation_date"`| string | yes | Production creation timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"modified_date"` | string | no | Production modification timestamp in ISO 8601 format | "2016-04-14T16:27:38" |
| `"start_date"`| string | yes | Start date in ISO 8601 format | "2016-04-14" |
| `"end_date"`| string | no | End date in ISO 8601 format | "2016-04-14" |
| `"start_time"`| string | yes | Start time in HH:MM or HH:MM:SS format | "20:00" |
| `"end_time"`| string | no | End time in HH:MM or HH:MM:SS format | "23:00" |
| `"duration"`| string | no | Duration time in H:MM or H:MM:SS format | "3:00" |
| `"pauses"`| integer | no | Amount of pauses | 2 |
| `"play_locations"` | list of location IDs | no | Theaters where this event takes place | |
| `"play_stages"` | list of stage IDs | no | Stages where this event takes place | |
| `"location_title"` | string | no | Location title (if `"play_locations"` is empty) | |
| `"street_address"`| string | no | Street address (first line) of the location (if `"play_locations"` is empty) | |
| `"street_address2"` | string | no | Street address (second line) of the location (if `"play_locations"` is empty) | |
| `"postal_code"`| string | no | Postal code of the location (if `"play_locations"` is empty) | |
| `"city"`| string | no | City of the location (if `"play_locations"` is empty) | |
| `"latitude"`| string | no | Latitude of the location (if `"play_locations"` is empty) | "52.5192" |
| `"longitude"` | string | no | Longitude of the location (if `"play_locations"` is empty) | "13.4061" |
| `"organizers"` | string | no | Organizer or organizers of this event | |
| `"description_de"` | string | no | Plain-text description in German | |
| `"description_en"` | string | no | Plain-text description in English | |
| `"teaser_de"` | string | no | Plain-text teaser in German | |
| `"teaser_en"` | string | no | Plain-text teaser in English | |
| `"work_info_de"` | string | no | Plain-text work info in German | |
| `"work_info_en"` | string | no | Plain-text work info in English | |
| `"contents_de"` | string | no | Plain-text contents in German | |
| `"contents_en"` | string | no | Plain-text contents in English | |
| `"press_text_de"` | string | no | Plain-text press text in German | |
| `"press_text_en"` | string | no | Plain-text press text in English | |
| `"credits_de"` | string | no | Plain-text credits in German | |
| `"credits_en"` | string | no | Plain-text credits in English | |
| `"concert_program_de"` | string | no | Plain-text concert program in German | |
| `"concert_program_en"` | string | no | Plain-text concert program in English | |
| `"supporting_program_de"` | string | no | Plain-text supporting program in German | |
| `"supporting_program_en"` | string | no | Plain-text supporting program in English | |
| `"remarks_de"` | string | no | Plain-text remarks in German | |
| `"remarks_en"` | string | no | Plain-text remarks in English | |
| `"duration_text_de"` | string | no | Plain-text information about duration in German | |
| `"duration_text_en"` | string | no | Plain-text information about duration in English | |
| `"subtitles_text_de"` | string | no | Plain-text information about subtitles in German | |
| `"subtitles_text_en"` | string | no | Plain-text information about subtitles in English | |
| `"age_text_de"` | string | no | Plain-text information about the age of the audience in German | |
| `"age_text_en"` | string | no | Plain-text information about the age of the audience in English | |
| `"free_entrance"` | string | no | Is the entrance free? One of "true" or "false" | "false" |
| `"price_from"` | string | no | Price from in Euros (no currency sign included) | "8.00" |
| `"price_till"` | string | no | Price till in Euros (no currency sign included) | "12.00" |
| `"tickets_website"` | URL | no | The URL of a website page where you can buy tickets to this event | "http://example.com/tickets/" |
| `"price_information_de"` | string | no | Additional plain-text information about prices in German | |
| `"price_information_en"` | string | no | Additional plain-text information about prices in English | |
| `"event_status"` | string | yes | Event status. One of: "`takes_place`", or "`canceled`" | "takes_place" |
| `"ticket_status"` | string | no | Tickets' status. One of: "`tickets_@_box_office`" or "`sold_out`" | "tickets_@_box_office" |
| `"characteristics"`| list of characteristic IDs | no | Event characteristics |  |
| `"leaders"` | list of `leader` objects | no | Leaders | |
| `"authors"` | list of `author` objects | no | Authors | |
| `"participants"` | list of `participant` objects | no | Participants | |
| `"videos"` | list of `video` objects | no | Videos | |
| `"live_streams"` | list of `live_stream` objects | no | Live streams | |
| `"images"` | list of `image` objects | no | Images | |
| `"pdfs"` | list of `pdf` objects | no | PDF documents | |
| `"language_and_subtitles_id"` | string | no | Language and subtitles | "in-deutscher-sprache" |
| `"sponsors"` | list of `sponsor` objects | no | Sponsors | |
| `"classiccard"` | string | no | Intended for ClassicCard holders. One of “true” or “false” | "false" |

### The Event Characteristics ###

This is a list of all available characteristics with IDs to enter as values at `"characteristic_id"` of the event:

<!--
from ruhrbuehnen.apps.productions.models import EventCharacteristics
es = EventCharacteristics.objects.all()
for e in es:
    print u'- {0} | {1} (ID = "{2}")'.format(e.title_de, e.title_en, e.slug)
-->

- Premiere | Premiere (ID = "premiere")
- Deutsche Erstaufführung | Premiere in Germany (ID = "deutsche-erstauffuehrung")
- Deutschsprachige Erstaufführung | Premiere in German (ID = "deutschsprachige-erstauffuehrung")
- Voraufführung | Preview (ID = "vorauffuehrung")
- zum letzten Mal in dieser Spielzeit | For the last time in the repertory season (ID = "zum-letzten-mal-dieser-spielzeit")
- zum letzten Mal | For the last time (ID = "zum-letzten-mal")
- Einführung | Introduction (ID = "einfuehrung")
- Familienpreise | Family prices (ID = "familienpreise")

For example, if an event can be classified as "Premiere" and "Familienpreise", the following keys and values should be set:

```json
"characteristics": ["premiere", "familienpreise"],
```

## Full featured JSON example ##

Finally, you can see the complete [JSON example](example.json).
