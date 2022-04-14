# N.U.F.O.R.C. SIGHTINGS DATABASE API

<h3><details>
<summary>Contents</summary>

1. [Description](#description)

2. [Representation](#database-representation)

3. [Endpoints](#endpoints)
</details></h3>

### Description

A [Flask](https://flask.palletsprojects.com/en/2.0.x/) powered API with monthly database updates for reports of UFO sightings submitted to the National UFO Reporting Center [(NUFORC)](http://www.nuforc.org/).<br>
<sub>[Contents](#nuforc-api)</sub>

### Database Representation

Using [Selenium](https://selenium-python.readthedocs.io/api.html) and [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) to grab data from each linked table on [NUFORC's 'Data Bank' by 'Event Date'](http://www.nuforc.org/webreports/ndxevent.html) page, the application uses custom NLP to parse `Duration` strings returning minimum/maximum `Duration` values for each sighting.  `Date / Time`  values are normalized for processing with [SQLite](https://www.sqlite.org/index.html). The resulting database can be browsed under the [`Endpoints`](#endpoints) listed below.  All information from the database is presented in its unaltered state with transformed data appended.<br>
<sub>[Contents](#nuforc-api)</sub>

### Endpoints
<h4><details>
<summary>Glossary</summary><br>

[`/sightings/today/rss.xml`](#sightingstodayrssxml)

[`/sightings/today/random`](#sightingstodayrandom)

[`/sightings/query?maximumduration`](#sightingsquerymaximumduration)

[`/sightings/query?minimumduration`](#sightingsqueryminimumduration)

[`/sightings/query?startdate`](#sightingsquerystartdate)

[`/sightings/query?dayclass`](#sightingsquerydayclass)

[`/sightings/query?enddate`](#sightingsqueryenddate)

[`/sightings/query?month`](#sightingsquerymonth)

[`/sightings/query?shape`](#sightingsqueryshape)

[`/sightings/query?state`](#sightingsquerystate)

[`/sightings/query?city`](#sightingsquerycity)

[`/sightings/query?date`](#sightingsquerydate)

[`/sightings/query?year`](#sightingsqueryyear)

[`/sightings/query?day`](#sightingsqueryday)

[`/sightings/query?`](#sightingsquery)

[`/sightings/today`](#sightingstoday)

[`/sightings`](#sightings)

[`/sitemap`](#sitemap)

[`/`](#index)

</details></h3>

#### '/sightings/today/rss.xml'
`rss.xml` is an rss feed that publishes information from the `today` endpoint

use:   automatic

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/today/rss.xml`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/today/random'
`random` returns a single sighting report from this day in history.

use:   automatic

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/today/random`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:maximumduration'
`maximumduration` is a search parameter for the `query?` feature.

use:   `maximumduration` must be given a `float` value.  This value is used to filter out sightings that lasted longer than the specified `maximumduration` from the `MaximumDuration` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?maximumduration=<float(minutes)>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:minimumduration'
`minimumduration` is a search parameter for the `query?` feature.

use:   `maximumduration` must be given a `float` value.  This value is used to filter out sightings that were shorter than the specified `minimumduration` from the `MinimumDuration` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?minimumduration=<float(minutes)>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:startdate'
`startdate` is a search parameter for the `query?` feature.

use:   `startdate` must be given a numerical `string` value in the following order: four-digit year, two-digit month, two-digit day (YYYYMMDD).  This value is used to filter out sightings that occurred before the specified `startdate` from the `DateOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?startdate=<YYYYMMDD>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:dayclass'
`dayclass` is a search parameter for the `query?` feature.

use:   `dayclass` must be given a numerical `string` value in the following order: two-digit month, two-digit day (MMDD).  This value is used in a literal string match search of the `MonthOfSighting` and `DayOfSighting` columns of the database (equivalent to `https://nuforc-sightings-database-api.herokuapp.com/sightings/today` and `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?month=<today's two-digit month>&day=<today's two-digit day>`). `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?dayclass=<MMDD>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:enddate'
`enddate` is a search parameter for the `query?` feature.

use:   `enddate` must be given a numerical `string` value in the following order: four-digit year, two-digit month, two-digit day (YYYYMMDD).  This value is used to filter out sightings that occurred after the specified `enddate` from the `DateOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?enddate=<YYYYMMDD>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:month'
`month` is a search parameter for the `query?` feature.

use:   `month` must be given a numerical `string` value as a two-digit month (MM).  This value is used in a literal string match search of the `DayOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?month=<MM>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:shape'
`shape` is a search parameter for the `query?` feature.

use:   `shape` must be given a `string` value, this value is used in a partial string match search of the `Shape` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?shape=<shape>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:state'
`state` is a search parameter for the `query?` feature.

use:   `state` must be given a `string` value, this value is used in a partial string match search of the `StateOrProvince` column of the database.  Some of the values from the `StateOrProvince` column have 'province' abbreviations instead of 'state' abbreviations. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?state=<stateabbreviation>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:city'
`city` is a search parameter for the `query?` feature.

use:   `city` must be given a `string` value, this value is used in a partial string match search of the `CityAndOrCounty` column of the database.  Some of the values from the `CityAndOrCounty` column have two letter country abbreviations so this endpoint has some limited functionality for searching sightings by 'country' as well. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?city=<cityname>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:date'
`date` is a search parameter for the `query?` feature.

use:   `date` must be given a numerical `string` value in the following order: four-digit year, two-digit month, two-digit day (YYYYMMDD).  This value is used in a literal string match search of the `DateOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?date=<YYYYMMDD>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:year'
`year` is a search parameter for the `query?` feature.

use:   `year` must be given a numerical `string` value as a four-digit year (YYYY).  This value is used in a literal string match search of the `YearOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?year=<YYYY>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query:day'
`day` is a search parameter for the `query?` feature.

use:   `day` must be given a numerical `string` value as a two-digit day (DD).  This value is used in a literal string match search of the `DayOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?day=<DD>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/query'
`query` takes search parameters as input and returns search results (see `input_format`)

use:   `query` must function exactly the same as `sightings` if no search parameters are provided.  `query?` requires that any or all of the query parameters be appended to the URL in their specified formats.  `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?<query_parameter_1>=<**>&<query_parameter_2>=<**>&  ...  <query_parameter_n>=<**>`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings/today'
`today` returns a list of sightings from this day in history (equivalent to `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?dayclass=<today's dayclass>` and `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?month=<today's two-digit month>&day=<today's two-digit day>`)

use:   automatic

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings/today`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sightings'
`sightings` returns the complete database.

use:   automatic

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sightings`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/sitemap'
`sitemap` returns a list of all available endpoints.

use:   automatic

input format:   `https://nuforc-sightings-database-api.herokuapp.com/sitemap`

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>

#### '/' (index)
The 'index' page displays a list of available endpoints with links to example results.

use:   automatic

input format:   ``https://nuforc-sightings-database-api.herokuapp.com``

<sub>[Glossary](#endpoints)</sub>

<sub>[Contents](#nuforc-sightings-database-api)</sub>
