# Production Import Specification #

Last update: February 20, 2018

[TOC]

## Introduction ##

The Berlin Bühnen website has locations (theaters) and stages where plays happen. All plays are named as productions. Productions have general information about the play. Each production has multiple events, that is, exact dates and times when the play happens. Events might overwrite some general information of their production.

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
| `"language_and_subtitles_id"` | string | no | Language and subtitles | "sprache-kein-problem" |
| `"sponsors"` | list of `sponsor` objects | no | Sponsors | |
| `"events"` | list of `event` objects | no | Events | |
| `"classiccard"` | string | no | Intended for ClassicCard holders. One of “true” or “false” | "false" |

### The Locations and Stages for Productions or Events ###

This is a list of all available locations and stages with location IDs and stage IDs to enter as values at `"location_id"` and `"stage_id"`:

<!--
from berlinbuehnen.apps.locations.models import Location
ls = Location.objects.filter(status='published')
for l in ls:
    print u'- {0} (Location ID = {1})'.format(l.title, l.pk)
    for s in l.stage_set.all():
        print u'  - {0} (Stage ID = {1})'.format(s.title, s.pk)        
-->

- Acker Stadt Palast (Location ID = 68)
- ACUD Theater (Location ID = 69)
- Admiralspalast (Location ID = 53)
  - F101 (Stage ID = 26)
  - Studio (Stage ID = 28)
  - Theater (Stage ID = 25)
- Astrid Lindgren Bühne im FEZ-Berlin (Location ID = 129)
- ATZE Musiktheater (Location ID = 43)
  - Großer Saal (Stage ID = 151)
  - Studiobühne (Stage ID = 150)
- aufBruch KUNST GEFÄNGNIS STADT (Location ID = 156)
- Ballhaus Naunynstraße (Location ID = 40)
- Ballhaus Ost (Location ID = 19)
- BAR JEDER VERNUNFT (Location ID = 8)
- Berghain (Location ID = 145)
- Berliner Compagnie (Location ID = 178)
- Berliner Ensemble (Location ID = 24)
  - Großes Haus (Stage ID = 203)
  - Kleines Haus (Stage ID = 21)
  - Salon (Stage ID = 20)
  - Werkraum (Stage ID = 205)
- Berliner Festspiele (Location ID = 80)
  - A-Trane (Stage ID = 147)
  - Akademie der Künste (Stage ID = 148)
  - Haus der Berliner Festspiele (Stage ID = 32)
  - Haus der Berliner Festspiele, Gartenbühne (Stage ID = 122)
  - Haus der Berliner Festspiele, Große Bühne (Stage ID = 121)
  - Haus der Berliner Festspiele, Kassenhalle (Stage ID = 100)
  - Haus der Berliner Festspiele, Oberes Foyer (Stage ID = 89)
  - Haus der Berliner Festspiele, Seitenbühne (Stage ID = 88)
  - Kaiser-Wilhelm-Gedächtnis-Kirche Berlin (Stage ID = 149)
  - Kraftwerk Berlin (Stage ID = 157)
  - Martin-Gropius-Bau (Stage ID = 41)
  - Mazen Kerbaj, Bundesallee (Stage ID = 156)
- Berliner Kindertheater (Location ID = 76)
  - Fontane-Haus im Märkischen Viertel (Stage ID = 90)
  - Freilichtbühne an der Zitadelle Spandau (Stage ID = 40)
- Berliner Kriminal Theater (Location ID = 48)
- Berliner Philharmonie (Location ID = 65)
  - Foyer im Kammermusiksaal (Stage ID = 42)
  - Großer Saal (Stage ID = 39)
  - Hermann-Wolff-Saal (Stage ID = 59)
  - Kammermusiksaal (Stage ID = 29)
  - Mailand, Expo - La Scala (Stage ID = 60)
  - München, Philharmonie im Gasteig (Stage ID = 57)
  - Philharmonie – Karl-Schuke-Orgel (Stage ID = 58)
  - Philharmonie und Kammermusiksaal (Stage ID = 62)
  - Wien, Musikverein (Stage ID = 61)
