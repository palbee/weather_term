#!/usr/bin/env python3

import datetime
import json
import pathlib
import time

import matplotlib
import matplotlib.pyplot as plt
import requests
from matplotlib.dates import DateFormatter, DayLocator, HourLocator

matplotlib.use('module://matplotlib-backend-kitty')

with pathlib.Path("~/.weather_term.json").expanduser().open() as infile:
    config = json.load(infile)

LAT = config['LAT']
LON = config['LON']
API = config['OPENWEATHER_API']

del config

ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
report_data = pathlib.Path("/tmp/results.json")

payload = {'appid': API,
           'lat': LAT,
           'lon': LON,
           'units': 'imperial'}

now = time.time()
if not report_data.exists() or (now - report_data.stat().st_mtime) >= 600:
    r = requests.get(ENDPOINT, params=payload)
    with report_data.open('w') as results:
        results.write(r.text)
    data = r.json()
else:
    with report_data.open() as data_file:
        data = json.load(data_file)

times = [datetime.datetime.fromtimestamp(x['dt']) for x in
         data['list']]
temps = [x['main']['temp'] for x in data['list']]
mintemps = [x['main']['temp_min'] for x in data['list']]
maxtemps = [x['main']['temp_max'] for x in data['list']]
feels = [x['main']['feels_like'] for x in data['list']]

with plt.style.context('seaborn-v0_8-notebook'):
    fig, ax = plt.subplots(1, 1)

    # ax.fill_between(times, mintemps, maxtemps)
    ax.plot(times, temps, label='Temperature')
    ax.plot(times, feels, label='Feels Like')

    ax.grid(True)
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_minor_locator(HourLocator(range(0, 25, 3)))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_minor_formatter(DateFormatter('%H'))

    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.legend()
    fig.autofmt_xdate()

plt.show()
