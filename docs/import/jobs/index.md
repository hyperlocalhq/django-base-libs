# Job Offer Import Specification

_Last update: January 21, 2019_

[TOC]

## Introduction ##

The Creative City Berlin website shows job offers that can be created by its users or imported from content partners.

## How to prepare the feed?

The JSON for the import API should have the following structure:

```javascript
{
    "meta": {
        // meta information
    },
    "jobs": [
        {
            // job offer properties
        },
        {
            // job offer properties
        },
        // other job offers
    ]    
}
```

### The Meta Section ###

The `"meta"` section contains information about pagination and amount of jobs, as follows:

| Key                | Type    | Required | Description                                                            | Example                               |
|--------------------|---------|----------|------------------------------------------------------------------------|---------------------------------------|
| `"next"`           | URL     | no       | The API URL for the next page (or empty string for the last page)      | "http://example.com/api/jobs/?page=3" |
| `"previous"`       | URL     | no       | The API URL for the previous page (or empty string for the first page) | "http://example.com/api/jobs/?page=1" |
| `"total_count"`    | integer | yes      | How many jobs are there in total?                               | 521                                   |
| `"items_per_page"` | integer | yes      | What is the maximal amount of jobs per page?                    | 50                                    |

### The Jobs Section ###

The `"jobs"` section contains paginated list of jobs and their events.

## Jobs ##

### The Job Object ###

Each `job` object has the following keys and values:

| Object              | Type              | Required | Description                                                      | Example                               |
|---------------------|-------------------|----------|------------------------------------------------------------------|---------------------------------------|
| `"id"`              | string or integer | yes      | Unique job ID on your website                                    | 12                                    |
| `"creation_date"`   | dateTime          | yes      | job creation timestamp in ISO 8601 format                        | "2016-04-14T16:27:38"                 |
| `"modified_date"`   | dateTime          | no       | job modification timestamp in ISO 8601 format                    | "2016-04-14T16:27:38"                 |
| `"position"`        | string            | yes      | Position                                                         |                                       |
| `"description"`     | string            | yes      | Plain-text description. HTML is not allowed.                     |                                       |
| `"job_type_id"`     | string            | yes      | ID of one of the job types                                       | "full-time"                           |
| `"qualifications"`  | list              | no       | list of qualification IDs                                        | ["senior"]                            |
| `"job_sectors"`     | list              | no       | list of job sector IDs                                           | ["graphic-design", "product-manager"] |
| `"categories"`      | list              | no       | list of category IDs                                             | ["bildende-kunst"]                    |
| `"company"`         | string            | no       | Offering institution title                                       | "John & Co"                           |
| `"contact_person"`  | string            | no       | Contact person name                                              | "John Doe"                            |
| `"street_address"`  | string            | no       | Street address (first line) of the location                      |                                       |
| `"street_address2"` | string            | no       | Street address (second line) of the location                     |                                       |
| `"postal_code"`     | string            | no       | Postal code of the location                                      |                                       |
| `"city"`            | string            | no       | City of the location                                             |                                       |
| `"website"`         | URL               | no       | A link to the your website page about this job                   | "http://example.com/en/jobs/2345/"    |
| `"email"`           | string            | no       | Contact email address for this job                               | "john@example.com"                    |
| `"publish_email"`   | boolean           | no       | Can the email address be shown for unregistered visitors?        | false                                 |
| `"is_commercial"`   | boolean           | yes      | Do you need to pay to get the contact information about the job? | false                                 |

### Job Types

These are the job types that can be used:

- Full-time | Vollzeit (ID="full-time")
- Short-time | Kurzzeit (ID="short-time")
- Part-time | Teilzeit (ID="part-time")
- Temporary | Befristet (ID="temporary")
- Freelance | Freie Mitarbeit (ID="freelance")
- Apprenticeship | Ausbildung (ID="apprenticeship")
- Internship | Praktikum (ID="internship")
- Trainee | Volontariat/Trainee (ID="trainee")
- Student Assistance | Studentische Aushilfe (ID="student-assistance")
- Cooperation | Kooperation (ID="cooperation")
- N/A | N/A (ID="not-available")

### Qualifications

These are the qualifications that can be used:

- Junior (ID="junior")
- Middle (ID="middle")
- Senior (ID="senior")
- N/A (ID="not-available")

### Job Sectors

These are the job sectors that can be used:

- Community Management | Community Management (ID="community-management")
- Management | Management (ID="management")
- Product Manager | Product Manager (ID="product-manager")
- Sales & Support | Sales & Support (ID="sales-support")
- Museum & Art | Museum & Kunst (ID="museum-art")
- Funding & Non-profit | Stiftung & Nonprofit (ID="funding-non-profit")
- Culture | Kulturwirtschaft (ID="culture")
- Education & Opened Sector | Bildung & Öffentlicher Sektor (ID="education-opened-sector")
- Music & Scene | Musik & Bühne (ID="music-scene")
- Advertising | Werbung (ID="advertising")
- Online & IT | Online & IT (ID="online-it")
- Integrated | Integrated (ID="integrated")
- Graphic Design | Grafik Design (ID="graphic-design")
- Marketing | Marketing (ID="marketing")
- PR & Event | PR & Event (ID="pr-event")
- Dialog / DM / CRM | Dialog / DM / CRM (ID="dialog-dm-crm")
- Corporate - CD / CI / CC | Corporate - CD / CI / CC (ID="corporate-cd-ci-cc")
- Games | Games (ID="games")
- Industry / Product | Industrie / Produkt (ID="industry-product")
- TV / Movie | TV / Film (ID="tv-movie")
- Package Design | Package Design (ID="package-design")
- Mobile | Mobile (ID="mobile")
- Media & Literature | Medien & Literatur (ID="media-literature")
- Other | Andere (ID="other")

### Categories

These are the categories that can be used:

- Architecture | Architektur (ID="architektur")
- Visual Arts | Bildene Kunst (ID="bildende-kunst")
- Design | Design (ID="design")
- Event Industry | Eventbranche (ID="eventbranche")
- Film & Broadcast | Film & Rundfunk (ID="film-rundfunk")
- Photography | Fotographie (ID="fotografie")
- Games & Interactive | Games & Interactive (ID="games-interactive")
- Literature & Publishing | Literatur & Verlage (ID="literatur-verlage")
- Fashion & Textile | Mode & Textil (ID="mode-textil")
- Music | Musik (ID="musik")
- Theatre & Dance | Tanz & Theater (ID="tanz-theater")
- Advertising & PR | Werbung & PR (ID="werbung-pr")
- Miscellaneous | Sonstiges (ID="sonstiges")

## Publishing

All the jobs of the feed will be published to [Creative City Berlin Jobs](https://www.creative-city-berlin.de/de/jobs/) immediately when importing.