- BKA Theater (Location ID = 21)
- Blackmore's - Berlins Musikzimmer (Location ID = 168)
- Brotfabrik (Location ID = 70)
- Chamäleon Theater (Location ID = 60)
- Corbo Kleinkunstbühne (Location ID = 45)
- Das Weite Theater (Location ID = 71)
- Deutsche Oper Berlin (Location ID = 28)
  - Foyer (Stage ID = 37)
  - Restaurant (Stage ID = 102)
  - Restaurant Deutsche Oper (rdo) (Stage ID = 38)
  - Tischlerei Deutsche Oper Berlin (Stage ID = 45)
- Deutsches Theater Berlin (Location ID = 3)
  - Box und Bar (Stage ID = 1)
  - Kammerspiele (Stage ID = 2)
  - Saal (Stage ID = 3)
- Die Stachelschweine - Kabarett-Theater im Europa-Center (Location ID = 78)
- Die Wühlmäuse (Location ID = 16)
- DISTEL Kabarett-Theater (Location ID = 31)
  - DISTEL-Studio (Stage ID = 35)
  - Kabarett-Theater DISTEL (Stage ID = 79)
- DOCK 11 (Location ID = 157)
  - EDEN***** (Stage ID = 142)
- Dussmann das KulturKaufhaus GmbH (Location ID = 165)
- Elbphilharmonie und Laeiszhalle (Location ID = 187)
- English Theatre Berlin | International Performing Arts Center (Location ID = 58)
- Friedrichstadt-Palast Berlin (Location ID = 39)
- Galli Theater Berlin (Location ID = 77)
- Gästehaus Blumenfisch am Großen Wannsee (Location ID = 147)
- Gethsemanekirche (Location ID = 141)
- Gorki Brinkmannzimmer (Location ID = 169)
- GRIPS Theater (Location ID = 79)
  - GRIPS Hansaplatz (Stage ID = 31)
  - GRIPS Podewil (Stage ID = 47)
- Große Orangerie Schloss Charlottenburg (Location ID = 74)
  - Große Orangerie Schloss Charlottenburg (Stage ID = 70)
- Großer Sendesaal des RBB (Location ID = 176)
- HALLE TANZBÜHNE BERLIN (Location ID = 184)
- Hamburger Bahnhof (Location ID = 182)
- HAU Hebbel am Ufer (Location ID = 13)
  - HAU 1 in the Upper Foyer (Stage ID = 126)
  - HAU1 (Stage ID = 11)
  - HAU1 Installation (Stage ID = 128)
  - HAU1+2 (Stage ID = 124)
  - HAU2 (Stage ID = 12)
  - HAU2 Foyer (Stage ID = 127)
  - HAU2 Installation (Stage ID = 123)
  - HAU2 Outdoors (Stage ID = 130)
  - HAU3 (Stage ID = 13)
  - HAU3 Houseclub (Stage ID = 129)
  - Privatwohnungen in Berlin (Stage ID = 131)
  - Relexa Hotel (Stage ID = 132)
  - WAU im HAU2 (Stage ID = 125)
  - WAU Wirtshaus am Ufer (Stage ID = 30)
- Haus der Kulturen der Welt (Location ID = 26)
- Heimathafen Neukölln (Location ID = 34)
- Inseltheater Moabit (Location ID = 135)
- Kino Babylon (Location ID = 174)
- Kleines Theater (Location ID = 55)
- Komische Oper Berlin (Location ID = 5)
- Konzerthaus Berlin (Location ID = 14)
  - Carl-Maria-von-Weber-Saal (Stage ID = 146)
  - Eingangsfoyer (Stage ID = 145)
  - Großer Saal (Stage ID = 15)
  - Kleiner Saal (Stage ID = 16)
  - Konzerthaus Berlin (Stage ID = 143)
  - Ludwig-van-Beethoven-Saal (Stage ID = 18)
  - Musikclub (Stage ID = 17)
  - Philharmonie Berlin - Großer Saal (Stage ID = 144)
  - Werner-Otto-Saal (Stage ID = 14)
- Köpenicker Rathaushof Theater (Location ID = 167)
- Kühlhaus am Gleisdreieck (Location ID = 146)
- Kultur- und Kongresszentrum Luzern (Location ID = 190)
- Kulturhaus Karlshorst (Location ID = 163)
- Landesmusikakademie Berlin (Location ID = 63)
- Literatur Festival (Location ID = 144)
- Lokhalle Südgelände (Location ID = 189)
- Maxim Gorki Theater (Location ID = 12)
  - Foyer (Stage ID = 34)
  - Gorki Foyer Berlin (Stage ID = 9)
  - Gorki Theater (Stage ID = 33)
  - Marmorsaal (Stage ID = 213)
  - Studio Я (Stage ID = 10)
  - Vorplatz GORKI (Stage ID = 69)
