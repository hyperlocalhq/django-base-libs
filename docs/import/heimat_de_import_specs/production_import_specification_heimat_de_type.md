# Berlin Bühnen Production Import (Heimat.de type)

Last update: October 24, 2017

[TOC]

## Introduction ##

The Berlin Bühnen website has locations (theaters) and stages where plays happen. All plays are named as productions. Productions have general information about the play. Each production has multiple events, that is, exact dates and times when the play happens. Events might overwrite some general information of their production.

## How to prepare the feed?

The feed specification can be found in the following [PDF document](2010-11-17_WNI_cb-in_xml-terminschnittstelle_buehnen.pdf).

## Category Mappings at Berlin Bühnen

This is a list of category mappings for better transparency how categories are treated when importing. All unmentioned categories are ignored.

### Status ID ➔ Production Characteristics

Import Feed | Berlin Bühnen
----|----
Wiederaufnahme (ID = 2) | Wiederaufnahme
Gastspiel (ID = 6) | Gastspiel
Repertoire (ID = 21) | Repertoire
Uraufführung (ID = 23) | Uraufführung
On Tour (ID = 31) | On Tour
    
### Status ID ➔ Event Characteristics

Import Feed | Berlin Bühnen
----|----
Premiere (ID = 1) | Premiere
Vorauffuhrung (ID = 3) | Vorauffuhrung
Deutsche Erstauffuhrung (ID = 17) | Deutsche Erstauffuhrung
zum letzten Mal (ID = 22) | zum letzten Mal
Familienvorstellung (ID = 24) | Familienpreise
zum letzten Mal in dieser Spielzeit (ID = 28) | zum letzten Mal in dieser Spielzeit
Deutschsprachige Erstauffuhrung (ID = 30) | Deutschsprachige Erstauffuhrung
B-Premiere (ID = 33) | Berliner Premiere



