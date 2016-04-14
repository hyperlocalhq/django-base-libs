# Production Import Specification #

## Introduction ##

The Berlin Bühnen website has locations (theaters) and stages where plays happen. All plays are named as productions. Productions have general information about the play. Each production has multiple events, that is, exact dates and times when the play happens. Events might overwrite some general information of their production.

## Import XML ##

The XML for the import API should have the following structure:

```xml
<?xml version="1.0" encoding="utf-8"?>
<response>
    <meta>
        <!-- ... -->
    </meta>
    <productions>
		<!-- ... -->
	</productions>
</response>
```

## The `<meta>` Section ##

The `<meta>` section contains information about pagination and amount of productions, as follows:

| Node | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `<next>` | string | no | The API URL for the next page (or empty string for the last page) | http://example.com/api/productions/?page=3 |
| `<previous>` | string | no | The API URL for the previous page (or empty string for the first page) | http://example.com/api/productions/?page=1 |
| `<total_count>` | integer | yes | How many productions are there in total? | 521 |
| `<items_per_page>` | integer | yes | What is the maximal amount of productions per page? | 50 |

### The `<productions>` Section ###

The `<productions>` section contains paginated list of productions and their events. Each production is set as a `<production>` node.

## The `<production>` Node ##

The `<production>` node has the following elements:

| Node | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `<id>` | string or integer | yes | Unique production ID on your website | 12 |
| `<creation_date>`| string | yes | Production creation timestamp in ISO 8601 format | 2016-04-14T16:27:38 |
| `<modified_date>` | string | no | Production modification timestamp in ISO 8601 format | 2016-04-14T16:27:38 |
| `<status>` | string | yes | Publishing status, one of: "draft", "published", "not_listed", "expired", "trashed" | published |
| `<prefix_de>` | string | no | Title prefix in German | |
| `<prefix_en>` | string | no | Title prefix in English | |
| `<title_de>` | string | yes | Title in German | |
| `<title_en>` | string | yes | Title in English | |
| `<subtitle_de>` | string | no | Subtitle (Unterüberschrift) in German | |
| `<subtitle_en>` | string | no | Subtitle (Unterüberschrift) in English | |
| `<original_de>` | string | no | Original title in German | |
| `<original_en>` | string | no | Original title in English | |
| `<website>` | string | no | A link to the your website page about this production | |
| `<description_de>` | string | no | Plain-text description in German | |
| `<description_en>` | string | no | Plain-text description in English | |
| `<teaser_de>` | string | no | Plain-text teaser in German | |
| `<teaser_en>` | string | no | Plain-text teaser in English | |
| `<work_info_de>` | string | no | Plain-text work info in German | |
| `<work_info_en>` | string | no | Plain-text work info in English | |
| `<contents_de>` | string | no | Plain-text contents in German | |
| `<contents_en>` | string | no | Plain-text contents in English | |
| `<press_text_de>` | string | no | Plain-text press text in German | |
| `<press_text_en>` | string | no | Plain-text press text in English | |
| `<credits_de>` | string | no | Plain-text credits in German | |
| `<credits_en>` | string | no | Plain-text credits in English | |
| `<concert_program_de>` | string | no | Plain-text concert program in German | |
| `<concert_program_en>` | string | no | Plain-text concert program in English | |
| `<supporting_program_de>` | string | no | Plain-text supporting program in German | |
| `<supporting_program_en>` | string | no | Plain-text supporting program in English | |
| `<remarks_de>` | string | no | Plain-text remarks in German | |
| `<remarks_en>` | string | no | Plain-text remarks in English | |
| `<duration_text_de>` | string | no | Plain-text information about duration in German | |
| `<duration_text_en>` | string | no | Plain-text information about duration in English | |
| `<subtitles_text_de>` | string | no | Plain-text information about subtitles in German | |
| `<subtitles_text_en>` | string | no | Plain-text information about subtitles in English | |
| `<age_text_de>` | string | no | Plain-text information about the age of the audience in German | |
| `<age_text_en>` | string | no | Plain-text information about the age of the audience in English | |
| `<ensembles>` | string | no | Ensemble or ensembles playing in this production  | |
| `<organizers>` | string | no | Organizer or organizers of this production | |
| `<in_cooperation_with>` | string | no | Cooperator or cooperators | |
| `<free_entrance>` | string | no | Is the entrance free? One of "True" or "False" | False |
| `<price_from>` | decimal | no | Price from in Euros (no currency sign included) | 8.00 |
| `<price_till>` | decimal | no | Price till in Euros (no currency sign included) | 12.00 |
| `<tickets_website>` | string | no | The URL of a website page where you can buy tickets to this production | http://example.com/tickets/ |
| `<price_information_de>` | string | no | Additional plain-text information about prices in German | |
| `<price_information_en>` | string | no | Additional plain-text information about prices in English | |
| `<age_from>` | integer | no | Audience age from | 18 |
| `<age_till>` | integer | no | Audience age till | 99 |
| `<edu_offer_website>` | string | no | The URL of a website page with educational offer | http://example.com/educational-offer/ |
| `<in_program_of>` | list of `<location_id>` nodes | no | Theaters organizing this production | |
| `<play_locations>` | list of `<location_id>` nodes | no | Theaters where this production takes place | |
| `<play_stages>` | list of `<stage_id>` nodes | no | Stages where this production takes place | |
| `<location_title>` | string | no | Location title (if play_locations is empty) | |
| `<street_address>`| string | no | Street address (first line) of the location (if play_locations is empty) | |
| `<street_address2>` | string | no | Street address (second line) of the location (if play_locations is empty) | |
| `<postal_code>`| string | no | Postal code of the location (if play_locations is empty) | |
| `<city>`| string | no | City of the location (if play_locations is empty) | |
| `<latitude>`| decimal | no | Latitude of the location (if play_locations is empty) | 52.5192 |
| `<longitude>` | decimal | no | Longitude of the location (if play_locations is empty) | 13.4061 |
| `<categories>` | list of `<category_id>` nodes | no | Categories | |
| `<characteristics>`| list of `<characteristic_id>` nodes | no | Characteristics | |
| `<leaders>` | list of `<leader>` nodes | no | Leaders | |
| `<authors>` | list of `<author>` nodes | no | Authors | |
| `<participants>` | list of `<participant>` nodes | no | Participants | |
| `<videos>` | list of `<video>` nodes | no | Videos | |
| `<live_streams>` | list of `<live_stream>` nodes | no | Live streams | |
| `<images>` | list of `<image>` nodes | no | Images | |
| `<pdfs>` | list of `<pdf>` nodes | no | PDF documents | |
| `<social_media>` | list of `<social_media_channel>` nodes | no | Social media | |
| `<language_and_subtitles_id>` | string | no | Language and subtitles | |
| `<sponsors>` | list of `<sponsor>` nodes | no | Sponsors | |
| `<events>` | list of `<event>` nodes | no | Events | |