- Märchenhütte (Location ID = 186)
- Monbijou Theater (Location ID = 186)
  - Amphitheater (Stage ID = 165)
  - Jacob-Hütte (Stage ID = 166)
  - Wilhelm-Hütte (Stage ID = 167)
- Museum für Naturkunde Berlin (Location ID = 162)
- Neuköllner Oper (Location ID = 54)
  - Saal/Studio (Stage ID = 81)
- Parochialkirche (Location ID = 164)
- Pfefferberg Theater (Location ID = 172)
- Philharmonie Berlin (Location ID = 171)
- Pierre Boulez Saal (Location ID = 193)
- Podewil (Location ID = 150)
  - Foyer (Stage ID = 162)
  - Großer Saal (GRIPS) (Stage ID = 160)
  - Tanzstudio (Stage ID = 161)
- RADIALSYSTEM V (Location ID = 29)
- Renaissance-Theater Berlin (Location ID = 23)
  - Renaissance-Theater Berlin (Stage ID = 103)
  - Renaissance-Theater Berlin / Bruckner-Foyer (Stage ID = 23)
- Salzburger Festspiele (Location ID = 148)
- SCHAUBUDE BERLIN (Location ID = 51)
  - SCHAUBUDE BERLIN (Stage ID = 71)
- Schaubühne am Lehniner Platz (Location ID = 49)
- Schloss Charlottenburg (Location ID = 159)
- Schlosspark Theater (Location ID = 15)
- Shakespeare Company Berlin (Location ID = 161)
  - Natur-Park Schöneberger Südgelände (Stage ID = 164)
- Sophiensæle (Location ID = 4)
  - Festsaal (Stage ID = 4)
  - gesamtes Haus (Stage ID = 49)
  - Hochzeitssaal (Stage ID = 5)
  - Kantine (Stage ID = 48)
- St. Johannes-Evangelist-Kirche (Location ID = 188)
- Staatsballett Berlin (Location ID = 75)
  - Deutsche Oper Berlin (Stage ID = 75)
  - Komische Oper Berlin (Stage ID = 77)
  - Staatsoper Unter den Linden (Stage ID = 76)
- Staatskapelle Berlin (Location ID = 197)
- Staatsoper Unter den Linden (Location ID = 9)
  - Gläsernes Foyer (Stage ID = 22)
  - Bebelplatz (Stage ID = 56)
  - Bode Museum (Stage ID = 44)
  - Werkstatt (Stage ID = 24)
  - Probebühne I (Stage ID = 53)
  - Staatsoper Unter den Linden (Stage ID = 46)
- Stage BLUEMAX Theater (Location ID = 61)
- Stage Theater am Potsdamer Platz (Location ID = 57)
- Stage Theater des Westens (Location ID = 59)
- TAK Theater im Aufbau Haus (Location ID = 133)
- Testbühne Cinemarketing (Location ID = 143)
- testbühne für invite (Location ID = 67)
- Teststage 2 (Location ID = 134)
- Theater an der Parkaue (Location ID = 42)
  - Bühne 1 (Stage ID = 84)
  - Bühne 1 - Hinterbühne (Stage ID = 86)
  - Bühne 2 (Stage ID = 27)
  - Bühne 3 (Stage ID = 85)
  - Deutsche Oper - Tischlerei (Stage ID = 140)
  - Kulturhaus Karlshorst (Saal) (Stage ID = 139)
  - Prater (Stage ID = 141)
  - Studiobühne (Stage ID = 87)
- Theater Anu (Location ID = 154)
  - Berlin Tempelhofer Feld (Stage ID = 138)
- Theater auf der Zitadelle (Location ID = 185)
- Theater im Palais (Location ID = 32)
- Theater Morgenstern (Location ID = 38)
  - Rathaus Friedenau (Stage ID = 133)
- Theater O-TonArt (Location ID = 20)
- Theater o.N. (Location ID = 181)
- Theater RambaZamba (Location ID = 166)
- Theater Strahl (Location ID = 72)
  - STRAHL.Die Weiße Rose (Stage ID = 171)
  - STRAHL.Halle Ostkreuz (Stage ID = 173)
  - STRAHL.Probebühne (Stage ID = 172)
