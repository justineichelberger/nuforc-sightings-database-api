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
{random_sighting}