### The Locations and Stages ###

This is a list of all available locations and stages with location IDs and stage IDs to enter as values at `<location_id>` and `<stage_id>`:

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
- Berliner Ensemble (Location ID = 24)
  - Foyer (Stage ID = 20)
  - Gartenhaus (Stage ID = 104)
  - Pavillon (Stage ID = 19)
  - Probebühne (Stage ID = 21)
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
- English Theatre Berlin | International Performing Arts Center (Location ID = 58)
- Friedrichstadt-Palast Berlin (Location ID = 39)
- Galli Theater Berlin (Location ID = 77)
- GRIPS Theater (Location ID = 79)
  - GRIPS Hansaplatz (Stage ID = 31)
  - GRIPS Podewil (Stage ID = 47)
- Große Orangerie Schloss Charlottenburg (Location ID = 74)
  - Große Orangerie Schloss Charlottenburg (Stage ID = 70)
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
- Landesmusikakademie Berlin (Location ID = 63)
- Maxim Gorki Theater (Location ID = 12)
  - Foyer (Stage ID = 34)
  - Gorki Foyer Berlin (Stage ID = 9)
  - Gorki Theater (Stage ID = 33)
  - Studio Я (Stage ID = 10)
  - Vorplatz GORKI (Stage ID = 69)
- Natur-Park Schöneberger Südgelände (Location ID = 161)
- Neuköllner Oper (Location ID = 54)
  - Saal/Studio (Stage ID = 81)
- Pfefferberg Theater (Location ID = 172)
- Podewil (Location ID = 150)
  - Foyer (Stage ID = 162)
  - Großer Saal (GRIPS) (Stage ID = 160)
  - Tanzstudio (Stage ID = 161)
