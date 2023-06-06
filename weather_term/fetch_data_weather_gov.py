#!/usr/bin/env python3

import datetime
import json
import pathlib
import time

import matplotlib
import numpy as np
import requests

matplotlib.use('module://matplotlib-backend-kitty')
import matplotlib.pyplot as plt


def run():
    with pathlib.Path("~/.weather_term.json").expanduser().open() as infile:
        config = json.load(infile)
    ENDPOINT = f"https://api.weather.gov/gridpoints/{config['OFFICE']}/{config['GRID_X']}" \
               f",{config['GRID_Y']}/forecast/hourly"
    report_data = pathlib.Path("/tmp/results_weather_gov.json")

    now = time.time()
    if not report_data.exists() or (now - report_data.stat().st_mtime) >= 600:
        r = requests.get(ENDPOINT)
        with report_data.open('w') as results:
            results.write(r.text)
        data = r.json()
    else:
        with report_data.open() as data_file:
            data = json.load(data_file)

    report_periods = data['properties']['periods']
    times = [datetime.datetime.strptime(x['startTime'], "%Y-%m-%dT%H:%M:%S%z") for x in
             report_periods]
    thetas = [((x.hour + x.minute / 60) / 24) * np.pi * 2 for x in times]
    opacity = []
    temps = [x['temperature'] for x in report_periods]
    #
    with plt.style.context('seaborn-v0_8-notebook'):
        fig, ax = plt.subplots(1, 1)
        ax.plot(times, temps, label='Temperature')
        ax.grid(True)
        ax.legend()

    plt.show()


if __name__ == "__main__":
    run()
