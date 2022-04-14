import calendar
import datetime
import flask
import glob
import glom
import os
import sqlite3
import time

from datetime import date, datetime
from documentation import *
from flask import Flask, url_for, jsonify, render_template, request
from glom import glom
from markdown_templating import *
from os import path

#
endpoints_to_database_mapping_dictionary = {}

# initiate flask app and set folder for template rendering
app = flask.Flask(__name__, template_folder='templates') 
app.config["DEBUG"] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True  

## obtain day-class information for today
def dayclass():
    if date.today().year % 4 != 0:
        todays_ordinal_modulo_year = (date.toordinal(date.today()) - (date.toordinal(datetime(date.today().year, 1, 1))))+1
        if todays_ordinal_modulo_year > 59:
            todays_ordinal_modulo_year = todays_ordinal_modulo_year + 1
    else:
        todays_ordinal_modulo_year = (date.toordinal(date.today()) - (date.toordinal(datetime(date.today().year, 1, 1))))+1
    return todays_ordinal_modulo_year

## get path to most complete database resource
def database_selector():
    if os.path.getsize(sorted(glob.glob('./database/nuforc_sightings*.db'))[-1]) >= os.path.getsize(sorted(glob.glob('./database/backup/nuforc_sightings*.db'))[-1]):
        return sorted(glob.glob('./database/nuforc_sightings*.db'))[0]
    else:
        return sorted(glob.glob('./database/backup/nuforc_sightings*.db'))[0]

##
def endpoints_to_database_mapper(endpoint, database_column):
    database_mapping_dictionary = {}
    database_connection = sqlite3.connect(database_selector())
    database_cursor = database_connection.cursor()
    database_keys_object = database_cursor.execute("SELECT * FROM nuforcSightings")
    database_keys_list = [description[0] for description in database_keys_object.description]
    for i in range(len(database_keys_list)):
        database_mapping_dictionary[database_keys_list[i]] = i
    endpoints_to_database_mapping_dictionary[endpoint] = database_mapping_dictionary[database_column]
    return endpoints_to_database_mapping_dictionary

