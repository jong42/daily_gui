import os
import json
import requests
import datetime
import numpy as np
from backend import extract_vals_from_dict
from frontend import init_gui, add_figs_to_gui

location = "Jena"
weather_data_path = "/home/jonas/Desktop/daily_gui/data/weather_data/"
# Check if data has already been downloaded today
now = datetime.datetime.now()
weatherfiles = os.listdir(weather_data_path)
date_now = now.strftime("%Y_%m_%d")
already_downloaded = np.where([date_now in i for i in weatherfiles])[0]

if any(already_downloaded):
    filename = weatherfiles[already_downloaded[0]]
    filepath = os.path.join(weather_data_path, filename)
else:
    # Download and store data
    api_address = "https://api.openweathermap.org/data/2.5/forecast?q=" + location + ",units=metric,ger&appid=ca3c615c20062c4fed7b25374cb16a77"
    api_result = requests.get(api_address)
    filename = now.strftime("%Y_%m_%d_%H_%M_") + location + ".json"
    filepath = os.path.join(weather_data_path, filename)
    with open(filepath,"w") as fp:
        json.dump(api_result.json(), fp)

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