- Theater Thikwa (Location ID = 22)
- Komödie am Kurfürstendamm im Schiller Theater (Location ID = 25)
- Theater unterm Dach (Location ID = 73)
- Theaterdiscounter (Location ID = 2)
- Theaterforum Kreuzberg (Location ID = 173)
- Theaterhaus Berlin Mitte (Location ID = 132)
  - OPEN AIR BÜHNE (Stage ID = 174)
  - ROOM 207 (Stage ID = 169)
  - ROOM 403 (Stage ID = 168)
  - SOMMERGARTEN (Stage ID = 170)
  - WERKSTATTBÜHNE 003 (Stage ID = 159)
- Theater Zukunft (Location ID = 192)
- TIPI AM KANZLERAMT (Location ID = 7)
- UdK - Universität der Künste Berlin (Location ID = 142)
- ufaFabrik (Location ID = 56)
  - Open Air Bühne im überdachten Sommergarten (Stage ID = 182)
  - Theatersaal (Stage ID = 179)
  - Varieté Salon (Stage ID = 180)
  - Wolfgang Neuss Salon (Stage ID = 181)
- Uferstudios (Location ID = 66)
  - Heizhaus (Stage ID = 120)
  - Uferstudio 1 (Stage ID = 105)
  - Uferstudio 10 (Stage ID = 114)
  - Uferstudio 11 (Stage ID = 115)
  - Uferstudio 12 (Stage ID = 116)
  - Uferstudio 13 (Stage ID = 117)
  - Uferstudio 14 (Stage ID = 118)
  - Uferstudio 16 (Stage ID = 119)
  - Uferstudio 2 (Stage ID = 106)
  - Uferstudio 3 (Stage ID = 107)
  - Uferstudio 4 (Stage ID = 108)
  - Uferstudio 5 (Stage ID = 109)
  - Uferstudio 6 (Stage ID = 110)
  - Uferstudio 7 (Stage ID = 111)
  - Uferstudio 8 (Stage ID = 112)
  - Uferstudio 9 (Stage ID = 113)
- UNI.T - Theater der UdK Berlin (Location ID = 130)
- Vaganten Bühne (Location ID = 33)
- Volksbühne Berlin (Location ID = 6)
  - 3\. Stock (Stage ID = 8)
  - Books (Stage ID = 83)
  - Großes Haus (Stage ID = 82)
  - Grüner Salon (Stage ID = 6)
  - Roter Salon (Stage ID = 7)
  - Sternfoyer (Stage ID = 101)
  - Tempelhof Hangar 5 (Stage ID = 207)
  - Fullscreen (Stage ID = 208)
- Wintergarten Varieté (Location ID = 180)
- Young Euro Classic (Location ID = 158)
- ZIONSKIRCHE (Location ID = 152)
- Zitadelle (Location ID = 149)

For example, if a production is organized by "Volksbühne Berlin" and happens in the "Grüner Salon" stage, the following keys and values should be set:

```json
"in_program_of": [6],
"play_stages": [6],
```

### The Categories for Productions ###

This is a list of all available categories and subcategories with IDs to enter as values at `"category_id"`:

<!--
>>> from berlinbuehnen.apps.productions.models import ProductionCategory
>>> cs = ProductionCategory.objects.filter(parent=None)
>>> for c in cs:
    print u'- {0} | {1} (Category ID = {2})'.format(c.title_de, c.title_en, c.pk)
    for s in c.children.all():
        print u'  - {0} | {1} (Category ID = {2})'.format(s.title_de, s.title_en, s.pk)
-->

- Schauspiel | Theatre (Category ID = 1)
  - Boulevardtheater | Boulevard Theatre (Category ID = 11)
  - Dokumentarisches Theater | Documentary Theatre (Category ID = 12)
  - Improvisationstheater | Improvisation Theatre (Category ID = 13)
  - Schauspiel | Theatre (Category ID = 16)
- Musiktheater | Music Theater (Category ID = 2)
  - Oper | Opera (Category ID = 20)
  - Operette | Operetta (Category ID = 22)
  - Zeitgenössische Oper | Contemporary Opera (Category ID = 24)
  - Musiktheater | Music Theatre (Category ID = 19)
  - Singspiel | Singing Play (Category ID = 23)
  - Musical | Musical (Category ID = 18)
  - Konzertante Aufführung | Concert Performance (Category ID = 17)
