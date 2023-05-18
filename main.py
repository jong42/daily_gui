import os
import json
import datetime
import PySimpleGUI as sg
from backend import (
    check_filenames,
    extract_vals_from_dict,
    download_weather_data,
    get_minmax_values,
    get_weather_symbols,
)
from frontend import init_layout, init_gui, add_figs_to_gui

location = "Jena"
weather_data_path = "/home/jonas/Desktop/daily_gui/data/weather_data/"
weather_symbols_path = "/home/jonas/Desktop/daily_gui/symbols/"
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

timestamps = timestamps[0:20]
temps = temps[0:20]
weather = weather[0:20]
prec_probs = prec_probs[0:20]

# Get min and max temperature per day
minmax_timestamps, minmax_temps = get_minmax_values(timestamps, temps)

# Construct GUI
layout = init_layout()
layout.append(["This is a line of text"])
gui = init_gui(layout)
symbols = get_weather_symbols(weather, weather_symbols_path)
add_figs_to_gui(
    gui, timestamps, temps, prec_probs, minmax_timestamps, minmax_temps, symbols
)

# show GUI
gui.read()
gui.close()
