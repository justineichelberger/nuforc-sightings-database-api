import glom
import json
import os
import shutil
from glom import glom, Assign

index_dictionary = {'description':"The 'index' page displays a list of available endpoints with links to example results.",'use':'automatic', 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com`'}

sightings_dictionary = {'description':"`sightings` returns the complete database.", 'use':'automatic', 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings`'}

sightings_query_dictionary = {'description':"`query` takes search parameters as input and returns search results (see `input_format`)", 'use':"`query` must function exactly the same as `sightings` if no search parameters are provided.  `query?` requires that any or all of the query parameters be appended to the URL in their specified formats.  `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':"`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?<query_parameter_1>=<**>&<query_parameter_2>=<**>&  ...  <query_parameter_n>=<**>`"}

sightings_query_city_dictionary = {'description':"`city` is a search parameter for the `query?` feature.", 'use':"`city` must be given a `string` value, this value is used in a partial string match search of the `CityAndOrCounty` column of the database.  Some of the values from the `CityAndOrCounty` column have two letter country abbreviations so this endpoint has some limited functionality for searching sightings by 'country' as well. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?city=<cityname>`'}

sightings_query_date_dictionary = {'description':"`date` is a search parameter for the `query?` feature.", 'use':"`date` must be given a numerical `string` value in the following order: four-digit year, two-digit month, two-digit day (YYYYMMDD).  This value is used in a literal string match search of the `DateOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?date=<YYYYMMDD>`'}

sightings_query_day_dictionary = {'description':"`day` is a search parameter for the `query?` feature.", 'use':"`day` must be given a numerical `string` value as a two-digit day (DD).  This value is used in a literal string match search of the `DayOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?day=<DD>`'}

sightings_query_dayclass_dictionary = {'description':"`dayclass` is a search parameter for the `query?` feature.", 'use':"`dayclass` must be given a numerical `string` value in the following order: two-digit month, two-digit day (MMDD).  This value is used in a literal string match search of the `MonthOfSighting` and `DayOfSighting` columns of the database (equivalent to `https://nuforc-sightings-database-api.herokuapp.com/sightings/today` and `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?month=<today's two-digit month>&day=<today's two-digit day>`). `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?dayclass=<MMDD>`'}

sightings_query_enddate_dictionary = {'description':"`enddate` is a search parameter for the `query?` feature.", 'use':"`enddate` must be given a numerical `string` value in the following order: four-digit year, two-digit month, two-digit day (YYYYMMDD).  This value is used to filter out sightings that occurred after the specified `enddate` from the `DateOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?enddate=<YYYYMMDD>`'}

sightings_query_maximumduration_dictionary = {'description':"`maximumduration` is a search parameter for the `query?` feature.", 'use':"`maximumduration` must be given a `float` value.  This value is used to filter out sightings that lasted longer than the specified `maximumduration` from the `MaximumDuration` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?maximumduration=<float(minutes)>`'}

sightings_query_minimumduration_dictionary = {'description':"`minimumduration` is a search parameter for the `query?` feature.", 'use':"`maximumduration` must be given a `float` value.  This value is used to filter out sightings that were shorter than the specified `minimumduration` from the `MinimumDuration` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?minimumduration=<float(minutes)>`'}

sightings_query_month_dictionary = {'description':"`month` is a search parameter for the `query?` feature.", 'use':"`month` must be given a numerical `string` value as a two-digit month (MM).  This value is used in a literal string match search of the `DayOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?month=<MM>`'}

sightings_query_shape_dictionary = {'description':"`shape` is a search parameter for the `query?` feature.", 'use':"`shape` must be given a `string` value, this value is used in a partial string match search of the `Shape` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?shape=<shape>`'}

sightings_query_startdate_dictionary = {'description':"`startdate` is a search parameter for the `query?` feature.", 'use':"`startdate` must be given a numerical `string` value in the following order: four-digit year, two-digit month, two-digit day (YYYYMMDD).  This value is used to filter out sightings that occurred before the specified `startdate` from the `DateOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?startdate=<YYYYMMDD>`'}

sightings_query_state_dictionary = {'description':"`state` is a search parameter for the `query?` feature.", 'use':"`state` must be given a `string` value, this value is used in a partial string match search of the `StateOrProvince` column of the database.  Some of the values from the `StateOrProvince` column have 'province' abbreviations instead of 'state' abbreviations. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?state=<stateabbreviation>`'}

sightings_query_year_dictionary = {'description':'`year` is a search parameter for the `query?` feature.', 'use':"`year` must be given a numerical `string` value as a four-digit year (YYYY).  This value is used in a literal string match search of the `YearOfSighting` column of the database. `input_format` shows static string requirements plainly whereas user input is shown wrapped within `<   >` but must not be wrapped in the `<   >` characters for the API call itself.", 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/query?year=<YYYY>`'}

sightings_today_dictionary = {'description':"`today` returns a list of sightings from this day in history (equivalent to `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?dayclass=<today's dayclass>` and `https://nuforc-sightings-database-api.herokuapp.com/sightings/query?month=<today's two-digit month>&day=<today's two-digit day>`)", 'use':'automatic', 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/today`'}

sightings_today_random_dictionary = {'description':'`random` returns a single sighting report from this day in history.', 'use':'automatic', 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/today/random`'}

sightings_today_rssxml_dictionary = {'description':"`rss.xml` is an rss feed that publishes information from the `today` endpoint", 'use':'automatic', 'input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sightings/today/rss.xml`'}

sitemap_dictionary = {'description':'`sitemap` returns a list of all available endpoints.','use':'automatic','input_format':'`https://nuforc-sightings-database-api.herokuapp.com/sitemap`'}

directory_list = [item.split('_')[:-1] for item in dir() if item.startswith("__") == False and item.startswith("endpoints") == False]
directory_list = sorted([directory for directory in directory_list if directory and directory != 'dictionary'])
endpoints_list = dict([zipped_dict for zipped_dict in zip([list_item[-1] for list_item in directory_list if list_item], sorted(['/'.join(list_item) for list_item in directory_list if list_item]))])

endpoints_documentation_dictionary = {'endpoints':{'endpoints':endpoints_list}}

target = endpoints_documentation_dictionary

def documentor(directory_list, target):
    for directory in directory_list:
        if directory:
            leaf_path = ''
            if len(directory) > 1:
                for i in range(len(directory[:-1])):
                    leaf_path += f"{directory[:i+1][-1]}."
                leaf_string = f"endpoints.{leaf_path}{directory[-1]}"
                leaf_key_assignment_string=leaf_string+'.'+directory[-1]
                leaf_value_assignment_string=f"{'_'.join(directory)}_dictionary"
            elif len(directory) == 1 and directory[-1] != 'dictionary':
                leaf_string = f"endpoints.{directory[-1]}"
                leaf_key_assignment_string=leaf_string+'.'+directory[-1]
                leaf_value_assignment_string=f"{'_'.join(directory)}_dictionary"
            try:
                spec = Assign(leaf_string, {f"{directory[-1]}": ''})
                target = glom(target, spec)
            except Exception:
                Exception
            try:
                spec = Assign(leaf_key_assignment_string, globals()[leaf_value_assignment_string])
                target = glom(target, spec)
            except Exception:
                Exception
    return target

def generate_documentation_examples(directory_list, dictionary, randomsightingfromtoday, rssfeed, sitemapper):
    root_directory = 'endpoints'
    try:
        shutil.rmtree(root_directory)
    except:
        Exception
    for directory in directory_list:
        if directory:
            leaf_path = ''
            if os.path.isdir(root_directory) == False:
                os.mkdir(root_directory)
            if len(directory) == 1:
                if not os.path.isdir(f'{root_directory}/{directory[0]}'):
                    os.mkdir(f'{root_directory}/{directory[0]}')
            for i in range(len(directory)):
                leaf_path += f'{directory[:i+1][-1]}/'
                if not os.path.isdir(f'{root_directory}/{leaf_path}'):
                    os.mkdir(f'{root_directory}/{leaf_path}')
            if directory[-1] != 'index' and directory[-1] != 'random'  and directory[-1] != 'rssxml' and directory[-1] != 'sitemap' and directory[-1] != 'today':
                with open(f'endpoints/{leaf_path}{directory[-1]}.txt', 'w') as output_file:
                    json.dump(dictionary[i], output_file)
            elif directory[-1] == 'random' or directory[-1] == 'today':
                with open(f'endpoints/{leaf_path}{directory[-1]}.txt', 'w') as output_file:
                    json.dump(randomsightingfromtoday, output_file)
            elif directory[-1] == 'rssxml':
                with open(f'endpoints/{leaf_path}{directory[-1]}.txt', 'w') as output_file:
                    json.dump(rssfeed, output_file)
            elif directory[-1] == 'sitemap':
                with open(f'endpoints/{leaf_path}{directory[-1]}.txt', 'w') as output_file:
                    json.dump(sitemapper, output_file)
    