- Tanz | Dance (Category ID = 3)
  - Ballet | Ballet (Category ID = 25)
  - Zeitgenössischer Tanz | Contemporary Dance (Category ID = 29)
  - Urban Dance | Urban Dance (Category ID = 28)
  - Tanztheater | Dance Theatre (Category ID = 27)
- Performance | Performance (Category ID = 4)
  - Cross Media | Cross Media (Category ID = 30)
  - Lecture Performance | Lecture Performance (Category ID = 31)
  - Performance | Performance (Category ID = 32)
  - Installation | Installation (Category ID = 34)
- Konzert | Concert (Category ID = 5)
  - Sinfoniekonzert | Symphony Concert (Category ID = 89)
  - Klassik | Classic (Category ID = 43)
  - Kammermusik | Chamber Music (Category ID = 90)
  - Liederabend | Song Recital (Category ID = 44)
  - Neue Musik | New Music (Category ID = 45)
  - A cappella | A cappella (Category ID = 94)
  - Blues | Blues (Category ID = 35)
  - Chanson | Chanson (Category ID = 36)
  - Country | Country (Category ID = 37)
  - Elektronische Musik | Electronic Music (Category ID = 38)
  - Folk | Folk (Category ID = 39)
  - Funk | Funk (Category ID = 40)
  - Hip Hop | Hip Hop (Category ID = 41)
  - Schlager | Schlager (Category ID = 93)
  - Jazz | Jazz (Category ID = 42)
  - Pop | Pop (Category ID = 46)
  - Rock | Rock (Category ID = 47)
  - Soul | Soul (Category ID = 48)
  - Crossover | Crossover (Category ID = 49)
  - World Music | World Music (Category ID = 50)
- Comedy & Kabarett | Comedy & Cabaret (Category ID = 7)
  - Comedy | Comedy (Category ID = 56)
  - Kabarett | Cabaret (Category ID = 57)
- Entertainment | Entertainment (Category ID = 6)
  - Show | Spectacular (Category ID = 53)
  - Revue | Revue (Category ID = 52)
  - Varieté | Varieté (Category ID = 54)
  - Burlesque | Burlesque (Category ID = 88)
  - New Circus | New Circus (Category ID = 51)
  - Zirkus | Circus (Category ID = 55)
- Figurentheater | Figure Theater (Category ID = 62)
  - Puppentheater | Puppet Theater (Category ID = 66)
  - Figurentheater | Figure Theater (Category ID = 84)
  - Objekttheater | Object Theater (Category ID = 65)
- Kinder & Jugend | Children & Youth (Category ID = 8)
  - Jugend (ab  14 Jahre) | Youth (from 14 years old) (Category ID = 63)
  - Kinder (bis 13 Jahre) | Children (till 13 years old) (Category ID = 64)
  - Kleinkind (bis 6 Jahre) | Young children (till 6 years old) (Category ID = 91)
  - Kleinstkind (bis 2 Jahre) | Toddlers (till 2 years old) (Category ID = 92)
- Literatur | Literature (Category ID = 86)
  - Lesung | Reading (Category ID = 15)
  - Poetry Slam | Poetry Slam (Category ID = 87)
  - Szenische Lesung | Staged Reading (Category ID = 85)
- Diskurs | Discourse (Category ID = 9)
  - Gespräch | Conversation (Category ID = 83)
  - Diskussion | Discussion (Category ID = 68)
  - Konferenz | Conference (Category ID = 69)
  - Lecture Performance | Lecture Performance (Category ID = 70)
  - Symposium | Symposium (Category ID = 71)
  - Tagung | Meeting (Category ID = 72)
  - Vortrag | Lecture (Category ID = 73)
- Sonstiges | Other (Category ID = 10)
  - Ausstellung | Exhibition (Category ID = 74)
  - Fest | Feast (Category ID = 75)
  - Film/Video | Film / Video (Category ID = 76)
  - Fotografie | Photography (Category ID = 77)
  - Führung | Guided tour (Category ID = 78)
  - Neue Medien | New Media (Category ID = 79)
  - Party | Party (Category ID = 80)
  - Spezial | Special (Category ID = 81)
  - Workshop | Workshop  Action (Category ID = 82)

