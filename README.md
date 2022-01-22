# NUFORC API

<h3><details>
<summary>Contents</summary>

<h6>

1. [Description](#description)
</h6><h6>

2. [Representation](#database-representation)
</h6><h6>

3. [Endpoints](#endpoints)
</h6><h6>
</details></h3>

### Description

A [Flask](https://flask.palletsprojects.com/en/2.0.x/) powered RESTful API with monthly database updates for reports of UFO sigthings submitted to the National UFO Reporting Center [(NUFORC)](http://www.nuforc.org/).  <br>
<sub><sub>[Contents](#nuforc-api)</sub></sub>

### Database Representation

Using [Selenium](https://selenium-python.readthedocs.io/api.html) and [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) to grab all of the data from each linked table on [NUFORC's 'Latest UFO Reports' page](http://www.nuforc.org/webreports/ndxevent.html), the application uses custom NLP to parse `Duration` strings returning minimum/maximum duration values for each sighting. Four-digit calendar years for sightings are referenced on the sightings reports index page but are not stored as such in the `Date / Time` column of each month's sightings report, necessitaing the addition of a four-digit `Year` column.  All information from the source is presented in its unaltered state with the further-processed data obtained from the source for `Year`, `Minimum Duration` and `Maximum Duration` appended.<br>
<sub><sub>[Contents](#nuforc-api)</sub></sub>

### Endpoints

`baseURL`

`baseURL/today`

`baseURL/aRandomSigthingFromTodayInHistory`

`baseURL/rss.xml`<br>
<sub><sub>[Contents](#nuforc-api)</sub></sub>