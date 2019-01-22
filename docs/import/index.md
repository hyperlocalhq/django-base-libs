# Frequently Asked Questions about Imports to Creative City Berlin

_Last update: January 21, 2019_

[TOC]

## What imports do exist at Creative City Berlin?

There are 3 imports depending on the data type. Creative City Berlin imports [news articles](articles/), [marketplace bulletins](bulletins), and [job offers](jobs/).

## When are the imports executed?

Imports of __news articles__ and __marketplace bulletins__ happen once in an hour. Imports of __job offers__ happen every night between 2:00 and 5:00.

## Will the elements be updated with the next import?

As of today, this is the behaviour of all imports:

- For the news, if article has been modified or published at Creative City Berlin, it won't be updated by the next import execution. Otherwise it will.
- For the market place, if the bulletin has been modified or published at Creative City Berlin, it won't be updated by the next import execution. Otherwise it will.
- For the jobs, all of the job offers from the job feed will be updated if they have been changed at the import source (`modified_date` at the source is newer than `modified_date` at Creative City Berlin)

## What fields will be updated with the next import?

All fields that are previously used for creating an article, bulletin, or job will be updated.

## If an object is deleted at Creative City Berlin, will it be reimported again?

No, if an object was imported and later deleted by Creative City Berlin moderators, it won't be imported again.