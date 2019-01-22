# Article Import Specification #

_Last update: January 21, 2019_

[TOC]

## Introduction ##

The Creative City Berlin website shows industry news that can be created by content administrators and moderators or imported from content partners' websites. The news import uses RSS feeds of the content partners. Each feed can be asociated with specific categories that will be applied to the imported new articles. The news can be either published immediately or moderated by content administrators manuallly before publishing.

## How to prepare the feed?

We expect the standard RSS 2.0 feed in XML format with UTF-8 encoding. Here is an example:

```xml
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>News at Your Website</title>
    <description>Your website description.</description>
    <link>https://www.example.com</link>
    <copyright>Copyright 2019 Your Company, Inc.</copyright>
    <language>de-de</language>
    <lastBuildDate>Mon, 21 Jan 2019 15:57:17 +0100</lastBuildDate>
    <pubDate>Mon, 21 Jan 2019 15:57:17 +0100</pubDate>
    <atom:link href="https://www.example.com/news/rss.xml" rel="self" type="application/rss+xml" />
    <item>
      <guid>http://www.example.com/news/article-title-1/</guid>
      <title>Article Title #1</title>
      <description><![CDATA[ 
      <p>Article text. Article text. Article text. Article text. </p>
      <p>Article text. Article text. Article text. Article text. </p>
      <p>Article text. Article text. Article text. Article text. </p>
      ]]></description>
      <link>http://www.example.com/news/article-title-1/</link>
      <pubDate>Mon, 21 Jan 2019 15:57:17 +0100</pubDate>
    </item>
    <item>
      <guid>http://www.example.com/news/article-title-2/</guid>
      <title>Article Title #2</title>
      <description><![CDATA[ 
      <p>Article text. Article text. Article text. Article text. </p>
      <p>Article text. Article text. Article text. Article text. </p>
      <p>Article text. Article text. Article text. Article text. </p>
      ]]></description>
      <link>http://www.example.com/news/article-title-2/</link>
      <pubDate>Mon, 21 Jan 2019 15:57:17 +0100</pubDate>
    </item>
    <item>
      <guid>http://www.example.com/news/article-title-3/</guid>
      <title>Article Title #3</title>
      <description><![CDATA[ 
      <p>Article text. Article text. Article text. Article text. </p>
      <p>Article text. Article text. Article text. Article text. </p>
      <p>Article text. Article text. Article text. Article text. </p>
      ]]></description>
      <link>http://www.example.com/news/article-title-3/</link>
      <pubDate>Mon, 21 Jan 2019 15:57:17 +0100</pubDate>
    </item>
  </channel>
</rss>
```

## Meta

Channel meta information will be ignored, so it doesn't matter what it contains as long as the information is logical and informative for human beings.

## Article Fields

Each article is defined as an `<item`> node. It can have the following children:

### `<guid>`

It is essential that `<item>` nodes have unique `<guid>` children. We use it to identify which articles have been imported and which are new. Don't make it longer than 255 characters.

### `<title>`

It defines the title of the news article.

### `<description>`

It defines the content of the news article. The `<description>` nodes can contain HTML, but it should either use CDATA like this: `<![CDATA[<p>Hello, World!</p>]]>` or be escaped at the special character level like this: `&lt;p&gt;Hello, World!&lt;/p&gt;`. 

### `<link>`

It defines the full URL of the original news article on your website.

### `<pubDate>`

It defines the publishing date and time of the news article. We will use the `<pubDate>` with RFC822-formated timestamp to figure out whether to update the imported article or leave it as it was. The abbrevations of weekdays and months should be in English. The year should be a 4-digit number.

Here are some examples of the same time:

- Fri, 20 Mar 2020 15:57:17 +0100
- Fri, 20 Mar 2020 14:57:17 GMT
- Fri, 20 Mar 2020 09:57:17 -0500

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

All the news of the feed will either be published to [Creative City Berlin News](https://www.creative-city-berlin.de/de/news/) immediately when importing, or selected for publishing later manually by content moderators.
