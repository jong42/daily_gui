from typing import List
import PySimpleGUI as sg
#import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def extract_vals_from_dict(d:dict) -> [List,List,List,List]:
    """
    Extract data on time stamps, temperature, weather status and precipitation probability from dictionary downloaded
    from openweathermap
    :param d: dictionary
    :return:
        timestamps: list of timestamps
        temps: list of temperature values
        weather_status: list of weather status values
        prec_probs: list of precipitation probabilities
    """

    timestamps = []
    temps = []
    weather = []
    prec_probs = []

    for entry in d['list']:
        timestamp = entry['dt_txt']
        temp = entry['main']['temp']
        weather_status = entry['weather'][0]['description']
        prec_prob = entry['pop']

        timestamps.append(timestamp)
        temps.append(temp)
        weather.append(weather_status)
        prec_probs.append(prec_prob)

    return timestamps, temps, weather, prec_probs

### handle api_call ###
#api_address = "api.openweathermap.org/data/2.5/forecast?q=Jena,ger&appid=ca3c615c20062c4fed7b25374cb16a77"
#api_result = requests.get(api_address)

#temporary workaround
import json
f = open("/home/jonas/Desktop/forecast.json")
api_result = json.load(f)

timestamps, temps, weather, prec_probs = extract_vals_from_dict(api_result)

###Construct GUI ###
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def init_gui():
    _VARS = {'window': False}
    layout = [[sg.Text("This is a line of text")], [sg.Text(temps[0])], [sg.Canvas(key='figCanvas')]]
    _VARS['window'] = sg.Window("daily_gui", layout, finalize=True)
    return _VARS

_VARS = init_gui()

### Create matplotlib plot ###

def add_fig_to_gui(gui):
    fig = plt.figure()
    plt.plot(timestamps, temps)
    # Instead of plt.show
    draw_figure(gui['window']['figCanvas'].TKCanvas, fig)

add_fig_to_gui(_VARS)

### show GUI
_VARS['window'].read()
_VARS['window'].close()