- RADIALSYSTEM V (Location ID = 29)
- Renaissance-Theater Berlin (Location ID = 23)
  - Renaissance-Theater Berlin (Stage ID = 103)
  - Renaissance-Theater Berlin / Bruckner-Foyer (Stage ID = 23)
- SCHAUBUDE BERLIN (Location ID = 51)
  - SCHAUBUDE BERLIN (Stage ID = 71)
- Schaubühne am Lehniner Platz (Location ID = 49)
- Schlosspark Theater (Location ID = 15)
- Sophiensæle (Location ID = 4)
  - Festsaal (Stage ID = 4)
  - gesamtes Haus (Stage ID = 49)
  - Hochzeitssaal (Stage ID = 5)
  - Kantine (Stage ID = 48)
- Staatsballett Berlin (Location ID = 75)
  - Deutsche Oper Berlin (Stage ID = 75)
  - Komische Oper Berlin (Stage ID = 77)
  - Staatsoper im Schiller Theater (Stage ID = 76)
- Staatsoper im Schiller Theater (Location ID = 9)
  - Bebelplatz (Stage ID = 56)
  - Bode Museum (Stage ID = 44)
  - Gläsernes Foyer (Stage ID = 22)
  - Probebühne I (Stage ID = 53)
  - Staatsoper Unter den Linden (Stage ID = 46)
  - Werkstatt (Stage ID = 24)
- Stage BLUEMAX Theater (Location ID = 61)
- Stage Theater am Potsdamer Platz (Location ID = 57)
- Stage Theater des Westens (Location ID = 59)
- TAK Theater im Aufbau Haus (Location ID = 133)
- Theater an der Parkaue (Location ID = 42)
  - Bühne 1 (Stage ID = 84)
  - Bühne 1 - Hinterbühne (Stage ID = 86)
  - Bühne 2 (Stage ID = 27)
  - Bühne 3 (Stage ID = 85)
  - Deutsche Oper - Tischlerei (Stage ID = 140)
  - Kulturhaus Karlshorst (Saal) (Stage ID = 139)
  - Prater (Stage ID = 141)
  - Studiobühne (Stage ID = 87)
- Theater im Palais (Location ID = 32)
- Theater Morgenstern (Location ID = 38)
  - Rathaus Friedenau (Stage ID = 133)
- Theater O-TonArt (Location ID = 20)
- Theater Strahl (Location ID = 72)
- Theater Thikwa (Location ID = 22)
- Theater und Komödie am Kurfürstendamm (Location ID = 25)
  - Komödie am Kurfürstendamm (Stage ID = 94)
  - Theater am Kurfürstendamm (Stage ID = 95)
- Theater unterm Dach (Location ID = 73)
- Theaterdiscounter (Location ID = 2)
- Theaterhaus Berlin Mitte (Location ID = 132)
  - Werkstattbühne 003 (Stage ID = 159)
- TIPI AM KANZLERAMT (Location ID = 7)
- ufaFabrik (Location ID = 56)
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
- Volksbühne am Rosa-Luxemburg-Platz (Location ID = 6)
  - 3\. Stock (Stage ID = 8)
  - Books (Stage ID = 83)
  - Großes Haus (Stage ID = 82)
  - Grüner Salon (Stage ID = 6)
  - Roter Salon (Stage ID = 7)
  - Sternfoyer (Stage ID = 101)
- Wintergarten Berlin (Location ID = 180)

For example, if a production is organized by "Volksbühne am Rosa-Luxemburg-Platz" and happens in the "Grüner Salon" stage, the following XML should be set:

```xml
<in_program_of>
    <location_id>6</location_id>
</in_program_of>
<play_stages>
    <stage_id>6</stage_id>
</play_stages>
```

### The Categories ###

This is a list of all available categories and subcategories with IDs to enter as values at `<category_id>`:

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

For example, if a production can be classified as "Tanz", "Ballet", and "Neue Medien" (under "Sonstiges"), the following XML should be set:

```xml
<categories>
    <category_id>3</category_id>
    <category_id>25</category_id>
    <category_id>10</category_id>
    <category_id>79</category_id>
</categories>
```
### The Production Characteristics ###



## Full featured XML example ##

Finally, you can see the whole [XML example](example.xml).