import requests
import csv
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import os.path
import datetime

# Download links from Network tab of Developer Tools
# Source: https://www.reddit.com/r/html5/comments/9f8knj/how_do_i_find_hidden_download_links_on_click_to/

# facebook
url = 'https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222021-11-29T05%5C%5C%3A15%5C%5C%3A59%202021-12-06T05%5C%5C%3A15%5C%5C%3A59%22%2C%22resolution%22%3A%22HOUR%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22facebook%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22CM%22%2C%22category%22%3A0%7D%7D&token=APP6_UEAAAAAYa7uD93nNiPbvBMib2tBL4gceFan1PNM&tz=300'
# url = 'https://trends.google.com/trends/explore?date=now%207-d&q=facebook'
r = requests.get(url, allow_redirects=True)
open('facebook_lowercase.csv', 'wb').write(r.content)


# Source: https://stackoverflow.com/questions/59970956/delete-first-rows-of-csv-file-in-python
with open("facebook_lowercase.csv",'r') as f, open("facebook_lowercase_temp.csv",'w') as f1:
    for i in range(3):
        next(f) # skip header line
    for line in f:
        # Only hours that stock market is open
        if ("T10," in line) or ("T11," in line) or ("T12," in line) or ("T13," in line) or ("T14," in line) or ("T15," in line) or ("T16," in line):
            f1.write(line)
    
    # for line in f:
    #     line[0] = datetime.datetime.strptime(line[0], '%Y-%m-%dT%H')
    #     f1.write(line)


# Create header row of final csv
# Source: https://stackoverflow.com/questions/39662891/read-in-the-first-column-of-a-csv-in-python/39662990
with open("facebook_lowercase_temp.csv",'r') as f, open("final.csv",'w') as f1:
    csv_reader = csv.reader(f, delimiter=',')
    # Leave space for first empty entry of first row
    f1.write(' ')
    for row in csv_reader:
        # Convert time to datetime format
        # Source: https://stackabuse.com/converting-strings-to-datetime-in-python/
        if datetime.datetime.strptime(row[0], '%Y-%m-%dT%H').weekday() < 5:
            f1.write(',' + str(datetime.datetime.strptime(row[0], '%Y-%m-%dT%H')))
    f1.write(',target\n')

with open("facebook_lowercase_temp.csv",'r') as f, open("final.csv",'a') as f1:
    csv_reader = csv.reader(f, delimiter=',')
    f1.write('facebook')
    for row in csv_reader:
        if datetime.datetime.strptime(row[0], '%Y-%m-%dT%H').weekday() < 5:
            f1.write(',' + row[1])
    f1.write(',neutral')


# Source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_html.html
# to read csv file
a = pd.read_csv("final.csv")
    
# to save as html file
# named as "Table"
a.to_html("table.html", index=False, border=None)

# assign it to a
# variable (string)
html_file = a.to_html()
