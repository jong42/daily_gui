import os
import datetime
from backend import (
    get_weather_data,
    get_minmax_values,
    get_weather_symbols,
)
from frontend import init_layout, init_gui, add_fig_to_gui

location = "Jena"
weather_data_path = "/home/jonas/Desktop/daily_gui/data/weather_data/"
weather_symbols_path = "/home/jonas/Desktop/daily_gui/symbols/"
recipes_path = "/home/jonas/Desktop/daily_gui/data/recipes.json"

timestamps, temps, weather, prec_probs = get_weather_data(weather_data_path, location)

# Get min and max temperature per day
minmax_timestamps, minmax_temps = get_minmax_values(timestamps, temps)

# Construct GUI
layout = init_layout()
gui = init_gui(layout)
symbols = get_weather_symbols(weather, weather_symbols_path)
add_fig_to_gui(
    gui, timestamps, temps, prec_probs, minmax_timestamps, minmax_temps, symbols
)

# show GUI
gui.read()
gui.close()