##  
def has_no_empty_parameters(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

##
def queryparameter():
    pass

##
def query_mapper(parameter, parameter_attribute):
    if parameter_attribute:
        query_mapper.parameter = parameter_attribute
        endpoints_to_database_mapping_dictionary[parameter] = query_mapper.parameter
    if not parameter and not parameter_attribute:
        return endpoints_to_database_mapping_dictionary

## configure SQLite query
def query_parameters(mapping):
    if not mapping:
        if request.args.get('city'):
            city = f"%{request.args.get('city')}%".lower()
        else:
            city = request.args.get('city')
        date = request.args.get('date')
        day = request.args.get('day')
        dayclass = request.args.get('dayclass')
        enddate = request.args.get('enddate')
        maximumduration = request.args.get('maximumduration')
        minimumduration = request.args.get('minimumduration')
        month = request.args.get('month')
        if request.args.get('shape'):
            shape = f"%{request.args.get('shape')}%".lower()
        else: 
            shape = request.args.get('shape')
        startdate = request.args.get('startdate')
        if request.args.get('state'):
            state = f"%{request.args.get('state')}%".lower()
        else:
            state = request.args.get('state')
        year = request.args.get('year')
        query = "SELECT * FROM nuforcSightings WHERE"
        to_filter = []
    if not mapping:
        if city:
            query += ' CityAndOrCountry LIKE ? AND'
            to_filter.append(city)
    # query_parameters.city = 'CityAndOrCountry'
    query_mapper('city', 'CityAndOrCountry')
    if not mapping:
        if date:
            query += ' DateOfSighting=? AND'
            to_filter.append(date)
    # query_parameters.date = 'DateOfSighting'
    query_mapper('date', 'DateOfSighting')
    if not mapping:
        if day:
            query += ' DayOfSighting=? AND'
            to_filter.append(day)
    # query_parameters.day = 'DayOfSighting'
    query_mapper('day', 'DayOfSighting')
    if not mapping:
        if dayclass:
            query += ' substr(DateOfSighting, 5, 8)=? AND'
            to_filter.append(dayclass)
    # query_parameters.dayclass = 'DateOfSighting'
    query_mapper('dayclass', 'DateOfSighting')
    if not mapping:
        if enddate:
            query += ' DateOfSighting <=? AND'
            to_filter.append(enddate)   
    # query_parameters.enddate = 'DateOfSighting'
    query_mapper('enddate', 'DateOfSighting')
    if not mapping:
        if maximumduration:
            query += ' typeof(MaximumDuration) = "real" AND MaximumDuration<=? AND'
            to_filter.append(maximumduration)
    # query_parameters.maximumduration = 'MaximumDuration'
    query_mapper('maximumduration', 'MaximumDuration')
    if not mapping:
        if minimumduration:
            query += ' typeof(MinimumDuration) = "real" AND MinimumDuration>=? AND'
            to_filter.append(minimumduration)
    # query_parameters.minimumduration = 'MinimumDuration'
    query_mapper('minimumduration', 'MinimumDuration')
    if not mapping:
        if month:
            query += ' MonthOfSighting=? AND'
            to_filter.append(month)
    # query_parameters.month = 'MonthOfSighting'
    query_mapper('month', 'MonthOfSighting')
    if not mapping:
        if shape:
            query += ' Shape LIKE ? AND'
            to_filter.append(shape)
    # query_parameters.shape = 'Shape'
    query_mapper('shape', 'Shape')
    if not mapping:
        if startdate:
            query += ' DateOfSighting >=? AND'
            to_filter.append(startdate)
    # query_parameters.startdate = 'DateOfSighting'
    query_mapper('startdate', 'DateOfSighting')
    if not mapping:
        if state:
            query += ' StateOrProvince LIKE ? AND'
            to_filter.append(state)
    # query_parameters.state = 'StateOrProvince'
    query_mapper('state', 'StateOrProvince')
    if not mapping:
        if year:
            query += ' YearOfSighting=? AND'
            to_filter.append(year)
    # query_parameters.year = 'YearOfSighting'
    query_mapper('year', 'YearOfSighting')
    if not mapping:
        if not any(parameter for parameter in query_parameters.__code__.co_varnames[:-5]): 
            return page_not_found(404)
    if not mapping:
        query = query[:-4] + ';'
        database_connection = sqlite3.connect(database_selector())
        database_cursor = database_connection.cursor()
        results = database_cursor.execute(query, to_filter).fetchall()
    if not mapping:
        return results

def random_sighting_from_today():
    todaysMonth = date.today().month
    todaysDay = date.today().day
    database_connection = sqlite3.connect(database_selector())
    database_cursor = database_connection.cursor()
    today_database = database_cursor.execute("SELECT * FROM nuforcSightings WHERE MonthOfSighting = ? AND DayOfSighting = ? ORDER BY RANDOM() LIMIT 1", (todaysMonth, todaysDay)).fetchall()
    return today_database

def rss_feed():
#### obtain day-class information for today's feed
    todays_ordinal_modulo_year = dayclass()
#### query date parameters
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
##### query database to obtain data for feed dictionary 
    today_database = database_cursor.execute("SELECT * FROM nuforcSightings WHERE MonthOfSighting = ? AND DayOfSighting = ?", (todaysMonth, todaysDay)).fetchall()
#### prepare list of entries dictionary to be added to the feed dictionary 
    entries_list = []
    today_row_counter = 0 
    todays_sightings_count = len(today_database)
    for row in today_database:
        entry_dictionary = {}
        entry_dictionary = dict(zip(database_row.keys(), row))
        entry_dictionary["title"] = todays_sightings_count-today_row_counter
        entry_dictionary["description"] = f"In {entry_dictionary['CityAndOrCountry']} {entry_dictionary['StateOrProvince']} on {entry_dictionary['DateAndTime']} for approximately {entry_dictionary['MinimumDuration']} to {entry_dictionary['MaximumDuration']} minutes witness reports: '{entry_dictionary['CompleteSummary']}'"
        entry_dictionary["pubDate"] = rss_RFC822(database_selector().split('/')[-1].split('_'))
        entry_dictionary["guid"] = entry_dictionary['CompleteSummaryURL']
        entry_dictionary["link"] = entry_dictionary['CompleteSummaryURL']
        entry_dictionary["shape"] = {'name':["NUFORC"]}
        entries_list.append(entry_dictionary)
        today_row_counter += 1
#### generate rss feed dictionary
    entries = entries_list
    feed = {"title":f'ufo sightings from dayclass {todays_ordinal_modulo_year} in history',"html_url":"https://nuforc-sightings-database-api.herokuapp.com","rss_url":"https://nuforc-sightings-database-api.herokuapp.com/sightings/today/rss.xml","description":"database last updated on: ","pubDate":f"{rss_RFC822(database_selector().split('/')[-1].split('_'))}", "entries":entries}
    return feed

## format datetime for rss feed
def rss_RFC822(datetime_published):
    rss_RFC822_string = f"{datetime(int(datetime_published[2]), int(datetime_published[3]), int(datetime_published[4])).strftime('%a')}, {datetime_published[4]} {calendar.month_abbr[int(datetime_published[3])]} {'%04d' % int(datetime_published[2])} {datetime_published[5]}:{datetime_published[6]}:{datetime_published[7].split('.')[0]} {time.strftime('%z')}"
    return rss_RFC822_string

## mapping function that generates a list of all routes
def sitemapper():
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_parameters(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return links

## prepare list of endpoints for sitemap
for endpoint in [parameter for parameter in query_parameters.__code__.co_varnames[:-5] if parameter != 'mapping']:
    app.delete("/sightings/query:" + endpoint)
    app.add_url_rule("/sightings/query:" + endpoint, f'{endpoint}')
    app.view_functions["/sightings/query:" + endpoint] = queryparameter()

query_parameters('mapping')

## API routes
### make updated data available to app
@app.context_processor
def inject_data():
    database_keys_list = []
    database_mapping_dictionary = {}
    random_sightings = []
    database_connection = sqlite3.connect(':memory:')
    database_connection = sqlite3.connect(database_selector())
    database_cursor = database_connection.cursor()
    database_keys_object = database_cursor.execute("SELECT * FROM nuforcSightings")
    database_keys_list = [description[0] for description in database_keys_object.description]
    for i in range(len(database_keys_list)):
        database_mapping_dictionary[database_keys_list[i]] = i
    database_object = database_cursor.execute(f"SELECT * FROM nuforcSightings WHERE ? ||''|| ?  IS NOT NULL ORDER BY RANDOM() LIMIT {len(sitemapper())}", (database_keys_list[0], database_keys_list[-1])).fetchall()
    for row in database_object:
        random_sightings.append(list(row))
    return dict(database_mapping_dictionary=database_mapping_dictionary, endpoints_to_database_mapping_dictionary=query_mapper('',''), random_sightings=random_sightings)

###
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

###
@app.route('/', methods=['GET', 'POST'])
def index():
    githubflavoredmarkdown(sitemapper())
    documentor_dictionary = {}
    database_keys_list = []
    database_mapping_dictionary = {}
    list_of_random_sightings = []
    random_sightings = []
    database_connection = sqlite3.connect(database_selector())
    database_cursor = database_connection.cursor()
    database_keys_object = database_cursor.execute("SELECT * FROM nuforcSightings")
    database_keys_list = [description[0] for description in database_keys_object.description]
    datatypes_object = database_cursor.execute("PRAGMA table_info(nuforcSightings)")
    datatypes_list = [datatype_string for datatype_string in datatypes_object]
    
    for link in sitemapper():
        if link:
            try:
                documentor_dictionary[link[0].replace('.', '').replace('/', '.').replace(':','.')[1:]] = glom(documentor(directory_list, target), f"endpoints.{link[0].replace('.', '').replace('/', '.').replace(':','.')[1:]}.{link[0].replace('.', '').replace('/', '.').replace(':','.').split('.')[-1]}")
            except Exception:
                documentor_dictionary['index'] = glom(documentor(directory_list, target), 'endpoints.index.index')

    for i in range(len(database_keys_list)):
        database_mapping_dictionary[database_keys_list[i]] = i
        if i == 0:
            examples_query = "SELECT * FROM nuforcSightings WHERE ? IS NOT NULL AND"
        elif i < len(database_keys_list)-1:
            examples_query += " ? IS NOT NULL AND"
        else:
            examples_query += " ? IS NOT NULL"
    
    for i in range(len(database_keys_list)):
        if i == 0:
            database_column_names_list = database_keys_list.copy()
            database_column_names_list += [[datatype_string[2] for datatype_string in datatypes_list][i]]
            examples_query += f" AND typeof({[datatype_string[1] for datatype_string in datatypes_list][i]}) = ? AND"
        elif i < len(database_keys_list)-1:
            database_column_names_list += [[datatype_string[2] for datatype_string in datatypes_list][i]]
            examples_query += f" typeof({[datatype_string[1] for datatype_string in datatypes_list][i]}) = ? AND"
        elif i == len(database_keys_list)-1:
            database_column_names_list += [[datatype_string[2] for datatype_string in datatypes_list][i]]
            examples_query += f" typeof({[datatype_string[1] for datatype_string in datatypes_list][i]}) = ? ORDER BY RANDOM() LIMIT {len(sitemapper())}"
        
    database_object = database_cursor.execute(examples_query, tuple(database_column_names_list)).fetchall()

    for row in database_object:
        random_sightings.append(list(row))

    for sighting in range(len(random_sightings)):
        list_of_random_sightings.append(dict([item for item in zip(tuple(database_keys_list), tuple(random_sightings[sighting]))]))
    
    random_sighting = dict(dict([item for item in zip(tuple(database_keys_list), tuple(random_sighting_from_today()[0]))]))

    generate_documentation_examples(directory_list, list_of_random_sightings, dict([item for item in zip(tuple(database_keys_list), tuple(random_sighting_from_today()[0]))]), rss_feed(), sitemapper());

    # <br><br>{{ '../endpoints'+link[0].replace(':','/')+'/'+link[0].replace(':','/').split('/')[-1]+'.txt' }}
    
    return render_template("index.html", database_mapping_dictionary=database_mapping_dictionary, documentor=documentor_dictionary, endpoints_to_database_mapping_dictionary=query_mapper('',''), feed=rss_feed(), links=sitemapper(), random_sighting=random_sighting, random_sightings=list_of_random_sightings, todays_ordinal_modulo_year=dayclass())

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

### query the entire database
@app.route('/sightings/query', methods=['GET', 'POST'])
def query():
    return jsonify(query_parameters(''))

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
    return jsonify(random_sighting_from_today())

### rss feed route
@app.route('/sightings/today/rss.xml')
def rss():
    return render_template('rss.xml', feed=rss_feed)

if __name__=='__main__':
    app.run(debug=True, use_reloader=False)