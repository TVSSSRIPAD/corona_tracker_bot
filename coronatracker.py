#! /home/sripad/anaconda3/bin/python
import requests
from bs4 import BeautifulSoup
import datetime
import json
import argparse
import logging
from tabulate import tabulate
from slack_client import slacker

SHORT_HEADERS = ['S.No', 'State','People','Cured','D']
FILE_NAME = 'corona_india_data.json'
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]

parser  = argparse.ArgumentParser()
parser.add_argument('--states', default=',')
args = parser.parse_args()
interested_states = args.states.split(',')

current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
info = []

res = requests.get('https://www.mohfw.gov.in/')
soup =  BeautifulSoup(res.content , 'html.parser')

table = soup.find(class_ = 'data-table')
#print(table.prettify())
rows = soup.find_all('tr')
#print(rows)
stats = []

for row in rows:
    stat = extract_contents(row.find_all('td'))
    if stat:
        if len(stat) < 4:
            stat = []
        elif len(stat) ==4:
            stat = [' ', 'Total India',stat[1],stat[2],stat[3]]
            stats.append(stat)
        elif any([s.lower() in stat[1].lower() for s in interested_states]):
            stats.append(stat)

mytable = tabulate(stats, headers=SHORT_HEADERS, tablefmt='psql')
slack_text = f'Please find CoronaVirus Summary for India below:\n```{mytable}```'
slacker()(slack_text)

