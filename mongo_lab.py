#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 17:17:13 2022

@author: thomasmurray
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

# Read in data associating zipcodes with lat/long coordinates. The file
# must be downloaded locally and is available on Git. The data was obtained from
# the following link:
#https://gist.github.com/senning/58a8c82e0c97712eabbe4700ce2187a1#file-us-zip-codes-from-2016-government-data 
geo_data = pd.read_csv(r'geo_data.csv')

geo_data['ZIP'] = geo_data['ZIP'].astype(str).str.zfill(5)

# Obtain a zipcode from user
area_code = input('Gimme a zipcode: ')

# Find the lat/long coords associated with the zipcode
lat = geo_data.loc[geo_data['ZIP'] == area_code].iloc[0][1]

lng = geo_data.loc[geo_data['ZIP'] == area_code].iloc[0][2]


# Create a URL for the National Weather Service report on this lat/long coord.
url = 'https://forecast.weather.gov/MapClick.php?lat={}&lon={}#.Y2xx3uxOm3J'.format(lat, lng)

# Ping the URL and begin parsing
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

# Obtain data on the 7-day forecast
seven_day = soup.find(id='seven-day-forecast-container')
forecast_items = seven_day.find_all(class_='tombstone-container')

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
short_descs = [sd.get_text() for sd in seven_day.select('.tombstone-container .short-desc')]
temps = [t.get_text() for t in seven_day.select('.tombstone-container .temp')]
descs = [d['title'] for d in seven_day.select('.tombstone-container img')]

# Create a dataframe containing the 7-day forecast
weather = pd.DataFrame({
    'period': periods,
    'short_desc': short_descs,
    'temp': temps,
    'desc': descs
})

# Display to user the forecast for each day
for each in descs:
    print(each)

# Obtain data on the current conditions
current_conds = soup.find(id='current_conditions_detail')
current_conds_items = current_conds.find_all('tr')

humidity = current_conds_items[0].get_text().strip().split('\n')[-1].strip()
wind_speed = current_conds_items[1].get_text().strip().split('\n')[-1].strip()
dew_point = current_conds_items[3].get_text().strip().split('\n')[-1].strip()
last_update = current_conds_items[-1].get_text().strip().split('\n')[-1].strip()

# Disply to user the current conditions
print('The current humidity is', humidity)
print('The current wind speed is', wind_speed)
print('The current dew point is', dew_point)
print('The current conditions were last updated', last_update)

# Create a dataframe containing the current conditions
conditions = pd.DataFrame({
    'humidity': [humidity],
    'wind speed': [wind_speed],
    'dew point': [dew_point],
    'last update': [last_update]
})
