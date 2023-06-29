import PySimpleGUI as sg
from backend import (
    get_weather_data,
    get_minmax_values,
    get_weather_symbols,
)
from recipes_backend import load_recipes_from_json, delete_recipe, update_recipe
from frontend import init_layout, init_gui, add_fig_to_gui, show_gui

location = "Jena"
weather_data_path = "/home/jonas/Desktop/daily_gui/data/weather_data/"
weather_symbols_path = "/home/jonas/Desktop/daily_gui/symbols/"
recipes_path = "/home/jonas/Desktop/daily_gui/data/recipes.json"

# Get weather data and process it
timestamps, temps, weather, prec_probs = get_weather_data(weather_data_path, location)
minmax_timestamps, minmax_temps = get_minmax_values(timestamps, temps)
symbols = get_weather_symbols(weather, weather_symbols_path)

# Get recipes
recipes = load_recipes_from_json(recipes_path)

# Construct GUI
layout = init_layout()
gui = init_gui(layout, recipes)
add_fig_to_gui(
    gui, timestamps, temps, prec_probs, minmax_timestamps, minmax_temps, symbols
)

# show GUI
show_gui(gui, recipes_path, recipes)
