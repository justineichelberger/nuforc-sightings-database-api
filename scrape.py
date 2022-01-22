import glob
import os
import pandas as pd
import re
import shutil
import sqlite3

from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
from datetime import date, datetime, time 
from rq import Connection, Queue, Worker 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from splinter import Browser
from time import strftime, strptime
from utilities import duration_normalizer, two_digits_from_digits 
from webdriver_manager.chrome import ChromeDriverManager

# last update on this date and time
def timestamptopath():
    timepublished = datetime.now()
    yearpublished = str(timepublished.year)
    monthpublished  = two_digits_from_digits(timepublished.month)
    daypublished = two_digits_from_digits(timepublished.day)
    hourpublished = two_digits_from_digits(timepublished.hour)
    minutepublished = two_digits_from_digits(timepublished.minute)
    secondpublished = two_digits_from_digits(timepublished.second)
    timestampstring = f'_{yearpublished}_{monthpublished}_{daypublished}_{hourpublished}_{minutepublished}_{secondpublished}'
    return timestampstring

# set base url for webscrape
base_url = "http://www.nuforc.org/webreports/"

# complete webscraping process for entire database
def scrape(base_url):
## move most recently updated database to backup directory
    try:
        if os.path.exists(sorted(glob.glob('./database/nuforc_sightings*.db'))[0]):
            for file in sorted(glob.glob('./database/nuforc_sightings*.db')):
                newbackupfile = file.split('/')[-1]
                try: 
                    if os.path.exists(sorted(glob.glob('./database/backup/nuforc_sightings*.db'))[0]):
                        for backupfile in sorted(glob.glob('./database/backup/nuforc_sightings*.db')):
                                os.remove(backupfile)
                        shutil.move(file, f'./database/backup/{newbackupfile}')
                except Exception:
                    Exception
    except Exception:
        Exception
## initialize database connection
    timestampstring = timestamptopath()
    database_connection = sqlite3.connect(f'./database/nuforc_sightings{timestampstring}.db')
    database_cursor = database_connection.cursor()
### create table
    database_cursor.execute('''CREATE TABLE nuforcSightings
               (DateAndTime text, CityAndOrCountry text, StateOrProvince text, Shape text, Duration text, SummaryIncipit text, DateReportWasPublished text, DateOfSighting integer, YearOfSighting integer, MonthOfSighting integer, DayOfSighting integer, MinimumDuration real, MaximumDuration real,  CompleteSummaryURL text, CompleteSummary text)''')    
## initialize webscraping parameters
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    database_url = "http://www.nuforc.org/webreports/ndxevent.html"
## visit full database index page
    browser.visit(database_url)
    search_html = browser.html
## iterate through full database index page
    for link in bs(search_html, parse_only=ss('a'), features="lxml"):   
### isolate href links text and have browser visit each link
        if link.has_attr('href'):
            report_url = f"{base_url}{link['href']}"
            report_month = report_url[-7:-5]
            report_year = report_url[-11:-7]
### visit each month's reports page
            browser.visit(report_url)
            report_html = bs(browser.html, 'html.parser')
            try:
                # print(link) 
                report_data_headers = report_html.thead.find_all('tr')
                # print(report_data_headers)
            except Exception:
                report_data_headers = []
#### obtain complete list of data rows for each monthly report
            for header in report_data_headers:
                counter = 0
                report_data = report_html.tbody.find_all('tr')
##### for each row of data
                for row in report_data:
                    counter += 1
##### first obtain a list of column names
                    if counter == 1:
                        header_list = pd.Series(header.text.split('\n'))
                        print(header_list)
##### subsequently, obtain a list of row data
                    row_list = pd.Series(row.text.split('\n'))
##### prepare a row of data to be appended to today_in_ufo_sigthings_df dataframe
                    row_dictionary = dict(zip(header_list, row_list))
                    del row_dictionary[""]
##### add 'DateOfSighting', 'YearOfSighting', 'MonthOfSighting', 'DayOfSighting', 'MinimumDuration', and 'MaximumDuration' columns to database
                    try:
                        row_year = str(report_year.zfill(4))
                        print('year', row_year)
                        row_month = str(report_month.zfill(2))
                        print('month', row_month)
                        row_day = row.a.text.split('/')[1]
                        row_day = str(row_day.zfill(2))
                        print('day', row_day)
                        row_dictionary['DateOfSighting'] = f'{row_year}{row_month}{row_day}'
                        row_dictionary['YearOfSighting'] = int(row_year)
                        row_dictionary['MonthOfSighting'] = int(row_month)
                        row_dictionary['DayOfSighting'] = int(row_day)
                    except Exception:
                        row_dictionary['DateOfSighting'] = ''
                        row_dictionary['YearOfSighting'] = ''
                        row_dictionary['MonthOfSighting'] = ''
                        row_dictionary['DayOfSighting'] = ''
                    try:    
                        row_dictionary['MinimumDuration'] = duration_normalizer(row_dictionary['Duration'])[0]
                        row_dictionary['MaximumDuration'] = duration_normalizer(row_dictionary['Duration'])[1]
                    except Exception:                       
                        row_dictionary['MinimumDuration'] = row_dictionary['Duration']                   
                        row_dictionary['MaximumDuration'] = row_dictionary['Duration']
###### visit each sigthing's webpage
                    for link in row.find_all('a'):
                        cell_counter = 0
                        report_card_string = f"{base_url}{link.get('href')}"
                        browser.visit(report_card_string)
                        report_card_html = bs(browser.html, 'html.parser')
###### append each sighting's full summary text and full summary's URL to sighting dictionary
                        row_dictionary['url'] = report_card_string
                        try:
                            report_card_html_iterated = [cell for cell in report_card_html.tbody.find_all('font')]
                            # print(len(report_card_html_iterated))
                            if len(report_card_html_iterated) > 1:
                                for cell in report_card_html.tbody.find_all('font'):
                                    cell_counter += 1
                                    if cell_counter == 2:
                                        row_dictionary['Full Summary'] = cell.get_text()
                            else: 
                                row_dictionary['Full Summary'] = row_dictionary['Summary']
                        except Exception:
                            row_dictionary['Full Summary'] = row_dictionary['Summary']
                    rowObject = row_dictionary.values()
                    rowList = [item for item in rowObject]
                    # print(tuple(rowList))
                    database_cursor.execute('''INSERT INTO nuforcSightings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(rowList))
                    database_connection.commit()
    browser.quit()
    database_connection.close()
    return report_url

scrape(base_url)