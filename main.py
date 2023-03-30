import PySimpleGUI as sg
#import requests



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

### Create matplotlib plot ###

###Include plot into gui ###

layout = [[sg.Text("This is a line of text")], [sg.Text("This is another line of text")]]
window = sg.Window("daily_gui", layout)

window.read()