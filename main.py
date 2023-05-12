import os
import json
import requests
import datetime
from backend import extract_vals_from_dict
from frontend import init_gui, add_figs_to_gui

location = "Jena"

# Check if data has already been downloaded today
now = datetime.datetime.now()
weatherfiles = os.listdir("/home/jonas/Desktop/daily_gui/data/weather_data/")
date_now = now.strftime("%Y_%m_%d")
already_downloaded = any([date_now in filename for filename in weatherfiles])

if not already_downloaded:
    # Download and store data
    api_address = "api.openweathermap.org/data/2.5/forecast?q=" + location + ",units=metric,ger&appid=ca3c615c20062c4fed7b25374cb16a77"
    api_result = requests.get(api_address)
    filepath = now.strftime("%Y_%m_%d_%H_%M_") + location + ".json"
    with open(filepath,"w") as fp:
        json.dump(api_result, fp)

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
