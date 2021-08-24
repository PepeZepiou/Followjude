#!/usr/bin/python3

import requests
from requests import ConnectionError
from bs4 import BeautifulSoup
import sys
from datetime import datetime

logJ_path = './logJ.txt'
log_path = './log.txt'
# logJ_path = '/home/pi/Documents/logJ.txt'
# log_path = '/home/pi/Documents/log.txt'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.vesselfinder.com/fr',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}
url = 'https://www.vesselfinder.com/fr/vessels/JUDE-IMO-0-MMSI-329011750'
# Setup string for output (which will be logged in crontab.log)
output_date = '{:%d-%m-%Y %H:%M :  scrapper   : }'.format(datetime.now())


# Try to get html page
try:
    page = requests.get(url, headers=headers)
except ConnectionError:
    sys.exit(output_date + "ConnectionError")
# Parse html page
soup = BeautifulSoup(page.content, 'html.parser')
# 1st: find last position date/hour
step1 = soup.find('td', class_="v3 tooltip expand")
step2 = str(step1)
step3 = step2.split('=')[2]
date = step3.split('"')[1]
# 2nd: find latitude
step1 = soup.find('div', class_='coordinate lat')
lat = step1.string
# 3rd: find longitude
step1 = soup.find('div', class_='coordinate lon')
lon = step1.string
# 4th: format data
data = date + "\t" + lat + "\t" + lon + "\n"
# 5th: write data in log files
with open(logJ_path, 'a') as file:
    file.write(data)
with open(log_path, 'a') as file:
    file.write(data)
# Exit with return "Done" for crontab.log
sys.exit(output_date + "Done")
