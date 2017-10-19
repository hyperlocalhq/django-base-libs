# Frequently Asked Questions about Production Import to Berlin Bühnen

Last update: December 7, 2016

## What kind of imports do exist at Berlin Bühnen?

There are 3 types of imports depending on the source format.

1. The first type is based on the old XML format of CultureBase server. This format is used by the following partners:

    - Deutsche Oper Berlin
    - RADIALSYSTEM V
    - Staatsoper im Schiller Theater

2. The other format is based on a the XML structure defined at http://cb.heimat.de/interface/schema/interfaceformat.xsd. This format is used by the following partners:

    - GRIPS Theater
    - Berliner Philharmonie
    - Deutsches Theater
    - HAU
    - Komische Oper Berlin
    - Schaubuehne
    - Sophiensaele
    - Staatsballet Berlin
    - Volksbuehne
    - Wuehlmaeuse

3. The third format was specifically designed to match the database structure of Berlin Bühnen. It can be provided as XML or JSON. This format is used by these partners:

    - Schlosspark Theater
	- Maxim Gorki Theater


## What is the difference of production data and event data?

The Berlin Bühnen website has locations (theaters) and stages where plays happen. All plays are named as productions. Productions have general information about the play. Each production has multiple events, that is, exact dates and times when the play happens. Events might overwrite some general information of their production.

## When are the imports executed?

Imports from all different sources are executed by a cron job every night between 3:00 and 4:00. Exceptionally, imports from GRIPS Theater are executed every 15 minutes, because their data about ticket availability should be as close to real time as possible.

## Will the productions be updated with the next import?

Yes, productions will be updated, unless __no_overwriting__ flag is set for the production at Berlin Bühnen.

Productions at Berlin Bühnen have a Boolean field __no_overwriting__ which is

- shown in the frontend production editing form if the production was imported (not created manually)
- shown in production backend administration for staff users.

The __no_overwriting__ flag ensures that when the import script is executed again, the production is not overwritten with the data from the import source and that the production and its events are not deleted by import scripts.

## What fields will be updated with the next import?

These are the fields and relations that get updated or recreated in the case of reimporting the same production:

- status
- title in German and English
- website link
- slug
- minimal price (in case of CultureBase)
- maximal price (in case of CultureBase)
- tickets website (in case of CultureBase)
- all text fields in both languages
- in-program-of location
- play locations
- play stages
- organizers (in case of CultureBase)
- new images are added, missing images are removed, other images stay as they were. Image descriptions are not updated.
- categories
- characteristics
- involved persons (+ leaders and authors in case of CultureBase)
- sponsors

These are the fields and relations that get updated or recreated in the case of reimporting the same event:

- event start date and time
- duration
- minimal price
- free entrance (in case of Heimat.de)
- textual price information (in case of Heimat.de)
- maximal price
- tickets website
- event status (taking place or canceled)
- ticket status (available or sold out (once sold out, it isn’t changed back to available the next time))
- all text fields in both languages
- organizers (in case of CultureBase)
- new images are added, missing images are removed, other images stay as they were. Image descriptions are not updated.
- play locations
- play stages
- characteristics
- involved persons (+ leaders and authors in case of CultureBase)
- sponsors

## Are canceled or outdated events deleted at Berlin Bühnen?

No, outdated events do not get deleted at Berlin Bühnen by the import scripts, except for the GRIPS Theater.

There are 3 proposals regading this matter:
- administrators of theaters can delete non actual events manually at Berlin Bühnen.
- import source might provide statuses for events, like "published" and "trashed" which will later be taken into account.
- content partners might provide a specific feed, listing IDs of events that need to be deleted.

## If a production is deleted at Berlin Bühnen, will it be reimported again?

No, productions deleted at Berlin Bühnen are meant to be deleted on purpose and therefore they won't be recreated again by the import script.

This restriction can be excluded for specific cases on request.