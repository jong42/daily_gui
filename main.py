import PySimpleGUI as sg
from backend import (
    get_weather_data,
    get_minmax_values,
    get_weather_symbols,
)
from recipes_backend import load_recipes_from_json
from frontend import init_layout, init_gui, add_fig_to_gui

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
while True:
    event, values = gui.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == '-LIST-':
        update_name = values['-LIST-'][0]
        update_ingredients = recipes[update_name].ingredients
        for i, ingredient in enumerate(update_ingredients):
            element_name = '-INGREDIENTS' + str(i) + '-'
            gui[element_name].update(ingredient)
        # current fixed number of ingredients is 10, that's were the numbers come from
        for i in range(10 - len(update_ingredients)):
            element_name = '-INGREDIENTS' + str(9-i) + '-'
            gui[element_name].update("")
        update_preparation = recipes[update_name].preparation
        gui['-NAME-'].update(update_name)
        gui['-PREPARATION-'].update(update_preparation)
gui.close()







