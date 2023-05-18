import os
import json
import datetime
import numpy as np
import PySimpleGUI as sg
from backend import check_filenames, extract_vals_from_dict, download_weather_data
from frontend import init_layout, init_gui, add_figs_to_gui

location = "Jena"
weather_data_path = "/home/jonas/Desktop/daily_gui/data/weather_data/"
now = datetime.datetime.now()
filename = now.strftime("%Y_%m_%d_") + location + ".json"
filepath = os.path.join(weather_data_path, filename)

# Check if data has already been downloaded today
already_downloaded = check_filenames(weather_data_path, filename)

# Download data if necessary
if len(already_downloaded) == 0:
    download_weather_data(location, filepath)

# Load data
f = open(filepath)
api_result = json.load(f)

# Extract values
timestamps, temps, weather, prec_probs = extract_vals_from_dict(api_result)

# Get min and max temperature per day
minmax_timestamps = []
minmax_temps = []
unique_dates = np.unique([i[0:10] for i in timestamps])
for date in unique_dates:
    # Get all data points corresponding to a given date
    sub_timestamp_indices = np.asarray([date in i for i in timestamps]).nonzero()[0]
    sub_timestamps = [timestamps[i] for i in sub_timestamp_indices]
    sub_temps = [temps[i] for i in sub_timestamp_indices]
    # Get exact timestamp and temperature for max and min temperature on that date
    max_temp = np.max(sub_temps)
    min_temp = np.min(sub_temps)
    max_temp_index = sub_temps.index(max_temp)
    min_temp_index = sub_temps.index(min_temp)
    max_temp_timestamp = sub_timestamps[max_temp_index]
    min_temp_timestamp = sub_timestamps[min_temp_index]
    # Add results to corresponding lists
    minmax_timestamps.append(max_temp_timestamp)
    minmax_timestamps.append(min_temp_timestamp)
    minmax_temps.append(max_temp)
    minmax_temps.append(min_temp)

# Construct GUI
layout = init_layout()
layout.append([sg.Text('This is text')])
gui = init_gui(layout)


test_string = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


#gui = init_gui()
add_figs_to_gui(gui, timestamps, temps, prec_probs, minmax_timestamps, minmax_temps)

# show GUI
gui.read()
gui.close()