For example, if a production can be classified as "Tanz", "Ballet", and "Neue Medien" (under "Sonstiges"), the following key and value should be set:

```json
"categories": [3, 25, 10, 79],
```
### The Production Characteristics ###

This is a list of all available characteristics with IDs to enter as values at `"characteristic_id"` of the production:

<!--
>>> from berlinbuehnen.apps.productions.models import ProductionCharacteristics
>>> ps = ProductionCharacteristics.objects.all()
>>> for p in ps:
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
>>> from berlinbuehnen.apps.people.models import Prefix 
>>> ps = Prefix.objects.all()
>>> for p in ps:
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
>>> from berlinbuehnen.apps.people.models import InvolvementType 
>>> its = InvolvementType.objects.all()
>>> for it in its:
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
- Kostüme | Costumes (ID = "kostume")
- Künstler/ -in | Artist (ID = "kuenstler")
- Künstlerische Leitung | Artistic director (ID = "kunstlerische-leitung")
- Licht | Light (ID = "licht")
- Moderator/-in | Moderator (ID = "moderator")
- Musik | Music (ID = "musik")
- Orchester | Orchestra (ID = "orchester")
- Performer/-in |  (ID = "performer")
- Produktionsleitung |  (ID = "produktionsleitung")
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
| `"url"` | URL | yes | URL of the original (large-scale) image. Must end with the file extension ".jpg" or ".png" | |
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
| `"url"` | URL | yes | URL of the PDF document. Must end with the file extension ".pdf" | |
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
| `"url"` | URL | yes | URL of social media profile | "https://www.facebook.com/berlinbuehnen" |

For example, Twitter and Facebook profiles for the production can be defined like this:

```json
"social_media": [
    {
        "channel_type": "Twitter",
        "url": "https://twitter.com/berlinbuehnen"
    },
    {
        "channel_type": "Facebook",
        "url": "https://www.facebook.com/berlinbuehnen"
    }
],
```

### Language and subtitles for Productions or Events ###

This is a list of choices for the `"language_and_subtitles_id"` object:

<!--
>>> from berlinbuehnen.apps.productions.models import LanguageAndSubtitles
>>> ls = LanguageAndSubtitles.objects.all()
>>> for l in ls:
    print u'- {0} | {1} (ID = "{2}")'.format(l.title_de, l.title_en, l.slug)
-->

- In englischer Sprache | In English (ID = "in-englischer-sprache")
- Sprache kein Problem | Language no Problem (ID = "sprache-kein-problem")
- Mit englischen Übertiteln | With English surtitles (ID = "mit-engl-uebertiteln")
- Mit französischen Übertiteln | With French surtitles (ID = "mit-franzoesischen-uebertiteln")
- Andere Sprache | Other Languages (ID = "andere-sprache")
- Simultanübersetzung englisch-deutsch | Simultaneous translation English-German (ID = "simultanubersetzung-englisch-deutsch")

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
| `"image_url"` | URL | no | URL of the sponsor logo in JPG or PNG format. Must end with the file extension ".jpg" or ".png" | "http://example.com/media/sponsor-logo.png" |
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

Events are specific dates and times when production is happening. If event's keys match production's keys, they will overwrite production's data, otherwise the value from the production will be used at the Berlin Bühnen website. The `"events"` key contains a list of `event` objects.

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
| `"language_and_subtitles_id"` | string | no | Language and subtitles | "sprache-kein-problem" |
| `"sponsors"` | list of `sponsor` objects | no | Sponsors | |
| `"classiccard"` | string | no | Intended for ClassicCard holders. One of “true” or “false” | "false" |

### The Event Characteristics ###

This is a list of all available characteristics with IDs to enter as values at `"characteristic_id"` of the event:

<!--
>>> from berlinbuehnen.apps.productions.models import EventCharacteristics
>>> es = EventCharacteristics.objects.all()
>>> for e in es:
    print u'- {0} | {1} (ID = "{2}")'.format(e.title_de, e.title_en, e.slug)
-->

- Premiere | Premiere (ID = "premiere")
- Deutsche Erstaufführung | Premiere in Germany (ID = "deutsche-erstauffuehrung")
- Deutschsprachige Erstaufführung | Premiere in German (ID = "deutschsprachige-erstauffuehrung")
- Berliner Premiere | Premiere in Berlin (ID = "berliner-premiere")
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
