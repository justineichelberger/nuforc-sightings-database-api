import datetime
import flask
import glob
import os
import sqlite3

from datetime import date
from flask import Flask, url_for, jsonify, render_template, request 
from os import path

# initiate flask app
app = flask.Flask(__name__) 
app.config["DEBUG"] = True  

## 
def dayclass():
    #### obtain day-class information for today
    if date.today().year % 4 != 0:
        todays_ordinal_MODish_year = (date.toordinal(date.today()) - (date.toordinal(datetime.date(date.today().year, 1, 1))))+1
        if todays_ordinal_MODish_year > 59:
            todays_ordinal_MODish_year = todays_ordinal_MODish_year + 1
    else:
        todays_ordinal_MODish_year = (date.toordinal(date.today()) - (date.toordinal(datetime.date(date.today().year, 1, 1))))+1
    return todays_ordinal_MODish_year

##  
def has_no_empty_parameters(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

##
def database_selector():
### get path to most complete database resource
    if os.path.getsize(sorted(glob.glob('./database/nuforc_sightings*.db'))[0]) >= os.path.getsize(sorted(glob.glob('./database/backup/nuforc_sightings*.db'))[0]):
        return sorted(glob.glob('./database/nuforc_sightings*.db'))[0]
    else:
        return sorted(glob.glob('./database/backup/nuforc_sightings*.db'))[0]

##
def queryparameter():
    pass

##
def query_parameters():
    city = request.args.get('city')
    date = request.args.get('date')
    day = request.args.get('day')
    dayclass = request.args.get('dayclass')
    enddate = request.args.get('enddate')
    maximumduration = request.args.get('maximumduration')
    minimumduration = request.args.get('minimumduration')
    month = request.args.get('month')
    shape = request.args.get('shape')
    startdate = request.args.get('startdate')
    state = request.args.get('state')
    year = request.args.get('year')
###    
    query = "SELECT * FROM nuforcSightings WHERE"
    to_filter = []
    if city:
        query += ' CityAndOrCountry=? COLLATE NOCASE AND'
        to_filter.append(city)
    if date:
        query += ' DateOfSighting=? AND'
        to_filter.append(date)
    if day:
        query += ' DayOfSighting=? AND'
        to_filter.append(day)
    if dayclass:
        query += ' substr(DateOfSighting, 5, 8)=? AND'
        to_filter.append(dayclass)
    if enddate:
        query += ' DateOfSighting <=? AND'
        to_filter.append(enddate)    
    if maximumduration:
        query += ' typeof(MaximumDuration) = "real" AND MaximumDuration<=? AND'
        to_filter.append(maximumduration)
    if minimumduration:
        query += ' typeof(MinimumDuration) = "real" AND MinimumDuration>=? AND'
        to_filter.append(minimumduration)
    if month:
        query += ' MonthOfSighting=? AND'
        to_filter.append(month)
    if shape:
        query += ' Shape=? COLLATE NOCASE AND'
        to_filter.append(shape)
    if startdate:
        query += ' DateOfSighting >=? AND'
        to_filter.append(startdate)
    if state:
        query += ' StateOrProvince=? COLLATE NOCASE AND'
        to_filter.append(state)
    if year:
        query += ' YearOfSighting=? AND'
        to_filter.append(year)
    if not any(parameter for parameter in query_parameters.__code__.co_varnames[:-5]): 
        return page_not_found(404)
    query = query[:-4] + ';'
    database_connection = sqlite3.connect(database_selector())
    database_cursor = database_connection.cursor()
    results = database_cursor.execute(query, to_filter).fetchall()
    return results

##
def sitemapper():
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_parameters(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return links

## prepare list of endpoints for sitemap
for endpoint in query_parameters.__code__.co_varnames[:-5]:
    app.delete("/sightings/query_parameter_" + endpoint)
    app.add_url_rule("/sightings/query_parameter:" + endpoint, f'{endpoint}')
    app.view_functions["/sightings/query_parameter:" + endpoint] = queryparameter()  

## API routes
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

###
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", todays_ordinal_MODish_year=dayclass(), links=sitemapper())

###
@app.route("/sitemap")
def sitemap():
    return jsonify(sitemapper())

### complete database
@app.route('/sightings', methods=['GET', 'POST'])
def sightings():
    database_connection = sqlite3.connect(database_selector())
    database_cursor = database_connection.cursor()
    complete_database = database_cursor.execute("SELECT * FROM nuforcSightings").fetchall()
    return jsonify(complete_database)

### query the database
@app.route('/sightings/query', methods=['GET', 'POST'])
def query():
    return jsonify(query_parameters())

### all sightings from this day in history
@app.route('/sightings/today', methods=['GET', 'POST'])
def today():
    todaysMonth = date.today().month
    todaysDay = date.today().day
    database_connection = sqlite3.connect(database_selector())
    database_cursor = database_connection.cursor()
    today_database = database_cursor.execute("SELECT * FROM nuforcSightings WHERE MonthOfSighting = ? AND DayOfSighting = ?", (todaysMonth, todaysDay)).fetchall()
    return jsonify(today_database)

### a randomly selected sighting from this day in history
@app.route('/sightings/today/random', methods=['GET', 'POST'])
def random():
    todaysMonth = date.today().month
    todaysDay = date.today().day
    database_connection = sqlite3.connect(database_selector())
    database_cursor = database_connection.cursor()
    today_database = database_cursor.execute("SELECT * FROM nuforcSightings WHERE MonthOfSighting = ? AND DayOfSighting = ? ORDER BY RANDOM() LIMIT 1", (todaysMonth, todaysDay)).fetchall()
    return jsonify(today_database)

### rss feed route
@app.route('/sightings/today/rss')
def rss():
#### obtain day-class information for today's feed
    todays_ordinal_MODish_year = dayclass()
#### database last updated
    pubYear = database_selector().split('/')[-1].split('_')[2]
    pubMonth = database_selector().split('/')[-1].split('_')[3]
    pubDay = database_selector().split('/')[-1].split('_')[4]
#### publish date parameters
    todaysMonth = date.today().month
    todaysDay = date.today().day
#### connect to database
    database_connection = sqlite3.connect(database_selector())
##### prepare connection to iterate through database rows
    database_connection.row_factory = sqlite3.Row
    row_cursor = database_connection.cursor()
    database_cursor = database_connection.cursor()
##### query database to obtain keys for feed dictionary    
    database_row = row_cursor.execute("SELECT * FROM nuforcSightings WHERE MonthOfSighting = ? AND DayOfSighting = ?", (todaysMonth, todaysDay)).fetchone()
    today_database = database_cursor.execute("SELECT * FROM nuforcSightings WHERE MonthOfSighting = ? AND DayOfSighting = ?", (todaysMonth, todaysDay)).fetchall()
#### prepare list of entries dictionary to be added to the feed dictionary 
    entries_list = []
    today_row_counter = 0 
    todays_sightings_count = len(today_database)
    for row in today_database:
        entry_dictionary = {}
        entry_dictionary = dict(zip(database_row.keys(), row))
        entry_dictionary["title"] = todays_sightings_count-today_row_counter
        entry_dictionary["description"] = entry_dictionary['DateAndTime']
        entry_dictionary["pubDate"] = entry_dictionary['DateReportWasPublished']
        entry_dictionary["guid"] = entry_dictionary['CompleteSummaryURL']
        entry_dictionary["link"] = entry_dictionary['CompleteSummaryURL']
        entry_dictionary["shape"] = {'name':["NUFORC"]}
        entries_list.append(entry_dictionary)
        today_row_counter += 1
#### generate rss feed dictionary
    entries = entries_list
    feed = {"title":f'ufo sightings from DayClass {todays_ordinal_MODish_year} in history',"html_url":"http://127.0.0.1:5000/","rss_url":"http://127.0.0.1:5000/rss.xml","description":f'database last updated on:  {pubYear}-{pubMonth}-{pubDay}    ',"pubDate":f"today's date:  {date.today()}    ", "entries":entries}
    return render_template('rss.xml', feed=feed)

if __name__=='__main__':
    app.run(debug=True, use_reloader=False)