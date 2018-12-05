# Frequently Asked Questions about Production Import to Ruhr Bühnen

Last update: October 30, 2018

[TOC]

## What kind of imports do exist at Ruhr Bühnen?

There are 3 types of imports depending on the source format.

1. The first type is based on the old XML format of CultureBase server. We call it "[CultureBase type](culturebase_import_specs/production_import_specification_culturebase_type.html)".

2. The other format is based on [this XML structure specification](http://cb.heimat.de/interface/schema/interfaceformat.xsd). We call it "[Heimat.de type](heimat_de_import_specs/production_import_specification_heimat_de_type.html)".

3. The third format was specifically designed to match the database structure of Ruhr Bühnen. We call it "[Ruhr Bühnen type](rb_import_specs/production_import_specification_rb_type_xml.html)". It can be provided as [XML](rb_import_specs/production_import_specification_rb_type_xml.html) or [JSON](rb_import_specs/production_import_specification_rb_type_json.html). It is a __recommended format__ for all new import feeds.

## What is the difference of production data and event data?

The Ruhr Bühnen website has locations (theaters) and stages where plays happen. All plays are named as productions. Productions have general information about the play. Each production has multiple events, that is, exact dates and times when the play happens. Events might overwrite some general information of their production.

## When are the imports executed?

Imports from all different sources are executed by a cron job every night between 3:00 and 4:00. Exceptionally, imports from GRIPS Theater are executed every 15 minutes, because their data about ticket availability should be as close to real time as possible.

## Will the productions be updated with the next import?

Yes, productions will be updated, unless __no_overwriting__ flag is set for the production at Ruhr Bühnen.

Productions at Ruhr Bühnen have a Boolean field __no_overwriting__ which is

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

## Are canceled or outdated events deleted at Ruhr Bühnen?

Productions that existed in the import feed before, but don't exist there anymore will get a status "trashed". The same is with events: events that existed in the import feed before, but don't exist there anymore will get event status "trashed".

Productions and events republished at the import feed will reappear at Ruhr Bühnen again, unless __no_overwriting__ is set to True there. 


## If a production is deleted at Ruhr Bühnen, will it be reimported again?

If a production or event is manually trashed in the dashboard of Ruhr Bühnen, the production will get __status__ "trashed" or event will get __event_status__ "trashed" and __no_overwriting__ for the production will be set to True. So with the next import it won't be updated.
