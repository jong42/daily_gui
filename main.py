import PySimpleGUI as sg
#import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

### handle api_call ###
#api_address = "api.openweathermap.org/data/2.5/forecast?q=Jena,ger&appid=ca3c615c20062c4fed7b25374cb16a77"
#api_result = requests.get(api_address)

#temporary workaround
import json
f = open("/home/jonas/Desktop/forecast.json")
api_result = json.load(f)

### Convert api result to array of values of interest ###
timestamps = []
temps = []
weather = []
prec_probs = []

for entry in api_result['list']:
    timestamp = entry['dt_txt']
    temp = entry['main']['temp']
    weather_status = entry['weather'][0]['description']
    prec_prob = entry['pop']

    timestamps.append(timestamp)
    temps.append(temp)
    weather.append(weather_status)
    prec_probs.append(prec_prob)
### pyplot integration to PySImpleGUI boilerplate

# VARS CONSTS:
_VARS = {'window': False}

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


###Construct GUI ###

layout = [[sg.Text("This is a line of text")], [sg.Text(temps[0])], [sg.Canvas(key='figCanvas')]]
_VARS['window'] = sg.Window("daily_gui", layout, finalize=True)



### Create matplotlib plot ###

fig = plt.figure()
plt.plot(timestamps, temps)
# Instead of plt.show
draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig)

### show GUI
_VARS['window'].read()
_VARS['window'].close()