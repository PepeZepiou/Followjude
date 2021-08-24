#!/usr/bin/python3

import smtplib
from email.message import EmailMessage
import math
import socket
import sys
from datetime import datetime

# Declare all variables
username = "your_username"
password = "your_password"
path = "/home/pi/Documents/logJ.txt"
# path = "./logJ.txt"
text = ""
body = ""
lat = []
lon = []
data2 = []
lines = []
# Setup string for output (which will be logged in crontab.log)
output_date = '{:%d-%m-%Y %H:%M : mail_sender : }'.format(datetime.now())

# Read raw data from daily_log
with open(path, 'r') as file:
    data = file.readlines()

# In case of troubles with scrapper, sometimes there is date, but no positions in log.
# This block remove corrupted lines
for line in data:
    try:
        lat.append(float(line.split('\t')[-2]))
        lon.append(float(line.split('\t')[-1]))
        data2.append(line)
    except ValueError:
        pass

# Check number of points
numOfLine = len(lon)

# This block calculate orthodromic distance between point and the and previous one.
# If distance is lower than definite distance (here 20m), point is not stored.
# This can reduce the number of point on the map.
for i in range(1, numOfLine):
    L1 = math.radians(lat[i])
    L2 = math.radians(lat[i-1])
    G21 = math.radians(lon[i-1] - lon[i])
    M = 1852 * 60 * math.degrees(math.acos((math.sin(L1)*math.sin(L2)) + (math.cos(L1)*math.cos(L2)*math.cos(G21))))
    if M > 20:
        lines.append(data2[i])

# Remove first line of data if still the first of raw data.
# (First line of daily log is same as last of previous day)
if data[0] in lines:
    lines = lines[1:]

# Re_create text from list
for line in lines:
    text += line

# Remove non-ASCII symbols
for symbol in text:
    if symbol.isascii():
        body += symbol

# Create Email message
msg = EmailMessage()
msg['From'] = username
msg['To'] = username
msg['Subject'] = 'Data'
msg.set_content(body)

# Try to connect and log to mail server
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
except socket.gaierror:
    sys.exit(output_date + "ConnectionError")
server.login(username, password)
# Send email
server.send_message(msg)
# Disconnect to mail server
server.quit()
# Exit with return "Done" for crontab.log
sys.exit(output_date + "Done")
