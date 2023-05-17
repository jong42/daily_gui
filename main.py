import os
import json
import datetime
from backend import check_filenames, extract_vals_from_dict, download_weather_data
from frontend import init_gui, add_figs_to_gui

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

# Construct GUI
gui = init_gui()
add_figs_to_gui(gui, timestamps, temps, prec_probs)

# show GUI
gui.read()
gui.close()
