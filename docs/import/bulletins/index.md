# Bulletin Import Specification #

_Last update: January 21, 2019_

[TOC]

## Introduction ##

The Creative City Berlin website shows marketplace bulletins that can be created by its users or imported from content partners.

## How to prepare the feed?

We expect the standard RSS 2.0 feed with some extensions in XML format with UTF-8 encoding. Here is an example:

```xml
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" 
    xmlns:bulletin="https://www.creative-city-berlin.de/static/0/site/xmlns/bulletin/"
    xmlns:atom="http://www.w3.org/2005/Atom"
>
  <channel>
    <title>Bulletin Board at Your Website</title>
    <description>Your website description.</description>
    <link>https://www.example.com</link>
    <copyright>Copyright 2019 Your Company, Inc.</copyright>
    <language>de-de</language>
    <lastBuildDate>Mon, 21 Jan 2019 15:57:17 +0100</lastBuildDate>
    <pubDate>Mon, 21 Jan 2019 15:57:17 +0100</pubDate>
    <atom:link href="https://www.example.com/bulletin-board/rss.xml" rel="self" type="application/rss+xml" />
    <item>
      <guid>http://www.example.com/bulletin-board/bulletin-title-1/</guid>
      <title>Bulletin Title #1</title>
      <description><![CDATA[ 
      <p>Bulletin text. Bulletin text. Bulletin text. Bulletin text. </p>
      <p>Bulletin text. Bulletin text. Bulletin text. Bulletin text. </p>
      <p>Bulletin text. Bulletin text. Bulletin text. Bulletin text. </p>
      ]]></description>
      <link>http://www.example.com/bulletin-board/bulletin-title-1/</link>
      <pubDate>Mon, 21 Jan 2019 15:57:17 +0100</pubDate>
      <bulletin:type>search</bulletin:type>
      <bulletin:category>partner</bulletin:category>
      <bulletin:contact_person>John Doe</bulletin:contact_person>
      <bulletin:company>John &amp; Co</bulletin:company>
      <bulletin:company_url>http://john.example.com/</bulletin:company_url>
      <bulletin:phone>+49 123 456789</bulletin:phone>
      <bulletin:email>john@example.com</bulletin:email>
    </item>
    <item>
      <guid>http://www.example.com/bulletin-board/bulletin-title-2/</guid>
      <title>Bulletin Title #2</title>
      <description><![CDATA[ 
      <p>Bulletin text. Bulletin text. Bulletin text. Bulletin text. </p>
      <p>Bulletin text. Bulletin text. Bulletin text. Bulletin text. </p>
      <p>Bulletin text. Bulletin text. Bulletin text. Bulletin text. </p>
      ]]></description>
      <link>http://www.example.com/news/bulletin-board/bulletin-title-2/</link>
      <pubDate>Mon, 21 Jan 2019 15:57:17 +0100</pubDate>
      <bulletin:type>offer</bulletin:type>
      <bulletin:category>know how</bulletin:category>
      <bulletin:contact_person>John Doe</bulletin:contact_person>
      <bulletin:company>John &amp; Co</bulletin:company>
      <bulletin:company_url>http://john.example.com/</bulletin:company_url>
      <bulletin:phone>+49 123 456789</bulletin:phone>
      <bulletin:email>john@example.com</bulletin:email>
    </item>
    <item>
      <guid>http://www.example.com/bulletin-board/bulletin-title-3/</guid>
      <title>Bulletin Title #3</title>
      <description><![CDATA[ 
      <p>Bulletin text. Bulletin text. Bulletin text. Bulletin text. </p>
      <p>Bulletin text. Bulletin text. Bulletin text. Bulletin text. </p>
      <p>Bulletin text. Bulletin text. Bulletin text. Bulletin text. </p>
      ]]></description>
      <link>http://www.example.com/bulletin-board/bulletin-title-3/</link>
      <pubDate>Mon, 21 Jan 2019 15:57:17 +0100</pubDate>
      <bulletin:type>search</bulletin:type>
      <bulletin:category>material resources</bulletin:category>
      <bulletin:contact_person>John Doe</bulletin:contact_person>
      <bulletin:company>John &amp; Co</bulletin:company>
      <bulletin:company_url>http://john.example.com/</bulletin:company_url>
      <bulletin:phone>+49 123 456789</bulletin:phone>
      <bulletin:email>john@example.com</bulletin:email>
    </item>
  </channel>
</rss>
```

## Meta

Channel meta information will be ignored, so it doesn't matter what it contains as long as the information is logical and informative for human beings.

## Bulletin Fields

Each Bulletin is defined as an `<item`> node. It can have the following children:

### `<guid>`

It is essential that `<item>` nodes have unique `<guid>` children. We use it to identify which bulletins have been imported and which are new. Don't make it longer than 255 characters.

### `<title>`

It defines the title of the bulletin.

### `<description>`

It defines the content of the bulletin. The `<description>` nodes can contain HTML, but it should either use CDATA like this: `<![CDATA[<p>Hello, World!</p>]]>` or be escaped at the special character level like this: `&lt;p&gt;Hello, World!&lt;/p&gt;`. 

### `<link>`

It defines the full URL of the original bulletin on your website.

### `<pubDate>`

It defines the publishing date and time of the bulletin. We will use the `<pubDate>` with RFC822-formated timestamp to figure out whether to update the imported Bulletin or leave it as it was. The abbrevations of weekdays and months should be in English. The year should be a 4-digit number.

Here are some examples of the same time:

- Fri, 20 Mar 2020 15:57:17 +0100
- Fri, 20 Mar 2020 14:57:17 GMT
- Fri, 20 Mar 2020 09:57:17 -0500

### `<bulletin:type>`

It defines the type of the bulletin. It can have one of these values: "search" or "offer". It's a required field.

### `<bulletin:category>`

It defines the category of the bulletin. It can have one of these values: "partner", "know how", "material resources", "facilities", "other". It's a required field.

### `<bulletin:contact_person>`

It is the name of the contact person. It's an optional field if `<bulletin:company>` is defined.

### `<bulletin:company>`

It is the name of the company searching or offering something. It's an optional field if `<bulletin:contact_person>` is defined.

### `<bulletin:company_url>`

It is the website URL of the company searching or offering something. It's an optional field and shouldn't be provided if `<bulletin:company>` is empty or doesn't exist.

### `<bulletin:phone>`

It is the contact phone number. It is an optional field if contact information is provided in other fields.

### `<bulletin:email>`

It is the contact email. It is an optional field if contact information is provided in other fields.

## Categories

Specific categories will be applied for all news of the same feed. When providing the RSS feed URL to us, also give information which categories to apply to them. These are the possible choices:

- Architecture | Architektur
- Visual Arts | Bildene Kunst
- Design | Design
- Event Industry | Eventbranche
- Film & Broadcast | Film & Rundfunk
- Photography | Fotographie
- Games & Interactive | Games & Interactive
- Literature & Publishing | Literatur & Verlage
- Fashion & Textile | Mode & Textil
- Music | Musik
- Theatre & Dance | Tanz & Theater
- Advertising & PR | Werbung & PR
- Miscellaneous | Sonstiges

## Publishing

All the news of the feed will either be published to [Creative City Berlin Bulletin Market Place](https://www.creative-city-berlin.de/de/marketplace/) immediately when importing, or selected for publishing later manually by content moderators.
