# Bulletin Namespace for RSS Feeds

_Last update: January 21, 2019_

Bulletin namespace extends RSS feed nodes with bulletin-board specific fields.

## Fields

This namespace defines the following child nodes for the `<item>` node:

### `<bulletin:type>`

It can have one of these values: "search" or "offer". It's a required field.

### `<bulletin:category>`

It can have one of these values: "partner", "know how", "material resources", "facilities", "other". It's a required field.

### `<bulletin:contact_person>`

It is the name of the contact person. It's an optional field if `<bulletin:company>` is defined.

### `<bulletin:company>`

It is the name of the company searching or offering something. It's an optional field if `<bulletin:contact_person>` is defined.

### `<bulletin:company_url>`

It is the website URL of the company searching or offering something.

### `<bulletin:phone>`

It is the contact phone number.

### `<bulletin:email>`

It is the contact email.

## Usage

To use it add `xmlns:bulletin="https://www.creative-city-berlin.de/static/0/site/xmlns/bulletin/"` to `<rss>` node in your feed:

```xml
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" 
    xmlns:bulletin="https://www.creative-city-berlin.de/static/0/site/xmlns/bulletin/" >
    ...
</rss>
```

